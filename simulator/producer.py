import json
import time
import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from simulator.iot_simulator import ContainerTelemetrySimulator
from scripts.utils.logger import get_logger

logger = get_logger("kafka_producer")

# Attempt importing kafka-python with graceful fallback
try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logger.warning("kafka-python package not installed or unavailable. Producer will run in dry-run/mock mode.")

class TelemetryKafkaProducer:
    def __init__(self, bootstrap_servers: str = None, topic: str = None):
        load_dotenv()
        self.bootstrap_servers = bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.topic = topic or os.getenv("KAFKA_TOPIC", "container_telemetry")
        self.producer = None

        if KAFKA_AVAILABLE:
            self._connect_with_retry()

    def _connect_with_retry(self, max_retries: int = 5, retry_interval: int = 3):
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Connecting to Kafka broker at {self.bootstrap_servers} (Attempt {attempt}/{max_retries})...")
                self.producer = KafkaProducer(
                    bootstrap_servers=self.bootstrap_servers,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8') if k else None,
                    retries=3,
                    acks='all'
                )
                logger.info("Successfully connected to Kafka producer!")
                return
            except Exception as e:
                logger.error(f"Failed to connect to Kafka (Attempt {attempt}): {e}")
                if attempt < max_retries:
                    time.sleep(retry_interval)
                else:
                    logger.warning("Kafka broker connection failed after maximum retries. Operating in dry-run/mock mode.")

    def send_event(self, event: dict):
        key = event.get("container_id")
        if self.producer:
            try:
                future = self.producer.send(self.topic, key=key, value=event)
                record_metadata = future.get(timeout=10)
                logger.info(f"Published event for {key} to topic {record_metadata.topic} partition [{record_metadata.partition}] offset {record_metadata.offset}")
            except Exception as e:
                logger.error(f"Error publishing message for {key}: {e}")
        else:
            logger.info(f"[MOCK KAFKA PRODUCER] Topic: {self.topic} | Container: {key} | Temp: {event['temperature']}°C | Lat/Lon: ({event['latitude']}, {event['longitude']})")

    def run_continuous(self, interval_seconds: int = 2, max_ticks: int = None):
        simulator = ContainerTelemetrySimulator()
        logger.info(f"Starting continuous telemetry simulation (Interval: {interval_seconds}s)... Press Ctrl+C to stop.")
        ticks = 0

        try:
            while True:
                events = simulator.generate_all_events()
                for event in events:
                    self.send_event(event)
                
                ticks += 1
                if max_ticks and ticks >= max_ticks:
                    logger.info(f"Reached maximum target ticks ({max_ticks}). Stopping producer.")
                    break

                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Shutting down Kafka producer gracefully.")
        finally:
            self.close()

    def close(self):
        if self.producer:
            self.producer.flush()
            self.producer.close()
            logger.info("Kafka producer connection closed.")

if __name__ == "__main__":
    producer = TelemetryKafkaProducer()
    # Run 5 test ticks when invoked directly
    producer.run_continuous(interval_seconds=1, max_ticks=5)
