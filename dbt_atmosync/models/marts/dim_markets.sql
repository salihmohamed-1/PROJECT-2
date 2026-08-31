WITH candidate_markets AS (
    SELECT 'Chennai' AS market_name, 'Tamil Nadu' AS state, 13.0827 AS latitude, 80.2707 AS longitude UNION ALL
    SELECT 'Bangalore' AS market_name, 'Karnataka' AS state, 12.9716 AS latitude, 77.5946 AS longitude UNION ALL
    SELECT 'Hyderabad' AS market_name, 'Telangana' AS state, 17.3850 AS latitude, 78.4867 AS longitude UNION ALL
    SELECT 'Mumbai' AS market_name, 'Maharashtra' AS state, 19.0760 AS latitude, 72.8777 AS longitude UNION ALL
    SELECT 'Delhi' AS market_name, 'NCR' AS state, 28.7041 AS latitude, 77.1025 AS longitude UNION ALL
    SELECT 'Kolkata' AS market_name, 'West Bengal' AS state, 22.5726 AS latitude, 88.3639 AS longitude
)

SELECT
    market_name,
    state,
    latitude,
    longitude
FROM candidate_markets
