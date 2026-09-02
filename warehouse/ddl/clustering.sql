-- =====================================================================
-- AtmoSync Snowflake Optimization & Clustering Strategy
-- =====================================================================

USE DATABASE ATMOSYNC;
USE SCHEMA RAW;

-- Define Clustering Key on RAW_TELEMETRY to optimize partition pruning by Container and Time
ALTER TABLE RAW.RAW_TELEMETRY CLUSTER BY (CONTAINER_ID, DATE(EVENT_TIMESTAMP));

-- Re-cluster execution statement (if dynamic maintenance is needed)
ALTER TABLE RAW.RAW_TELEMETRY RECLUSTER;

-- Search Optimization Service for high-cardinality container lookups
ALTER TABLE RAW.RAW_TELEMETRY ADD SEARCH OPTIMIZATION ON EQUALITY(CONTAINER_ID, EVENT_ID);
