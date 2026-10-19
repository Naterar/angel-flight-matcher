from src.extract import validate_extraction
import sys


def test_validate_extraction_rejects_null_field():
    mission = {"mission_id": "AF-1", "pickup_airport": None, "drop_off_airport": "KJAX",
               "outbound_date": "2026-10-04", "passenger_count": 4, "total_weight": 340, "flight_distance_nm": 120}
    assert validate_extraction(mission) is None
