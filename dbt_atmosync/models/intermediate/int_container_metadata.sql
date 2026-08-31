WITH latest_telemetry AS (
    SELECT
        container_id,
        commodity,
        origin,
        destination,
        latitude AS current_latitude,
        longitude AS current_longitude,
        temperature AS current_temperature,
        humidity AS current_humidity,
        vibration AS current_vibration,
        event_timestamp AS last_event_timestamp,
        ROW_NUMBER() OVER (PARTITION BY container_id ORDER BY event_timestamp DESC) AS rn
    FROM {{ ref('stg_telemetry') }}
),

ref_metadata AS (
    SELECT
        commodity,
        CASE 
            WHEN commodity = 'Fresh Produce' THEN 2.0
            WHEN commodity = 'Dairy' THEN 0.0
            WHEN commodity = 'Frozen Food' THEN -20.0
            WHEN commodity = 'Seafood' THEN -2.0
            WHEN commodity = 'Pharmaceuticals' THEN 2.0
            ELSE 0.0
        END AS temp_min,
        CASE 
            WHEN commodity = 'Fresh Produce' THEN 8.0
            WHEN commodity = 'Dairy' THEN 4.0
            WHEN commodity = 'Frozen Food' THEN -12.0
            WHEN commodity = 'Seafood' THEN 2.0
            WHEN commodity = 'Pharmaceuticals' THEN 8.0
            ELSE 10.0
        END AS temp_max,
        CASE 
            WHEN commodity = 'Fresh Produce' THEN 48.0
            WHEN commodity = 'Dairy' THEN 24.0
            WHEN commodity = 'Frozen Food' THEN 96.0
            WHEN commodity = 'Seafood' THEN 36.0
            WHEN commodity = 'Pharmaceuticals' THEN 72.0
            ELSE 48.0
        END AS spoilage_baseline_hours,
        CASE 
            WHEN commodity = 'Fresh Produce' THEN 500000.0
            WHEN commodity = 'Dairy' THEN 750000.0
            WHEN commodity = 'Frozen Food' THEN 1200000.0
            WHEN commodity = 'Seafood' THEN 1500000.0
            WHEN commodity = 'Pharmaceuticals' THEN 2500000.0
            ELSE 500000.0
        END AS cargo_base_value_inr
    FROM (
        SELECT DISTINCT commodity FROM latest_telemetry
    ) c
)

SELECT
    t.container_id,
    t.commodity,
    t.origin,
    t.destination,
    t.current_latitude,
    t.current_longitude,
    t.current_temperature,
    t.current_humidity,
    t.current_vibration,
    t.last_event_timestamp,
    m.temp_min AS safe_temp_min,
    m.temp_max AS safe_temp_max,
    m.spoilage_baseline_hours,
    m.cargo_base_value_inr
FROM latest_telemetry t
LEFT JOIN ref_metadata m ON t.commodity = m.commodity
WHERE t.rn = 1
