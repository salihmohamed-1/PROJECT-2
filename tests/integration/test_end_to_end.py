import pytest
import sqlite3
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from simulator.iot_simulator import ContainerTelemetrySimulator

def test_full_pipeline_mock_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create raw table
    cursor.execute("""
    CREATE TABLE raw_telemetry (
        event_id TEXT PRIMARY KEY,
        container_id TEXT,
        event_timestamp TEXT,
        temperature REAL,
        humidity REAL,
        vibration REAL,
        latitude REAL,
        longitude REAL,
        commodity TEXT
    )
    """)

    # 1. Simulate data
    sim = ContainerTelemetrySimulator()
    events = sim.generate_all_events()

    # 2. Ingest data
    for e in events:
        cursor.execute("""
        INSERT INTO raw_telemetry VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            e["event_id"], e["container_id"], e["timestamp"],
            e["temperature"], e["humidity"], e["vibration"],
            e["latitude"], e["longitude"], e["commodity"]
        ))
    conn.commit()

    # 3. Query count
    cursor.execute("SELECT COUNT(*) FROM raw_telemetry")
    count = cursor.fetchone()[0]
    assert count == 20

    # 4. Query temperature drift detection
    cursor.execute("SELECT container_id, temperature FROM raw_telemetry WHERE temperature > 8.0")
    drifted_containers = cursor.fetchall()
    assert isinstance(drifted_containers, list)
