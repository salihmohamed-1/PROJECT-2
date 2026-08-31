# AtmoSync Windows PowerShell Setup & Execution Guide

This guide provides step-by-step instructions for installing, configuring, and executing the AtmoSync project on **Windows** using **PowerShell** and **VS Code**.

---

## 1. Prerequisites

Ensure the following tools are installed on your machine:
- **Python 3.11+**
- **Docker Desktop** (with WSL2 backend enabled)
- **Git**
- **Snowflake Account** (Optional for cloud execution; offline mock mode supported)

---

## 2. Virtual Environment Setup

Open **Windows PowerShell** in the project directory:

```powershell
# Navigate to workspace
cd D:\PROJECT-2

# If execution policy blocks scripts, enable local script execution for the current session:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Environment Configuration

Copy the example environment file and configure your credentials:

```powershell
Copy-Item .env.example .env
```

Edit `.env` in VS Code to set your Snowflake credentials, Kafka settings, and Slack Webhook URL.

---

## 4. Running Infrastructure (Docker)

Start Kafka, Zookeeper, and Kafka UI:

```powershell
docker compose up -d
```

Verify services are running:
- Kafka UI: http://localhost:8080
- Zookeeper: `localhost:2181`
- Kafka Broker: `localhost:9092`

---

## 5. Running the Pipeline

### Step 5.1: Run IoT Simulator & Kafka Producer
```powershell
python simulator/producer.py
```

### Step 5.2: Run Snowflake Ingestion Loader
```powershell
python warehouse/loader/snowflake_loader.py
```

### Step 5.3: Run dbt Data Modeling
```powershell
cd dbt_atmosync
dbt compile
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..
```

### Step 5.4: Run Master Orchestration Pipeline
```powershell
python scripts/orchestration/run_pipeline.py
```

---

## 6. Running Automated Tests

Execute unit and integration test suites:

```powershell
# Run Unit Tests
python -m pytest tests/unit -v

# Run Integration Tests
python -m pytest tests/integration -v

# Run All Tests
python -m pytest -v
```

---

## 7. Starting Apache Superset BI

Deploy Superset using Docker:

```powershell
docker compose -f superset/docker-compose.superset.yml up -d
```

Access Superset at http://localhost:8088:
- **Username**: `admin`
- **Password**: `admin`
