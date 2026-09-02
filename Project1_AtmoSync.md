# PROJECT 1 — "AtmoSync": Micro-Climate Arbitrage Analytics
### Infotact Solutions — 4-Week Team Execution Plan
**Team:** Salih (Team Lead), Meegadeesh, Anusha, Member4

---

## PART 1 — PROJECT FOUNDATION

### 1.1 Project Overview
AtmoSync is a real-time streaming analytics platform that detects micro-climate drift inside shipping
containers (temperature, humidity, vibration) and converts that drift into a financial "Spoilage
Arbitrage" signal, so a commodities trader can reroute at-risk shipments to a closer market before the
goods degrade. The system ingests continuous mock IoT telemetry, stores and models it in a cloud
warehouse, and visualizes live arbitrage opportunities on a BI dashboard with automated alerts.

### 1.2 Technology Stack
| Layer | Technology | Purpose |
|---|---|---|
| Ingestion | Apache Kafka | High-throughput streaming of IoT telemetry |
| Simulation | Python | Mock IoT sensor data generator |
| Warehouse | Snowflake | Storage of raw + modeled data |
| Transformation | dbt (core) | ELT modeling, spoilage/arbitrage SQL logic |
| Visualization | Apache Superset | Real-time BI dashboard |
| Orchestration/Ops | Docker, Docker Compose | Local environment for Kafka, Superset |
| Alerting | Slack/Email webhook | Arbitrage opportunity alerts |
| Version Control | Git / GitHub | Branch-based team collaboration |

### 1.3 Folder Structure (Target End-State)
```
atmosync/
├── data/
│   ├── raw/
│   └── sample_payloads/
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
│   │   ├── intermediate/
│   │   └── marts/
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml.example
├── superset/
│   ├── docker-compose.superset.yml
│   ├── dashboards/
│   └── alerts/
├── scripts/
│   ├── orchestration/
│   └── utils/
├── notebooks/
│   └── exploration.ipynb
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   ├── architecture.md
│   ├── setup_guide.md
│   └── data_dictionary.md
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md
├── requirements.txt
├── README.md
└── .gitignore
```

### 1.4 Architecture
```
[Python IoT Simulator] → [Kafka Producer] → [Kafka Topic: container_telemetry]
      → [Kafka Consumer / Loader] → [Snowflake RAW schema]
      → [dbt staging models] → [dbt intermediate models: spoilage curves]
      → [dbt marts: spoilage_arbitrage_fact] → [Apache Superset]
      → [Live Dashboard + Slack/Email Alerts]
```

### 1.5 Modules
1. Streaming Ingestion (Kafka + Python simulator)
2. Cloud Warehouse Landing (Snowflake RAW layer)
3. ELT Transformation (dbt staging → intermediate → marts)
4. Spoilage Arbitrage Logic (time-to-spoilage vs. distance-to-market)
5. BI Visualization (Superset dashboards)
6. Alerting (Slack/Email on arbitrage threshold breach)
7. Orchestration & Performance (scheduled dbt runs, clustering/materialized views)

### 1.6 Dependencies
`kafka-python`, `confluent-kafka`, `snowflake-connector-python`, `dbt-snowflake`, `apache-superset`,
`pandas`, `pyyaml`, `python-dotenv`, `requests`, `pytest`, `docker`, `docker-compose`

### 1.7 Deliverables
- Working end-to-end streaming ELT pipeline (Kafka → Snowflake → dbt)
- Superset dashboard showing live container health + arbitrage opportunities
- Automated Slack/Email alerting
- Full documentation, architecture diagram, and test suite
- Clean, reviewed, merged GitHub repository

### 1.8 GitHub Folder Structure (Branch Model)
```
main
├── salih        (architecture, Kafka core, integration, merges)
├── meegadeesh   (Snowflake + dbt data engineering)
├── anusha       (dbt modeling/testing/documentation)
└── member4      (Superset, alerting, Docker/deployment)
```

---

## PART 2 — 4-WEEK MODULE BREAKDOWN

| Week | Focus | Modules Covered |
|---|---|---|
| Week 1 | Ingestion Architecture + BI Foundations | Python IoT simulator, Kafka setup, Snowflake raw tables, Superset deployment & connection |
| Week 2 | ELT Pipeline + Initial Dashboards | dbt core config, staging models, commodity pricing joins, baseline Superset charts |
| Week 3 | Advanced Analytics + Arbitrage UI | Spoilage Arbitrage dbt models, at-risk container dashboard, reroute recommendation logic |
| Week 4 | Automation + Refine & Polish | dbt run orchestration, Snowflake query optimization, Slack/Email alerts, final UI polish |

