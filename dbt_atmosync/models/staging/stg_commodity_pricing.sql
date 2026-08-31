WITH source_pricing AS (
    SELECT
        COALESCE(PRICE_ID, UUID_STRING())::VARCHAR AS price_id,
        TRIM(COMMODITY)::VARCHAR AS commodity,
        TRIM(MARKET)::VARCHAR AS market,
        PRICE_PER_UNIT_INR::FLOAT AS price_per_unit_inr,
        CURRENCY::VARCHAR AS currency,
        EFFECTIVE_TIMESTAMP::TIMESTAMP_NTZ AS effective_timestamp,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(COMMODITY), TRIM(MARKET) 
            ORDER BY EFFECTIVE_TIMESTAMP DESC
        ) AS latest_rank
    FROM {{ source('raw', 'COMMODITY_PRICING') }}
    WHERE PRICE_PER_UNIT_INR >= 0
)

SELECT
    price_id,
    commodity,
    market,
    price_per_unit_inr,
    currency,
    effective_timestamp
FROM source_pricing
WHERE latest_rank = 1
