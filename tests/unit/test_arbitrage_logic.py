import pytest
import math

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def calculate_net_arbitrage(cargo_value: float, spoilage_loss: float, distance_km: float, freight_rate: float = 45.0) -> float:
    reroute_cost = distance_km * freight_rate
    recovered_value = spoilage_loss * 0.90
    return round(recovered_value - reroute_cost, 2)

def test_haversine_distance_chennai_to_bangalore():
    # Chennai (13.0827, 80.2707) to Bangalore (12.9716, 77.5946)
    dist = haversine_distance(13.0827, 80.2707, 12.9716, 77.5946)
    # Approximate straight-line distance is ~290 km
    assert 270.0 <= dist <= 310.0

def test_net_arbitrage_positive_profit():
    # Cargo ₹500,000, Spoilage loss ₹375,000, Distance 300 km @ ₹45/km = ₹13,500
    # Recovered value = ₹375,000 * 0.90 = ₹337,500
    # Net profit = ₹337,500 - ₹13,500 = ₹324,000
    net_profit = calculate_net_arbitrage(cargo_value=500000.0, spoilage_loss=375000.0, distance_km=300.0)
    assert net_profit == 324000.0

def test_net_arbitrage_negative_profit():
    # Spoilage loss ₹10,000, Distance 1000 km @ ₹45/km = ₹45,000
    # Recovered value = ₹9,000 -> Net profit = ₹9,000 - ₹45,000 = -₹36,000
    net_profit = calculate_net_arbitrage(cargo_value=500000.0, spoilage_loss=10000.0, distance_km=1000.0)
    assert net_profit < 0