*(Mid-Project Review falls inside Week 2→3 transition; Final Project Review falls at end of Week 4, matching Infotact SOP.)*

---

## PART 3 — WEEKLY → DAILY BREAKDOWN (Themes)

**Week 1:** D1 Setup & Scaffolding · D2 Simulator Build · D3 Kafka Core · D4 Snowflake Landing · D5 Superset Deploy · D6 End-to-End Ingestion Test · D7 Review & Merge

**Week 2:** D1 dbt Init · D2 Staging Models · D3 Pricing Data Join · D4 Baseline Charts · D5 Data Integrity Checks · D6 Mid-Review Prep · D7 Mid-Review & Merge

**Week 3:** D1 Spoilage Curve Logic · D2 Arbitrage Metric Modeling · D3 At-Risk Container Logic · D4 Arbitrage Dashboard Build · D5 Reroute Recommendation UI · D6 Cross-Testing · D7 Review & Merge

**Week 4:** D1 dbt Orchestration · D2 Snowflake Optimization · D3 Alerting Build · D4 UI Polish · D5 Full Regression Testing · D6 Documentation Finalization · D7 Final Review, Demo & Merge

---

## PART 4 — DAILY TASK DISTRIBUTION

### WEEK 1

| Day | Salih (Lead) | Meegadeesh | Anusha | Member4 |
|---|---|---|---|---|
| 1 | Create GitHub repo, branch structure, initial README | Research Kafka topic design for telemetry | Design project folder structure, requirements.txt | Set up Docker & docker-compose skeleton |
| 2 | Build IoT simulator skeleton (temperature/humidity/vibration generators) | Install & configure local Kafka broker | Define JSON schema for telemetry payload | Write Docker Compose for Kafka + Zookeeper |
| 3 | Add config-driven simulator (config.yaml, container IDs) | Write Kafka producer script streaming simulator output | Set up unit test scaffolding (pytest) | Provision Snowflake trial account & warehouse |
| 4 | Integrate simulator with Kafka producer end-to-end | Write Kafka consumer for raw topic | Draft data validation rules doc | Write Snowflake RAW schema DDL (raw_telemetry table) |
| 5 | Add producer error handling & retry logic | Build Kafka → Snowflake loader script | Set up structured logging across modules | Deploy Apache Superset via Docker |
| 6 | Add environment/config management (.env, secrets handling) | Run & validate end-to-end ingestion (simulator→Kafka→Snowflake) | Write ingestion unit tests | Connect Superset to Snowflake, configure roles |
| 7 | Code review of week's PRs; merge `meegadeesh`,`anusha`,`member4` into `main` | Fix ingestion bugs found in testing | Write Week 1 documentation section | Build Superset connection health-check dashboard, weekly wrap-up |

### WEEK 2

| Day | Salih (Lead) | Meegadeesh | Anusha | Member4 |
|---|---|---|---|---|
| 1 | Initialize dbt project (`dbt_atmosync`), configure Snowflake profile | Design staging model for raw telemetry JSON | Design staging model for mock commodity pricing data | Build baseline Superset chart: raw temperature time series |
| 2 | Review dbt project structure, set model layer conventions | Write `stg_telemetry.sql` staging model | Write `stg_commodity_pricing.sql` staging model | Build baseline chart: container route history |
| 3 | Set up dbt sources.yml & source freshness checks | Clean/parse nested JSON payload fields in staging | Write dbt tests (not_null, unique) on staging models | Build baseline chart: humidity fluctuation |
| 4 | Write intermediate model joining telemetry + container metadata | Join telemetry staging with commodity pricing staging | Document staging model logic in `docs/data_dictionary.md` | Style baseline dashboard layout (grouping, filters) |
| 5 | Review and refactor SQL for readability/performance | Optimize staging model query performance | Add data quality checks (schema tests) | Add container-selector filter to dashboard |
| 6 | Validate dbt models compile & run cleanly (`dbt build`) | Fix any staging model compile errors | Run and validate dbt test suite | Validate Superset renders live Snowflake tables correctly |
| 7 | Mid-Review prep: consolidate demo, merge branches into `main` | Finalize staging layer for Mid Review | Finalize documentation & test report for Mid Review | Finalize baseline dashboards for Mid Review demo |

### WEEK 3

