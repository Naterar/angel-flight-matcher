function parseMission(rawLine: string) {
  const fields = rawLine.split(",").map((piece) => piece.trim());

  if (fields.length !== 7) {
    return null;
  }

  for (const field of fields.slice(0, 7)) {
    if (!field) {
      return null;
    }
  }

  if (
    isNaN(Number(fields[4])) ||
    isNaN(Number(fields[5])) ||
    isNaN(Number(fields[6]))
  ) {
    return null;
  }

  return {
    missionId: fields[0],
    pickupAirport: fields[1],
    dropOffAirport: fields[2],
    flightDate: fields[3],
    numPassengers: Number(fields[4]),
    cargoWeight: Number(fields[5]),
    flightDistance: Number(fields[6]),
  };
}

console.log(parseMission("M-001, KSGJ, KJAX, 2026-10-04, 4, 340, 120"));
