# AtmoSync Architecture Blueprint

## System Overview

AtmoSync is an enterprise real-time streaming analytics platform that monitors micro-climate parameters (temperature, humidity, vibration) inside perishable cargo shipping containers. It converts micro-climate drift into a financial **Spoilage Arbitrage Signal**, enabling commodity traders to dynamically reroute at-risk containers to optimal destination markets before product degradation occurs.

```
+--------------------------+
|  Python IoT Simulator    |  Generates real-time sensor drift & GPS telemetry
+------------+-------------+
             |
             v
+--------------------------+
|   Apache Kafka Topic     |  `container_telemetry` (3 partitions)
|  (container_telemetry)   |
+------------+-------------+
             |
             v
+--------------------------+
| Kafka Consumer / Loader  |  Micro-batch bulk loader with deduplication
+------------+-------------+
             |
             v
+--------------------------+
|   Snowflake RAW Schema   |  `ATMOSYNC.RAW.RAW_TELEMETRY` (Clustered)
+------------+-------------+
             |
             v
+--------------------------+
|   dbt Staging Models     |  Data cleaning, deduplication, schema validation
+------------+-------------+
             |
             v
+--------------------------+
| dbt Intermediate Models  |  Spoilage curve degradation & Haversine distances
+------------+-------------+
             |
             v
+--------------------------+
|     dbt Marts Layer      |  `FCT_SPOILAGE_ARBITRAGE` (Financial Arbitrage)
+------------+-------------+
             |
             +------------------------------+
             |                              |
             v                              v
+--------------------------+  +--------------------------+
|   Apache Superset BI     |  |  Slack & Email Notifier  |
|  Live Dashboard & KPIs   |  | Webhook Alerts on High   |
+--------------------------+  | Risk / Arbitrage Signal  |
                              +--------------------------+
```

## Core Pipeline Components

1. **Streaming Ingestion**: Python simulator models IoT sensors across containers. Messages are serialized as JSON and streamed via Kafka Producer to the `container_telemetry` topic.
2. **Cloud Warehouse Landing**: `snowflake_loader.py` consumes messages from Kafka, validates schema, deduplicates events, and bulk loads into Snowflake `RAW.RAW_TELEMETRY`.
3. **dbt ELT Transformation**:
   - `STAGING`: Deduplicates events, validates coordinates, and casts timestamps.
   - `INTERMEDIATE`: Calculates thermal exposure units, time-to-spoilage degradation curves, and Haversine distances to major Indian commercial hubs.
   - `MARTS`: Evaluates candidate destination market spot prices, calculates transport rerouting costs, computes Net Arbitrage Profit, and assigns action recommendations.
4. **BI & Alerting**: Apache Superset visualizes live container coordinates, temperature drift, and financial arbitrage metrics. Critical risk conditions automatically trigger Slack Block Kit and SMTP Email notifications.
