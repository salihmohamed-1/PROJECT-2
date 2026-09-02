-- Custom test: Ensures sensor telemetry metrics fall within valid physical bounds
SELECT
    event_id,
    container_id,
    temperature,
    humidity,
    latitude,
    longitude
FROM {{ ref('stg_telemetry') }}
WHERE humidity < 0 OR humidity > 100
   OR latitude < -90 OR latitude > 90
   OR longitude < -180 OR longitude > 180
