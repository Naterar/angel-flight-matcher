from src.mission_loader import parse_mission
import sys


def test_parse_mission_good_row():
    result = parse_mission("M-001,KSGJ,KJAX,2026-10-04,4,340,120")
    assert result["pickup_airport"] == "KSGJ"


def test_parse_mission_short_row_returns_none():
    result = parse_mission("M-001,KSGJ,KJAX,2026-10-04,4,340")
    assert result is None


def test_parse_mission_empty_airport_returns_none():
    result = parse_mission("M-001,,KJAX,2026-10-04,4,340,120")
    assert result is None


def test_parse_mission_non_numeric_passengers_returns_none():
    result = parse_mission("M-001,KSGJ,KJAX,2026-10-04,four,340,120")
    assert result is None


def test_parse_mission_converts_types():
    result = parse_mission("M-001,KSGJ,KJAX,2026-10-04,4,340,120")
    assert isinstance(result["passenger_count"], int)
    assert isinstance(result["total_weight"], float)
    assert isinstance(result["flight_distance_nm"], float)
