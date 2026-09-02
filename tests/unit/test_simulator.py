import pytest
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from simulator.iot_simulator import ContainerTelemetrySimulator

def test_simulator_initialization():
    sim = ContainerTelemetrySimulator()
    assert len(sim.containers) == 20
    assert "CONT-001" in sim.containers

def test_generate_event_schema():
    sim = ContainerTelemetrySimulator()
    event = sim.generate_event("CONT-001")
    
    assert "event_id" in event
    assert "container_id" in event
    assert event["container_id"] == "CONT-001"
    assert "temperature" in event
    assert "humidity" in event
    assert "latitude" in event
    assert "longitude" in event
    assert isinstance(event["temperature"], (int, float))
    assert isinstance(event["humidity"], (int, float))

def test_temperature_drift_defective_container():
    sim = ContainerTelemetrySimulator()
    # Find defective container
    defective_cid = next(cid for cid, state in sim.containers.items() if state["is_defective"])
    
    initial_temp = sim.containers[defective_cid]["current_temperature"]
    event1 = sim.generate_event(defective_cid)
    event2 = sim.generate_event(defective_cid)
    
    # Defective unit temperature should increase over time
    assert event2["temperature"] > initial_temp
