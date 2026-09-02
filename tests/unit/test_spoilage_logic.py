import pytest

def calculate_time_to_spoilage(temp: float, safe_max: float, baseline_hours: float, vibration: float = 0.15) -> float:
    temp_dev = max(0.0, temp - safe_max)
    vib_penalty = max(0.0, (vibration - 0.5) * 1.5) if vibration > 0.5 else 0.0
    degradation_multiplier = 1.0 + (temp_dev * 0.45) + vib_penalty
    return max(0.5, baseline_hours / degradation_multiplier)

def test_spoilage_normal_conditions():
    # Fresh produce safe max = 8°C, baseline = 48h
    tts = calculate_time_to_spoilage(temp=5.0, safe_max=8.0, baseline_hours=48.0)
    assert tts == 48.0

def test_spoilage_elevated_temperature():
    # Temp elevated to 12°C (+4°C deviation) -> multiplier = 1 + (4 * 0.45) = 2.8
    # Expected TTS = 48 / 2.8 = 17.14 hours
    tts = calculate_time_to_spoilage(temp=12.0, safe_max=8.0, baseline_hours=48.0)
    assert round(tts, 2) == 17.14
    assert tts < 48.0

def test_spoilage_vibration_spike():
    # Temp normal, vibration spike = 0.9 -> penalty = (0.9-0.5)*1.5 = 0.6 -> multiplier = 1.6
    tts = calculate_time_to_spoilage(temp=5.0, safe_max=8.0, baseline_hours=48.0, vibration=0.9)
    assert round(tts, 2) == 30.0
