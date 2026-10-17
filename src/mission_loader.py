def parse_mission(raw_line):
    fields = [piece.strip() for piece in raw_line.split(',')]
    if len(fields) != 7:
        return None
    for field in fields[:4]:
        if not field:
            return None
    if not fields[4].isdigit():
        return None
    for field in fields[5:7]:
        if not field.replace('.', '', 1).isdigit():
            return None
    return {
        "mission_id": fields[0],
        "pickup_airport": fields[1],
        "drop_off_airport": fields[2],
        "outbound_date": fields[3],
        "passenger_count": int(fields[4]),
        "total_weight": float(fields[5]),
        "flight_distance_nm": float(fields[6])
    }


def load_intake(file_path):
    good_missions = []
    reject_count = 0

    with open(file_path) as intake_file:
        for line in intake_file:
            if line.startswith('#'):
                continue
            mission = parse_mission(line)
            if mission is not None:
                good_missions.append(mission)
            else:
                reject_count += 1

    return good_missions, reject_count


def parse_pilot(raw_line):
    fields = [piece.strip() for piece in raw_line.split(',')]
    if len(fields) != 6:
        return None
    for field in fields[:1]:
        if not field:
            return None
    if not fields[2].isdigit():
        return None
    for field in fields[3:5]:
        if not field.replace('.', '', 1).isdigit():
            return None
    return {
        "pilot_id": fields[0],
        # home_base is optional — a repositioning pilot may fly from anywhere, so it can be blank
        "home_base": fields[1],
        "seats": int(fields[2]),
        "useful_load": float(fields[3]),
        "aircraft_range_nm": float(fields[4]),
        "available_dates": fields[5],
    }


def load_pilots(file_path):
    good_pilots = []
    reject_count = 0

    with open(file_path) as pilot_file:
        for line in pilot_file:
            if line.startswith('#'):
                continue
            pilot = parse_pilot(line)
            if pilot is not None:
                good_pilots.append(pilot)
            else:
                reject_count += 1

    return good_pilots, reject_count


missions, rejects = load_intake("data/missions.csv")
pilots, pilot_rejects = load_pilots("data/pilots.csv")


def match_missions_to_pilots(missions, pilots):
    matches = []
    rejects = []

    for mission in missions:
        for pilot in pilots:
            available_dates = pilot["available_dates"].split(';')
            if mission["outbound_date"] not in available_dates:
                rejects.append({
                    "mission_id": mission["mission_id"],
                    "pilot_id": pilot["pilot_id"],
                    "reason": "Dates do not match"
                })
                continue
            if mission["passenger_count"] > pilot["seats"]:
                rejects.append({
                    "mission_id": mission["mission_id"],
                    "pilot_id": pilot["pilot_id"],
                    "reason": "Not enough seats"
                })
                continue
            if mission["total_weight"] > pilot["useful_load"]:
                rejects.append({
                    "mission_id": mission["mission_id"],
                    "pilot_id": pilot["pilot_id"],
                    "reason": "Exceeds useful load"
                })
                continue
            if mission["flight_distance_nm"] > pilot["aircraft_range_nm"]:
                rejects.append({
                    "mission_id": mission["mission_id"],
                    "pilot_id": pilot["pilot_id"],
                    "reason": "Exceeds aircraft range"
                })
                continue
            matches.append({
                "mission_id": mission["mission_id"],
                "pilot_id": pilot["pilot_id"]
            })
    return matches, rejects


matches, match_rejects = match_missions_to_pilots(missions, pilots)
print(matches)
print(match_rejects)