| Day | Salih (Lead) | Meegadeesh | Anusha | Member4 |
|---|---|---|---|---|
| 1 | Define "Spoilage Arbitrage" formula spec (time-to-spoilage vs distance-to-market) | Write intermediate model: `int_spoilage_curve.sql` | Write intermediate model: `int_distance_to_market.sql` | Design Arbitrage UI wireframe in Superset |
| 2 | Review spoilage curve logic against use-case data | Build spoilage degradation rate calculations | Build distance/market lookup logic | Build "At-Risk Containers" chart |
| 3 | Write mart model `fct_spoilage_arbitrage.sql` | Assist with mart model performance tuning | Write dbt tests for arbitrage mart | Build "Recommended Reroute Destination" table view |
| 4 | Review and refactor arbitrage SQL logic for correctness | Add incremental materialization to spoilage models | Validate arbitrage numbers against sample scenarios | Build arbitrage KPI summary cards |
| 5 | Integrate arbitrage mart into Superset dataset layer | Optimize Snowflake queries backing arbitrage mart | Cross-check arbitrage metric edge cases (negative margins) | Wire dashboard filters to arbitrage mart |
| 6 | Run full pipeline regression test (simulator → dashboard) | Fix data issues found in regression test | Update documentation with arbitrage metric definitions | Polish Arbitrage UI styling & color-coding by risk |
| 7 | Review PRs, merge into `main`, prep Week 3 demo | Finalize arbitrage transformation logic | Finalize arbitrage test suite | Finalize Arbitrage UI for demo |

### WEEK 4

| Day | Salih (Lead) | Meegadeesh | Anusha | Member4 |
|---|---|---|---|---|
| 1 | Design dbt run orchestration schedule (cron/Airflow-lite script) | Implement scheduled `dbt run` script | Write orchestration run-log documentation | Draft Slack webhook alert design |
| 2 | Review orchestration script reliability | Add Snowflake clustering keys to large tables | Test orchestration script under failure conditions | Implement Slack alert trigger on arbitrage threshold |
| 3 | Review Snowflake cost/performance tuning | Add materialized views for dashboard-critical marts | Write tests validating clustering doesn't break results | Implement Email alert fallback |
| 4 | Full code review pass across all modules | Benchmark query performance before/after optimization | Update data dictionary with final schema | Final UI polish: layout, labels, tooltips |
| 5 | Run end-to-end regression + performance test | Fix performance regressions | Execute full test suite (unit+integration) | Test alert delivery reliability |
| 6 | Finalize architecture diagram & README | Finalize warehouse optimization documentation | Finalize all documentation sections | Finalize dashboard + alerts for production demo |
| 7 | Final Review: merge all branches, tag release, run demo | Support final demo (data engineering Q&A) | Support final demo (documentation/testing Q&A) | Support final demo (dashboard/alerts walkthrough) |

---

## PART 5 — GIT COMMIT MESSAGES PER MEMBER

### Salih (Team Lead)
```
git commit -m "Initialize repository structure and branch strategy"
git commit -m "Add project README and setup instructions"
git commit -m "Build initial IoT simulator skeleton"
git commit -m "Add config-driven simulator with container ID generation"
git commit -m "Integrate simulator with Kafka producer"
git commit -m "Add producer retry and error-handling logic"
git commit -m "Add environment and secrets configuration"
git commit -m "Merge week 1 branches into main"
git commit -m "Initialize dbt project and Snowflake profile"
git commit -m "Configure dbt source freshness checks"
git commit -m "Add intermediate model joining telemetry and container metadata"
git commit -m "Refactor staging SQL for readability"
git commit -m "Validate dbt build across all models"
git commit -m "Merge mid-review branches into main"
git commit -m "Define spoilage arbitrage formula specification"
git commit -m "Write fct_spoilage_arbitrage mart model"
git commit -m "Refactor arbitrage SQL logic for accuracy"
git commit -m "Integrate arbitrage mart into Superset dataset layer"
git commit -m "Run full pipeline regression test"
git commit -m "Design dbt orchestration run schedule"
git commit -m "Review orchestration reliability and edge cases"
git commit -m "Complete full codebase review pass"
git commit -m "Finalize architecture diagram and documentation"
git commit -m "Tag v1.0 release and merge final branches into main"
```

