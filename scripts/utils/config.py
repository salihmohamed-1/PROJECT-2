import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Snowflake
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "ATMOSYNC")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAW")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "ATMOSYNC_WH")
    SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ATMOSYNC_ROLE")

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "container_telemetry")

    # Alerts
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    ALERT_EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM", "alerts@atmosync.io")
    ALERT_EMAIL_TO = os.getenv("ALERT_EMAIL_TO", "trader-ops@atmosync.io")
    ARBITRAGE_ALERT_THRESHOLD = float(os.getenv("ARBITRAGE_ALERT_THRESHOLD", 35000.0))
