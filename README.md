# AtmoSync – Micro-Climate Arbitrage Analytics

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Kafka](https://img.shields.io/badge/streaming-Apache_Kafka-black.svg?logo=apachekafka)](https://kafka.apache.org/)
[![Snowflake](https://img.shields.io/badge/warehouse-Snowflake-29B5E8.svg?logo=snowflake)](https://www.snowflake.com/)
[![dbt](https://img.shields.io/badge/transform-dbt_core-FF694B.svg?logo=dbt)](https://www.getdbt.com/)
[![Superset](https://img.shields.io/badge/visualization-Apache_Superset-00A699.svg?logo=apache)](https://superset.apache.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 1. Overview

**AtmoSync** is an enterprise real-time streaming analytics platform designed to detect internal micro-climate anomalies (temperature, humidity, vibration shock) within perishable cargo shipping containers. By combining real-time IoT streaming, cloud warehousing, and analytics engineering, AtmoSync converts environmental sensor drift into a financial **Spoilage Arbitrage Signal**.

This financial metric enables commodities traders and logistics dispatchers to dynamically reroute at-risk shipping containers to optimal regional destination markets before cargo degradation occurs, maximizing recovered asset value.

---

## 2. Problem Statement & Use Case

Refrigerated shipping containers (*reefers*) carrying high-value perishables (fresh produce, dairy, seafood, pharmaceuticals) frequently experience cooling system degradation or road shock events during long-distance transits.
- **Traditional Approach**: Passive logging. Traders only discover spoilage upon container arrival at the final destination, resulting in 100% cargo loss.
- **AtmoSync Approach**: Active streaming arbitrage. AtmoSync continuously calculates remaining shelf life versus transit times to candidate regional spot markets, automatically triggering **Slack/Email reroute alerts** when rerouting yields a positive net financial return.

---

## 3. Architecture Blueprint

```
[Python IoT Simulator] ──> [Kafka Producer] ──> [Kafka Topic: container_telemetry]
                                                      │
                                                      ▼
[Apache Superset BI] <── [dbt Marts / Models] <── [Snowflake Warehouse] <── [Kafka Consumer Loader]
         │
         ▼
[Slack / Email Alerts]
```

### Data Pipeline Flow:
1. **IoT Simulation**: Multi-container IoT generator producing real-time GPS locations and micro-climate sensor drift.
2. **Kafka Streaming**: High-throughput message streaming via Kafka topic `container_telemetry`.
3. **Snowflake Ingestion**: Micro-batch Kafka consumer ingesting payloads into `ATMOSYNC.RAW.RAW_TELEMETRY`.
4. **dbt ELT Pipeline**:
   - `STAGING`: Deduplicates events, validates coordinates, and casts types.
   - `INTERMEDIATE`: Computes degradation rates, time-to-spoilage curves, and Haversine distance vectors.
   - `MARTS`: Calculates rerouting transport costs, spot price premiums, Net Arbitrage Profit, and action recommendations.
5. **BI & Alerting**: Apache Superset dashboard visualizing live container locations, drift curves, and automated Slack/Email alerts.

---

## 4. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend & Simulator** | Python 3.11+, Pandas, PyYAML | IoT telemetry simulation & core logic |
| **Streaming** | Apache Kafka, kafka-python | Real-time event streaming |
| **Cloud Warehouse** | Snowflake, snowflake-connector | Scalable raw & analytical data storage |
| **Transformation** | dbt Core, dbt-snowflake | Structured ELT data modeling & data quality testing |
| **Visualization** | Apache Superset | Real-time BI dashboarding |
| **Infrastructure** | Docker, Docker Compose | Containerized local environment |
| **Alerting** | Slack Webhooks, SMTP Email | Real-time alerts on critical risk / arbitrage signals |
| **Testing** | Pytest | Automated unit & integration testing |

---

## 5. Complete Folder Structure

```
atmosync/
├── data/
│   ├── raw/
│   └── sample_payloads/
│       ├── telemetry_sample.json
│       └── commodity_pricing.json
├── simulator/
│   ├── iot_simulator.py
│   ├── producer.py
│   └── config.yaml
├── kafka/
│   ├── docker-compose.kafka.yml
│   └── topic_config.json
├── warehouse/
│   ├── ddl/
│   │   ├── raw_tables.sql
│   │   └── clustering.sql
│   └── loader/
│       └── snowflake_loader.py
├── dbt_atmosync/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_telemetry.sql
│   │   │   ├── stg_commodity_pricing.sql
│   │   │   └── schema.yml
│   │   ├── intermediate/
│   │   │   ├── int_container_metadata.sql
│   │   │   ├── int_spoilage_curve.sql
│   │   │   ├── int_distance_to_market.sql
│   │   │   └── schema.yml
│   │   └── marts/
│   │       ├── fct_spoilage_arbitrage.sql
│   │       ├── dim_containers.sql
│   │       ├── dim_markets.sql
│   │       └── schema.yml
│   ├── tests/
│   │   ├── assert_positive_prices.sql
│   │   └── assert_valid_telemetry.sql
│   ├── dbt_project.yml
│   ├── profiles.yml.example
│   ├── packages.yml
│   └── sources.yml
├── superset/
│   ├── docker-compose.superset.yml
│   ├── dashboards/
│   │   └── dashboard_export.json
│   └── alerts/
│       └── alert_rules.json
├── scripts/
│   ├── orchestration/
│   │   ├── run_pipeline.py
│   │   └── scheduler.py
│   └── utils/
│       ├── logger.py
│       ├── config.py
│       ├── slack_alert.py
│       └── email_alert.py
├── notebooks/
│   └── exploration.ipynb
├── tests/
│   ├── unit/
│   │   ├── test_simulator.py
│   │   ├── test_payload_schema.py
│   │   ├── test_spoilage_logic.py
│   │   └── test_arbitrage_logic.py
│   └── integration/
│       ├── test_kafka_pipeline.py
│       └── test_end_to_end.py
├── docs/
│   ├── architecture.md
│   ├── setup_guide.md
│   ├── data_dictionary.md
│   ├── arbitrage_metric.md
│   └── troubleshooting.md
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md
├── .env.example
├── .gitignore
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 6. Mathematical Spoilage & Arbitrage Logic

### 6.1 Time to Spoilage Calculation
$$\text{Temperature Deviation } \Delta T = \max(0, T_{\text{curr}} - T_{\text{max}}) + \max(0, T_{\text{min}} - T_{\text{curr}})$$
$$\text{Degradation Rate Multiplier } M_{\text{deg}} = 1.0 + (\Delta T \times 0.45) + \text{Vibration Penalty}$$
$$\text{Time to Spoilage (TTS)} = \max\left(0.5, \frac{\text{Baseline Safe Hours}}{M_{\text{deg}}}\right)$$

### 6.2 Net Spoilage Arbitrage Profit Formula
$$\text{Net Arbitrage Profit } \Pi_{\text{net}} = (\text{Spoilage Loss} \times 0.90) + \text{Price Premium} - \text{Reroute Transport Cost}$$

An **Arbitrage Opportunity** is flagged when:
1. Container is classified as `HIGH` or `CRITICAL` risk.
2. Transit time to candidate market < Remaining Time to Spoilage.
3. $\Pi_{\text{net}} > 0$.

---

## 7. Quickstart Setup (Windows PowerShell)

### 7.1 Virtual Environment Setup
```powershell
# Enable local script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 7.2 Environment Configuration
```powershell
Copy-Item .env.example .env
```

### 7.3 Infrastructure (Kafka & Zookeeper)
```powershell
docker compose up -d
```

---

## 8. Execution Commands

### 8.1 Run IoT Simulator & Kafka Producer
```powershell
python simulator/producer.py
```

### 8.2 Run Snowflake Ingestion Loader
```powershell
python warehouse/loader/snowflake_loader.py
```

### 8.3 Run dbt Transformation & Quality Tests
```powershell
cd dbt_atmosync
dbt compile
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..
```

### 8.4 Run Full Master Pipeline
```powershell
python scripts/orchestration/run_pipeline.py
```

### 8.5 Run Automated Pytest Suite
```powershell
python -m pytest tests/unit -v
python -m pytest tests/integration -v
```

---

## 9. Team Collaboration & Git Workflow

Branches assigned per engineering responsibilities:

- **Salih (Team Lead)**: Architecture, Kafka streaming core, pipeline orchestration, integration merges.
  ```bash
  git checkout -b salih
  ```
- **Meegadeesh**: Snowflake database DDL, loader ingestion, clustering strategies.
  ```bash
  git checkout -b meegadeesh
  ```
- **Anusha**: dbt transformation modeling (staging/intermediate/marts), SQL testing, documentation.
  ```bash
  git checkout -b anusha
  ```
- **Member4**: Apache Superset dashboards, Slack/Email alerting, Docker containerization.
  ```bash
  git checkout -b member4
  ```

---

## 10. License

This project is open-source under the **MIT License**.