### Meegadeesh
```
git commit -m "Research Kafka topic design for container telemetry"
git commit -m "Configure local Kafka broker and Zookeeper"
git commit -m "Implement Kafka producer for telemetry stream"
git commit -m "Implement Kafka consumer for raw topic"
git commit -m "Build Kafka to Snowflake loader script"
git commit -m "Validate end-to-end ingestion pipeline"
git commit -m "Fix ingestion bugs found during testing"
git commit -m "Design staging model for raw telemetry JSON"
git commit -m "Implement stg_telemetry dbt model"
git commit -m "Clean and parse nested JSON payload fields"
git commit -m "Join telemetry staging with commodity pricing data"
git commit -m "Optimize staging model query performance"
git commit -m "Fix dbt staging model compile errors"
git commit -m "Write int_spoilage_curve intermediate model"
git commit -m "Build spoilage degradation rate calculations"
git commit -m "Add incremental materialization to spoilage models"
git commit -m "Optimize Snowflake queries backing arbitrage mart"
git commit -m "Finalize arbitrage transformation logic"
git commit -m "Implement scheduled dbt run script"
git commit -m "Add Snowflake clustering keys to large tables"
git commit -m "Add materialized views for dashboard-critical marts"
git commit -m "Benchmark query performance before and after optimization"
git commit -m "Fix performance regressions"
git commit -m "Finalize warehouse optimization documentation"
```

### Anusha
```
git commit -m "Design project folder structure and requirements.txt"
git commit -m "Define JSON schema for telemetry payload"
git commit -m "Set up pytest scaffolding for unit tests"
git commit -m "Draft data validation rules documentation"
git commit -m "Set up structured logging across modules"
git commit -m "Write ingestion unit tests"
git commit -m "Write Week 1 documentation section"
git commit -m "Design staging model for commodity pricing data"
git commit -m "Implement stg_commodity_pricing dbt model"
git commit -m "Add not_null and unique dbt tests to staging models"
git commit -m "Document staging model logic in data dictionary"
git commit -m "Add schema-level data quality checks"
git commit -m "Run and validate dbt test suite"
git commit -m "Finalize documentation and test report for mid review"
git commit -m "Write int_distance_to_market intermediate model"
git commit -m "Write dbt tests for arbitrage mart"
git commit -m "Validate arbitrage numbers against sample scenarios"
git commit -m "Cross-check arbitrage metric edge cases"
git commit -m "Update documentation with arbitrage metric definitions"
git commit -m "Finalize arbitrage test suite"
git commit -m "Write orchestration run-log documentation"
git commit -m "Test orchestration script under failure conditions"
git commit -m "Update data dictionary with final schema"
git commit -m "Finalize all project documentation sections"
```

### Member4
```
git commit -m "Set up Docker and docker-compose skeleton"
git commit -m "Write docker-compose for Kafka and Zookeeper"
git commit -m "Provision Snowflake trial account and warehouse"
git commit -m "Write Snowflake RAW schema DDL"
git commit -m "Deploy Apache Superset via Docker"
git commit -m "Connect Superset to Snowflake and configure roles"
git commit -m "Build Superset connection health-check dashboard"
git commit -m "Build baseline chart for raw temperature time series"
git commit -m "Build baseline chart for container route history"
git commit -m "Build baseline chart for humidity fluctuation"
git commit -m "Style baseline dashboard layout and filters"
git commit -m "Add container-selector filter to dashboard"
git commit -m "Validate Superset renders live Snowflake tables"
git commit -m "Finalize baseline dashboards for mid review"
git commit -m "Design Arbitrage UI wireframe in Superset"
git commit -m "Build At-Risk Containers chart"
git commit -m "Build Recommended Reroute Destination table view"
git commit -m "Build arbitrage KPI summary cards"
git commit -m "Wire dashboard filters to arbitrage mart"
git commit -m "Polish Arbitrage UI styling and risk color-coding"
git commit -m "Draft Slack webhook alert design"
git commit -m "Implement Slack alert trigger on arbitrage threshold"
git commit -m "Implement Email alert fallback"
git commit -m "Finalize dashboard and alerts for production demo"
```

---

## PART 6 — PULL REQUESTS, MERGE SCHEDULE & BRANCH ORDER

### Daily PR Titles (representative pattern, repeated weekly per member)
- `[Salih] Day X: <task summary>`
- `[Meegadeesh] Day X: <task summary>`
- `[Anusha] Day X: <task summary>`
- `[Member4] Day X: <task summary>`

Example Week 1: `[Meegadeesh] Day 2: Add Kafka producer for telemetry stream`, `[Member4] Day 4: Add Snowflake RAW schema DDL`

