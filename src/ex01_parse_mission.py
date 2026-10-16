def parse_mission(raw_line):
    fields = [piece.strip() for piece in raw_line.split(',')]
    if len(fields) != 6:
        return None
    if not fields[4].isdigit():
        return None
    if not fields[5].replace('.', '', 1).isdigit():
        return None
    for field in fields[0:4]:
        if not field:
            return None
    return {
        "mission_id": fields[0],
        "pickup_airport": fields[1],
        "drop_off_airport": fields[2],
        "outbound_date": fields[3],
        "passenger_count": int(fields[4]),
        "total_weight": float(fields[5]),
    }


def load_intake(file_path):
    good_missions = []
    reject_count = 0

    with open(file_path) as intake_file:
        for line in intake_file:
            mission = parse_mission(line)
            if mission is not None:
                good_missions.append(mission)
            else:
                reject_count += 1

    return good_missions, reject_count


missions, rejects = load_intake("data/missions.csv")
print(missions)
print(rejects)
