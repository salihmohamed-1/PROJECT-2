-- Custom test: Ensures no negative prices in commodity spot pricing
SELECT
    price_id,
    commodity,
    market,
    price_per_unit_inr
FROM {{ ref('stg_commodity_pricing') }}
WHERE price_per_unit_inr < 0
