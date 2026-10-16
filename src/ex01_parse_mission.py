def parse_mission(raw_line):
    fields = [piece.strip() for piece in raw_line.split(',')]
    if len(fields) != 6:
        return None
    return {
        "mission_id": fields[0],
        "pickup_airport": fields[1],
        "drop_off_airport": fields[2],
        "outbound_date": fields[3],
        "passenger_count": int(fields[4]),
        "total_weight": float(fields[5]),
    }

### TESTING###
# print(parse_mission("M-001, KSGJ, KJAX, 2026-11-04, 2, 340"))
# print(parse_mission("M-002, KSGJ, KJAX,"))
# print(parse_mission("M-003, , KJAX, 2026-11-04, 2, 340"))
# print(parse_mission("M-004, KSGJ, KJAX, 2026-11-04, two, 340"))
# print(parse_mission(""))
# print(parse_mission("M-005, KSGJ, KJAX, 2026-11-04, 2, abc"))
# print(parse_mission(12345))
# print(parse_mission("M-006, KSGJ, KJAX, 2026-11-04, -2, 340"))
