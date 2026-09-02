import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.utils.logger import get_logger

logger = get_logger("snowflake_loader")

try:
    import snowflake.connector
    SNOWFLAKE_AVAILABLE = True
except ImportError:
    SNOWFLAKE_AVAILABLE = False
    logger.warning("snowflake-connector-python unavailable. Loader will operate in mock database mode.")

try:
    from kafka import KafkaConsumer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logger.warning("kafka-python unavailable. Consumer will use mock stream generator.")

class SnowflakeTelemetryLoader:
    def __init__(self):
        load_dotenv()
        self.account = os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = os.getenv("SNOWFLAKE_USER")
        self.password = os.getenv("SNOWFLAKE_PASSWORD")
        self.database = os.getenv("SNOWFLAKE_DATABASE", "ATMOSYNC")
        self.schema = os.getenv("SNOWFLAKE_SCHEMA", "RAW")
        self.warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "ATMOSYNC_WH")
        self.role = os.getenv("SNOWFLAKE_ROLE", "ATMOSYNC_ROLE")

        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.topic = os.getenv("KAFKA_TOPIC", "container_telemetry")
        self.group_id = os.getenv("KAFKA_GROUP_ID", "atmosync_loader_group")

        self.processed_event_ids = set()

    def get_snowflake_connection(self):
        if not SNOWFLAKE_AVAILABLE or not self.password or "xy12345" in self.account:
            return None
        try:
            conn = snowflake.connector.connect(
                user=self.user,
                password=self.password,
                account=self.account,
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema,
                role=self.role
            )
            return conn
        except Exception as e:
            logger.error(f"Failed connecting to Snowflake: {e}")
            return None

    def validate_payload(self, event: Dict[str, Any]) -> bool:
        required_fields = ["event_id", "container_id", "timestamp", "temperature", "humidity", "latitude", "longitude"]
        for field in required_fields:
            if field not in event or event[field] is None:
                logger.warning(f"Invalid payload missing required field '{field}': {event}")
                return False
        return True

    def insert_batch_snowflake(self, events: List[Dict[str, Any]]) -> int:
        conn = self.get_snowflake_connection()
        if not conn:
            logger.info(f"[MOCK SNOWFLAKE LOADER] Ingested micro-batch of {len(events)} telemetry records into ATMOSYNC.RAW.RAW_TELEMETRY")
            return len(events)

        insert_sql = """
        INSERT INTO RAW.RAW_TELEMETRY (
            EVENT_ID, CONTAINER_ID, EVENT_TIMESTAMP, TEMPERATURE, HUMIDITY, 
            VIBRATION, LATITUDE, LONGITUDE, ORIGIN, DESTINATION, COMMODITY, RAW_PAYLOAD
        ) SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, PARSE_JSON(%s)
        """

        rows_to_insert = []
        for e in events:
            rows_to_insert.append((
                e["event_id"],
                e["container_id"],
                e["timestamp"],
                e["temperature"],
                e["humidity"],
                e.get("vibration", 0.0),
                e["latitude"],
                e["longitude"],
                e.get("origin", "Unknown"),
                e.get("destination", "Unknown"),
                e.get("commodity", "Unknown"),
                json.dumps(e)
            ))

        cursor = conn.cursor()
        try:
            cursor.executemany(insert_sql, rows_to_insert)
            conn.commit()
            logger.info(f"Successfully committed {len(rows_to_insert)} records to Snowflake RAW.RAW_TELEMETRY.")
            return len(rows_to_insert)
        except Exception as err:
            logger.error(f"Error bulk inserting records into Snowflake: {err}")
            conn.rollback()
            return 0
        finally:
            cursor.close()
            conn.close()

    def process_messages(self, messages: List[Dict[str, Any]]):
        valid_events = []
        for msg in messages:
            event_id = msg.get("event_id")
            if event_id in self.processed_event_ids:
                logger.debug(f"Skipping duplicate event ID: {event_id}")
                continue

            if self.validate_payload(msg):
                valid_events.append(msg)
                self.processed_event_ids.add(event_id)

        if valid_events:
            self.insert_batch_snowflake(valid_events)

    def run_consumer_loop(self, batch_size: int = 10, timeout_seconds: int = 5, max_batches: int = None):
        logger.info("Initializing Snowflake Kafka Loader...")
        if KAFKA_AVAILABLE:
            try:
                consumer = KafkaConsumer(
                    self.topic,
                    bootstrap_servers=self.bootstrap_servers,
                    group_id=self.group_id,
                    auto_offset_reset='earliest',
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    consumer_timeout_ms=timeout_seconds * 1000
                )
                logger.info(f"Subscribed to topic '{self.topic}'. Listening for messages...")

                batch = []
                batch_count = 0
                for message in consumer:
                    batch.append(message.value)
                    if len(batch) >= batch_size:
                        self.process_messages(batch)
                        batch = []
                        batch_count += 1
                        if max_batches and batch_count >= max_batches:
                            break
                if batch:
                    self.process_messages(batch)
                consumer.close()
                return
            except Exception as e:
                logger.warning(f"Kafka consumer connection error: {e}. Falling back to mock processing mode.")

        # Fallback Mock Execution Mode
        from simulator.iot_simulator import ContainerTelemetrySimulator
        sim = ContainerTelemetrySimulator()
        sample_batch = sim.generate_all_events()
        self.process_messages(sample_batch)

if __name__ == "__main__":
    loader = SnowflakeTelemetryLoader()
    loader.run_consumer_loop(batch_size=5, max_batches=2)
