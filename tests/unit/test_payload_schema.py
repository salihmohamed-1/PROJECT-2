import pytest
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from warehouse.loader.snowflake_loader import SnowflakeTelemetryLoader

def test_payload_schema_validation():
    loader = SnowflakeTelemetryLoader()
    
    valid_payload = {
        "event_id": "test-uuid-1234",
        "container_id": "CONT-001",
        "timestamp": "2026-08-12T10:00:00Z",
        "temperature": 4.5,
        "humidity": 75.0,
        "vibration": 0.12,
        "latitude": 13.0827,
        "longitude": 80.2707,
        "commodity": "Fresh Produce"
    }
    
    invalid_payload = {
        "event_id": "test-uuid-1234",
        # Missing container_id and temperature
        "timestamp": "2026-08-12T10:00:00Z"
    }
    
    assert loader.validate_payload(valid_payload) is True
    assert loader.validate_payload(invalid_payload) is False

def test_deduplication():
    loader = SnowflakeTelemetryLoader()
    payload = {
        "event_id": "unique-event-001",
        "container_id": "CONT-002",
        "timestamp": "2026-08-12T10:00:00Z",
        "temperature": 5.0,
        "humidity": 70.0,
        "latitude": 13.0,
        "longitude": 80.0
    }
    
    loader.process_messages([payload, payload])
    assert len(loader.processed_event_ids) == 1
    assert "unique-event-001" in loader.processed_event_ids
