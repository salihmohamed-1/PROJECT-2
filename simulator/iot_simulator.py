import random
import uuid
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

class ContainerTelemetrySimulator:
    """
    Simulates real-time IoT sensor telemetry from refrigerated shipping containers.
    Models micro-climate parameters (temperature, humidity, vibration) and GPS locations.
    """

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.containers = self._initialize_container_states()

    def _initialize_container_states(self) -> Dict[str, Dict[str, Any]]:
        states = {}
        container_ids = self.config["containers"]["ids"]
        commodities = self.config["commodities"]
        routes = self.config["routes"]

        for idx, cid in enumerate(container_ids):
            commodity = commodities[idx % len(commodities)]
            route = routes[idx % len(routes)]
            
            # 25% of containers pre-programmed to experience refrigeration unit failure (drift)
            is_defective = (idx % 4 == 0)

            states[cid] = {
                "container_id": cid,
                "commodity": commodity["name"],
                "temperature_min": commodity["temperature_min"],
                "temperature_max": commodity["temperature_max"],
                "current_temperature": (commodity["temperature_min"] + commodity["temperature_max"]) / 2.0,
                "current_humidity": (commodity["humidity_min"] + commodity["humidity_max"]) / 2.0,
                "current_vibration": self.config["telemetry"]["vibration_base"],
                "origin": route["origin"],
                "destination": route["destination"],
                "start_coords": route["start_coords"],
                "end_coords": route["end_coords"],
                "current_coords": list(route["start_coords"]),
                "is_defective": is_defective,
                "step_count": 0
            }
        return states

    def generate_event(self, container_id: str) -> Dict[str, Any]:
        """Generates a single telemetry payload for the specified container."""
        state = self.containers[container_id]
        state["step_count"] += 1
        
        # Environmental micro-climate drift simulation
        if state["is_defective"]:
            # Defective cooling unit: progressive thermal drift (+0.3°C to +0.8°C per step)
            state["current_temperature"] += round(random.uniform(0.3, 0.8), 2)
            state["current_humidity"] += round(random.uniform(-1.5, 0.5), 2)
        else:
            # Normal operation: slight random jitter around set point
            temp_jitter = random.uniform(-0.2, 0.2)
            state["current_temperature"] = round(state["current_temperature"] + temp_jitter, 2)
            # Bound within safe limits for healthy units
            state["current_temperature"] = max(
                state["temperature_min"] - 0.5,
                min(state["temperature_max"] + 0.5, state["current_temperature"])
            )

        # Humidity limits (0 - 100%)
        humidity_jitter = random.uniform(-0.5, 0.5)
        state["current_humidity"] = max(0.0, min(100.0, round(state["current_humidity"] + humidity_jitter, 2)))

        # Vibration simulation
        vibration = self.config["telemetry"]["vibration_base"] + random.uniform(-0.02, 0.02)
        if random.random() < self.config["telemetry"]["vibration_spike_chance"]:
            vibration += random.uniform(0.4, 1.2)  # Road anomaly / shock event
        state["current_vibration"] = round(vibration, 3)

        # GPS interpolation along route
        progress = min(1.0, state["step_count"] / 100.0)
        start_lat, start_lon = state["start_coords"]
        end_lat, end_lon = state["end_coords"]
        current_lat = round(start_lat + (end_lat - start_lat) * progress + random.uniform(-0.005, 0.005), 6)
        current_lon = round(start_lon + (end_lon - start_lon) * progress + random.uniform(-0.005, 0.005), 6)
        state["current_coords"] = [current_lat, current_lon]

        payload = {
            "event_id": str(uuid.uuid4()),
            "container_id": container_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": state["current_temperature"],
            "humidity": state["current_humidity"],
            "vibration": state["current_vibration"],
            "latitude": current_lat,
            "longitude": current_lon,
            "origin": state["origin"],
            "destination": state["destination"],
            "commodity": state["commodity"]
        }
        return payload

    def generate_all_events(self) -> List[Dict[str, Any]]:
        """Generates telemetry events for all configured containers."""
        return [self.generate_event(cid) for cid in self.containers.keys()]

if __name__ == "__main__":
    simulator = ContainerTelemetrySimulator()
    sample_events = simulator.generate_all_events()
    print(f"Generated {len(sample_events)} telemetry events.")
    print("Sample Event:", sample_events[0])
