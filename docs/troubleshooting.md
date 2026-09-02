# AtmoSync Troubleshooting Guide

## 1. PowerShell Script Execution Policy Errors

**Symptom**: Running `.\venv\Scripts\Activate.ps1` returns `cannot be loaded because running scripts is disabled on this system`.

**Fix**: Set execution policy for current process:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

---

## 2. Kafka Connection Timeout / Refused

**Symptom**: `Failed to connect to Kafka (Attempt 1): NoBrokersAvailable`.

**Fix**:
1. Check Docker status: `docker compose ps`
2. Ensure Kafka container is healthy: `docker compose logs kafka`
3. Restart Kafka stack: `docker compose restart kafka`

---

## 3. Snowflake Connection Failures

**Symptom**: `snowflake.connector.errors.DatabaseError: 250001 (08001): Could not connect to Snowflake`.

**Fix**:
1. Verify `.env` credentials (`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`).
2. If working offline without live Snowflake credentials, the Python loader will automatically execute in Mock Database Mode.

---

## 4. dbt Profile Not Found

**Symptom**: `dbt.exceptions.DbtProfileError: Could not find profile named 'dbt_atmosync'`.

**Fix**:
Ensure your `profiles.yml` is configured or run dbt with `--profiles-dir .`:
```powershell
dbt run --profiles-dir .
```
