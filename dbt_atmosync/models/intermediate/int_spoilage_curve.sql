WITH base_meta AS (
    SELECT * FROM {{ ref('int_container_metadata') }}
),

degradation_calc AS (
    SELECT
        container_id,
        commodity,
        origin,
        destination,
        current_latitude,
        current_longitude,
        current_temperature,
        current_humidity,
        current_vibration,
        last_event_timestamp,
        safe_temp_min,
        safe_temp_max,
        spoilage_baseline_hours,
        cargo_base_value_inr,
        
        -- Temperature Deviation above upper threshold or below lower threshold
        CASE 
            WHEN current_temperature > safe_temp_max THEN current_temperature - safe_temp_max
            WHEN current_temperature < safe_temp_min THEN safe_temp_min - current_temperature
            ELSE 0.0
        END AS temp_deviation,

        -- Vibration risk multiplier
        CASE 
            WHEN current_vibration > 0.5 THEN (current_vibration - 0.5) * 1.5
            ELSE 0.0
        END AS vibration_penalty

    FROM base_meta
),

spoilage_summary AS (
    SELECT
        *,
        -- Compound Degradation Factor
        (1.0 + (temp_deviation * 0.45) + vibration_penalty) AS degradation_rate_multiplier,
        
        -- Remaining Safe Shelf Life in Hours
        GREATEST(0.5, spoilage_baseline_hours / (1.0 + (temp_deviation * 0.45) + vibration_penalty)) AS estimated_time_to_spoilage_hours
    FROM degradation_calc
)

SELECT
    container_id,
    commodity,
    origin,
    destination,
    current_latitude,
    current_longitude,
    current_temperature,
    current_humidity,
    current_vibration,
    last_event_timestamp,
    safe_temp_min,
    safe_temp_max,
    spoilage_baseline_hours,
    cargo_base_value_inr,
    temp_deviation,
    degradation_rate_multiplier,
    estimated_time_to_spoilage_hours,
    LEAST(1.0, GREATEST(0.0, 1.0 - (estimated_time_to_spoilage_hours / spoilage_baseline_hours))) AS spoilage_probability,
    CASE 
        WHEN estimated_time_to_spoilage_hours <= 12.0 OR temp_deviation >= 8.0 THEN 'CRITICAL'
        WHEN estimated_time_to_spoilage_hours <= 24.0 OR temp_deviation >= 4.0 THEN 'HIGH'
        WHEN estimated_time_to_spoilage_hours <= 36.0 OR temp_deviation >= 1.5 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_level
FROM spoilage_summary
