import pytest
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from simulator.iot_simulator import ContainerTelemetrySimulator
from warehouse.loader.snowflake_loader import SnowflakeTelemetryLoader

def test_producer_to_consumer_flow():
    simulator = ContainerTelemetrySimulator()
    loader = SnowflakeTelemetryLoader()

    events = simulator.generate_all_events()
    assert len(events) == 20

    # Process events through loader
    loader.process_messages(events)
    assert len(loader.processed_event_ids) == 20