### Merge Schedule
| Merge Point | Timing | Branches Merged |
|---|---|---|
| Weekly Merge 1 | End of Week 1, Day 7 | meegadeesh → main, anusha → main, member4 → main |
| Weekly Merge 2 (Mid Review) | End of Week 2, Day 7 | all branches → main |
| Weekly Merge 3 | End of Week 3, Day 7 | all branches → main |
| Final Merge (Final Review) | End of Week 4, Day 7 | all branches → main, tag release `v1.0` |

### Branch Merge Order
1. `meegadeesh` (data engineering foundation must land first)
2. `anusha` (transformation/testing depends on staging layer)
3. `member4` (dashboard depends on modeled data)
4. Salih resolves conflicts and performs final merge commit into `main`

---

## PART 7 — REPOSITORY SNAPSHOT AFTER EACH WEEK

**After Week 1**
```
atmosync/
├── simulator/
├── kafka/
├── warehouse/ddl/
├── superset/docker-compose.superset.yml
├── requirements.txt
├── README.md
└── docs/
```

**After Week 2**
```
atmosync/
├── simulator/
├── kafka/
├── warehouse/
├── dbt_atmosync/models/staging/
├── superset/dashboards/ (baseline charts)
├── tests/unit/
├── docs/data_dictionary.md
└── README.md
```

**After Week 3**
```
atmosync/
├── dbt_atmosync/models/staging/
├── dbt_atmosync/models/intermediate/
├── dbt_atmosync/models/marts/ (fct_spoilage_arbitrage.sql)
├── superset/dashboards/ (arbitrage UI, at-risk containers)
├── tests/unit/ + tests/integration/
└── docs/
```

**After Week 4 (Final)**
```
atmosync/
├── simulator/
├── kafka/
├── warehouse/ (ddl, clustering, loader)
├── dbt_atmosync/ (staging, intermediate, marts, tests)
├── superset/ (dashboards, alerts)
├── scripts/orchestration/
├── tests/ (unit, integration)
├── docs/ (architecture.md, setup_guide.md, data_dictionary.md)
├── requirements.txt
└── README.md
```

---

## PART 8 — README UPDATES PER WEEK

**Week 1 README additions:** Project intro, problem statement, tech stack, local setup instructions for simulator + Kafka + Snowflake + Superset.

**Week 2 README additions:** dbt project setup instructions, staging model overview, how to run `dbt build`, baseline dashboard screenshots.

**Week 3 README additions:** Spoilage Arbitrage metric explanation, arbitrage mart schema, Arbitrage UI walkthrough with screenshots.

**Week 4 README additions:** Orchestration/scheduling instructions, performance optimization notes, alerting setup guide, final architecture diagram, installation guide, contributors section.

---

## PART 9 — DOCUMENTATION TASKS PER MEMBER

- **Salih:** Architecture diagram, system design doc, final README consolidation, release notes.
- **Meegadeesh:** Kafka setup guide, Snowflake schema documentation, dbt staging/intermediate model docs.
- **Anusha:** Data dictionary, test coverage report, data validation rules documentation, arbitrage metric glossary.
- **Member4:** Superset setup guide, dashboard user guide, alerting configuration guide, installation/deployment guide.

---

## PART 10 — TESTING TASKS

| Type | Tasks |
|---|---|
| Unit Testing | Simulator output validation, Kafka producer/consumer message format tests, dbt staging model column tests |
| Integration Testing | Simulator → Kafka → Snowflake end-to-end flow, dbt run + Superset refresh integration |
| Pipeline Testing | Full pipeline regression (data freshness, row counts, null checks across layers) |
| Dashboard Testing | Superset chart rendering, filter behavior, alert trigger accuracy |
| Documentation Testing | Setup guide walkthrough validation (fresh-clone test), broken link check, data dictionary accuracy check |

---

## PART 11 — FINAL DELIVERABLES

- Final presentation deck (problem, architecture, demo, results)
- Screenshots of Superset dashboards (baseline + arbitrage UI)
- Architecture diagram (system + data flow)
- Workflow/pipeline diagram (ingestion → warehouse → transform → viz → alert)
- Fully merged GitHub repository (`main` branch, tagged release)
- Complete README with setup instructions
- Installation guide (step-by-step local environment setup)
- Final project report (problem statement, approach, results, learnings)

---

## PART 12 — Notes
Approximately 24 commits per member are listed above (Salih 24, Meegadeesh 24, Anusha 24, Member4 24), spread across 28 working days, all mapped to distinct, non-duplicate, real development tasks that build toward the final AtmoSync deliverable.
