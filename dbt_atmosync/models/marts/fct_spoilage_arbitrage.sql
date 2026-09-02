WITH spoilage_info AS (
    SELECT * FROM {{ ref('int_spoilage_curve') }}
),

market_distances AS (
    SELECT * FROM {{ ref('int_distance_to_market') }}
),

pricing_info AS (
    SELECT * FROM {{ ref('stg_commodity_pricing') }}
),

market_evaluation AS (
    SELECT
        s.container_id,
        s.commodity,
        s.origin,
        s.destination AS original_destination,
        s.current_temperature,
        s.current_humidity,
        s.current_vibration,
        s.last_event_timestamp,
        s.estimated_time_to_spoilage_hours,
        s.spoilage_probability,
        s.risk_level,
        s.cargo_base_value_inr,
        
        m.target_market,
        m.distance_km,
        m.estimated_transit_hours,
        m.reachable_before_spoilage,
        
        COALESCE(p.price_per_unit_inr, 50.0) AS target_market_unit_price,
        COALESCE(p_orig.price_per_unit_inr, 50.0) AS orig_market_unit_price,

        -- Freight cost calculation (₹45 per km transport fee)
        ROUND(m.distance_km * 45.0, 2) AS reroute_cost_inr,

        -- Expected loss if continuing on original route while degraded
        CASE 
            WHEN s.risk_level IN ('HIGH', 'CRITICAL') THEN s.cargo_base_value_inr * 0.75
            WHEN s.risk_level = 'MEDIUM' THEN s.cargo_base_value_inr * 0.30
            ELSE 0.0
        END AS estimated_spoilage_loss_inr

    FROM spoilage_info s
    JOIN market_distances m ON s.container_id = m.container_id
    LEFT JOIN pricing_info p ON s.commodity = p.commodity AND m.target_market = p.market
    LEFT JOIN pricing_info p_orig ON s.commodity = p_orig.commodity AND s.destination = p_orig.market
),

arbitrage_calc AS (
    SELECT
        *,
        -- Price premium ratio at destination market
        ((target_market_unit_price - orig_market_unit_price) / NULLIF(orig_market_unit_price, 0)) AS price_premium_ratio,

        -- Value saved by preventing spoilage through rerouting to closer/faster market
        CASE 
            WHEN reachable_before_spoilage THEN estimated_spoilage_loss_inr * 0.90
            ELSE 0.0
        END AS recovered_cargo_value_inr,

        -- Net Financial Arbitrage Profit
        CASE 
            WHEN reachable_before_spoilage THEN 
                (estimated_spoilage_loss_inr * 0.90) + 
                (cargo_base_value_inr * GREATEST(-0.1, ((target_market_unit_price - orig_market_unit_price) / NULLIF(orig_market_unit_price, 0)))) - 
                reroute_cost_inr
            ELSE -reroute_cost_inr
        END AS net_arbitrage_profit_inr

    FROM market_evaluation
),

ranked_recommendations AS (
    SELECT
        *,
        ROUND(
            LEAST(100.0, GREATEST(0.0, 
                (spoilage_probability * 40.0) + 
                (LEAST(500000.0, GREATEST(0.0, net_arbitrage_profit_inr)) / 500000.0 * 50.0) +
                (CASE WHEN reachable_before_spoilage THEN 10.0 ELSE 0.0 END)
            )), 1
        ) AS arbitrage_score,

        ROW_NUMBER() OVER (
            PARTITION BY container_id 
            ORDER BY 
                CASE WHEN reachable_before_spoilage THEN 1 ELSE 2 END,
                net_arbitrage_profit_inr DESC,
                distance_km ASC
        ) AS option_rank
    FROM arbitrage_calc
)

SELECT
    container_id,
    commodity,
    origin,
    original_destination,
    target_market AS recommended_market,
    current_temperature,
    current_humidity,
    current_vibration,
    risk_level,
    spoilage_probability,
    estimated_time_to_spoilage_hours,
    distance_km AS distance_to_recommended_market_km,
    estimated_transit_hours AS transit_hours_to_recommended_market,
    cargo_base_value_inr,
    estimated_spoilage_loss_inr,
    reroute_cost_inr,
    ROUND(net_arbitrage_profit_inr, 2) AS net_arbitrage_profit_inr,
    arbitrage_score,
    CASE 
        WHEN risk_level IN ('HIGH', 'CRITICAL') AND net_arbitrage_profit_inr > 0 AND reachable_before_spoilage THEN TRUE
        ELSE FALSE 
    END AS arbitrage_opportunity_flag,
    CASE 
        WHEN risk_level IN ('HIGH', 'CRITICAL') AND net_arbitrage_profit_inr > 0 AND reachable_before_spoilage 
            THEN CONCAT('RECOMMEND REROUTE -> ', target_market)
        WHEN risk_level IN ('HIGH', 'CRITICAL') AND NOT reachable_before_spoilage
            THEN 'CRITICAL SPOILAGE UNPREVENTABLE'
        ELSE 'NO REROUTE REQUIRED'
    END AS action_recommendation,
    last_event_timestamp
FROM ranked_recommendations
WHERE option_rank = 1
