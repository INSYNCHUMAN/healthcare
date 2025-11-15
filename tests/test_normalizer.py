from modules.data_ingest.normalizer import DEFAULT_BOUNDS, normalize_vitals


def test_normalization_produces_expected_values():
    reading = {"heart_rate": 100, "spo2": 98, "respiration": 16, "temperature": 37.2}
    normalized = normalize_vitals(reading)
    assert normalized == {
        "heart_rate": (100 - 40) / (180 - 40),
        "spo2": (98 - 85) / (100 - 85),
        "respiration": (16 - 8) / (32 - 8),
        "temperature": (37.2 - 35) / (40 - 35),
    }


def test_normalization_does_not_mutate_input():
    reading = {"heart_rate": 90, "spo2": 96, "respiration": 15, "temperature": 36.5}
    normalize_vitals(reading)
    assert reading == {"heart_rate": 90, "spo2": 96, "respiration": 15, "temperature": 36.5}


def test_missing_bounds_are_reported():
    reading = {"foo": 1.0}
    try:
        normalize_vitals(reading)
    except KeyError as exc:
        assert "foo" in str(exc)
    else:
        raise AssertionError("KeyError expected for missing metric")


def test_invalid_bounds_raise_value_error():
    bad_bounds = {"heart_rate": (100, 80)}
    try:
        normalize_vitals({"heart_rate": 90}, bounds=bad_bounds)
    except ValueError as exc:
        assert "Upper bound" in str(exc)
    else:
        raise AssertionError("ValueError expected for inverted bounds")
