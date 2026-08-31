WITH container_locations AS (
    SELECT
        container_id,
        commodity,
        current_latitude AS lat1,
        current_longitude AS lon1,
        estimated_time_to_spoilage_hours,
        risk_level
    FROM {{ ref('int_spoilage_curve') }}
),

candidate_markets AS (
    SELECT 'Chennai' AS market_name, 13.0827 AS lat2, 80.2707 AS lon2 UNION ALL
    SELECT 'Bangalore' AS market_name, 12.9716 AS lat2, 77.5946 AS lon2 UNION ALL
    SELECT 'Hyderabad' AS market_name, 17.3850 AS lat2, 78.4867 AS lon2 UNION ALL
    SELECT 'Mumbai' AS market_name, 19.0760 AS lat2, 72.8777 AS lon2 UNION ALL
    SELECT 'Delhi' AS market_name, 28.7041 AS lat2, 77.1025 AS lon2 UNION ALL
    SELECT 'Kolkata' AS market_name, 22.5726 AS lat2, 88.3639 AS lon2
),

cross_join_markets AS (
    SELECT
        c.container_id,
        c.commodity,
        c.lat1,
        c.lon1,
        c.estimated_time_to_spoilage_hours,
        c.risk_level,
        m.market_name,
        m.lat2,
        m.lon2,
        -- Distance in km using Haversine formula approximation (6371 km Earth radius)
        2 * 6371 * ASIN(
            SQRT(
                POWER(SIN(RADIANS(m.lat2 - c.lat1) / 2), 2) +
                COS(RADIANS(c.lat1)) * COS(RADIANS(m.lat2)) *
                POWER(SIN(RADIANS(m.lon2 - c.lon1) / 2), 2)
            )
        ) AS distance_km
    FROM container_locations c
    CROSS JOIN candidate_markets m
)

SELECT
    container_id,
    commodity,
    market_name AS target_market,
    lat1 AS container_latitude,
    lon1 AS container_longitude,
    lat2 AS market_latitude,
    lon2 AS market_longitude,
    ROUND(distance_km, 2) AS distance_km,
    -- Estimated travel time at average 60 km/h cargo transit speed + 1 hour handling buffer
    ROUND((distance_km / 60.0) + 1.0, 2) AS estimated_transit_hours,
    estimated_time_to_spoilage_hours,
    risk_level,
    CASE 
        WHEN ROUND((distance_km / 60.0) + 1.0, 2) < estimated_time_to_spoilage_hours THEN TRUE 
        ELSE FALSE 
    END AS reachable_before_spoilage
FROM cross_join_markets
