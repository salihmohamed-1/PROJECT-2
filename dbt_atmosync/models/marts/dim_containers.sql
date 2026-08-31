WITH metadata AS (
    SELECT * FROM {{ ref('int_container_metadata') }}
)

SELECT
    container_id,
    commodity,
    origin,
    destination,
    safe_temp_min,
    safe_temp_max,
    spoilage_baseline_hours,
    cargo_base_value_inr,
    last_event_timestamp AS last_active_at
FROM metadata
