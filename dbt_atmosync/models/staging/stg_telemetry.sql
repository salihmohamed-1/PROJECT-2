WITH source_data AS (
    SELECT
        EVENT_ID::VARCHAR AS event_id,
        CONTAINER_ID::VARCHAR AS container_id,
        EVENT_TIMESTAMP::TIMESTAMP_NTZ AS event_timestamp,
        TEMPERATURE::FLOAT AS temperature,
        HUMIDITY::FLOAT AS humidity,
        VIBRATION::FLOAT AS vibration,
        LATITUDE::FLOAT AS latitude,
        LONGITUDE::FLOAT AS longitude,
        ORIGIN::VARCHAR AS origin,
        DESTINATION::VARCHAR AS destination,
        COMMODITY::VARCHAR AS commodity,
        INGESTED_AT::TIMESTAMP_NTZ AS ingested_at,
        ROW_NUMBER() OVER (
            PARTITION BY EVENT_ID 
            ORDER BY INGESTED_AT DESC
        ) AS dedup_rank
    FROM {{ source('raw', 'RAW_TELEMETRY') }}
    WHERE CONTAINER_ID IS NOT NULL
      AND EVENT_ID IS NOT NULL
      AND LATITUDE BETWEEN -90 AND 90
      AND LONGITUDE BETWEEN -180 AND 180
)

SELECT
    event_id,
    container_id,
    event_timestamp,
    temperature,
    humidity,
    vibration,
    latitude,
    longitude,
    origin,
    destination,
    commodity,
    ingested_at
FROM source_data
WHERE dedup_rank = 1
