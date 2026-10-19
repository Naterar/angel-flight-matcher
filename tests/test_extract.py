from src.extract import validate_extraction


def test_validate_extraction_rejects_null_field():
    mission = {
        "mission_id": "AF-2294",
        "pickup_airport": None,
        "drop_off_airport": "KTPA",
        "outbound_date": "2026-11-12",
        "passenger_count": 2,
        "total_weight": 295,
        "flight_distance_nm": 245,
    }
    assert validate_extraction(mission) is None


def test_validate_extraction_accepts_complete_mission():
    mission = {
        "mission_id": "AF-2294",
        "pickup_airport": "KMCN",
        "drop_off_airport": "KTPA",
        "outbound_date": "2026-11-12",
        "passenger_count": 2,
        "total_weight": 295,
        "flight_distance_nm": 245,
    }
    assert validate_extraction(mission) == mission
