import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from simulator.iot_simulator import ContainerTelemetrySimulator

def generate_sample_dataset(file_path: str, total_ticks: int = 50):
    sim = ContainerTelemetrySimulator()
    all_events = []

    for tick in range(total_ticks):
        events = sim.generate_all_events()
        all_events.extend(events)

    target_path = Path(file_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(all_events, f, indent=2)

    print(f"Generated {len(all_events)} telemetry events across {len(sim.containers)} containers -> {file_path}")

if __name__ == "__main__":
    out_path = Path(__file__).parent.parent.parent / "data" / "sample_payloads" / "telemetry_sample.json"
    generate_sample_dataset(out_path, total_ticks=55)  # 20 containers * 55 ticks = 1100 events
