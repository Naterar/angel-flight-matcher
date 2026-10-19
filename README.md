# Angel Flight Matcher

![tests](https://github.com/Naterar/angel-flight-matcher/actions/workflows/tests.yml/badge.svg)

Matches volunteer medical-transport missions to available pilots, and returns a specific reason for every pilot who can't fly it.

Built on synthetic data. Not affiliated with or endorsed by Angel Flight West.

---

## The problem

Volunteer medical-transport organizations run on coordinators matching patient requests to pilots by hand. A request arrives as an email. Somebody reads it, types it into a spreadsheet, and works down a pilot roster checking four things: enough seats, enough useful load, enough range, and availability on the date.

When nothing fits, the coordinator knows it didn't fit. They don't necessarily know _why_ — whether everyone was range-limited, or it was a date problem, or one pilot was close.

This tool does the matching and keeps the reasons.

## Pipeline

```
Mission request  →  Extract  →  Validate  →  Match  →  Coordinator reviews
 (free text)       (Claude)    (schema)    (constraints)   (human approves)
```

Two paths in — a CSV intake file, or a free-text email extracted by Claude. Both satisfy the same contract before anything downstream sees them.

## What it does

**Parses and validates.** Four guard layers on every row: field count, required fields present, passenger count is a whole number, weight and distance are numeric. A malformed row is rejected and counted; it never reaches the matcher as partial data.

**Matches on four constraints.** Passenger count against seats, total weight against useful load, flight distance against aircraft range, and the mission date against the pilot's availability.

**Explains every rejection.** The output is not a filtered list. Each pilot who can't fly the mission comes back with the constraint that disqualified them.

```
{'mission_id': 'M-001', 'pilot_id': 'AF002', 'reason': 'Exceeds useful load'}
```

**Extracts from free text.** A coordinator email goes to Claude with a schema and a no-inference rule. The response is cleaned, parsed, and validated against the same contract the CSV path uses.

## What it doesn't do

- **No booking, no dispatch, no notification.** It produces a shortlist. A human approves every match.
- **No distance calculation.** Distance comes in with the mission. Deriving it from airport coordinates is a later stage.
- **No date ranges.** Availability is exact-match on a date string. A pilot free on the 4th is not considered for the 5th.
- **No rejection summary.** When all pilots fail the same check, the coordinator reads one line per pilot instead of one line total. Logged in `FINDINGS.md`.

## Running it

```bash
# Match missions against the pilot roster
python3 src/mission_loader.py

# Extract a mission from a free-text request (requires an API key)
python3 src/extract.py

# Run the test suite
pytest
```

The extraction path needs an Anthropic API key in a `.env` file at the repo root:

```
ANTHROPIC_API_KEY=your-key-here
```

`.env` is gitignored. No key is committed.

## Tests

Six tests covering the parser's guard layers and the extraction validator:

| Test                                     | Verifies                                 |
| ---------------------------------------- | ---------------------------------------- |
| `good_row`                               | valid input parses                       |
| `short_row_returns_none`                 | field-count guard                        |
| `empty_airport_returns_none`             | required-field guard                     |
| `non_numeric_passengers_returns_none`    | numeric guard                            |
| `converts_types`                         | `int` and `float` conversion             |
| `validate_extraction_rejects_null_field` | LLM output with a null field is rejected |

One broken thing per test, so a pass identifies which guard caught it.

The extraction function is not tested against the live API. Model output is non-deterministic — what gets tested is the cleaning, the parsing, and the validation, all of which are deterministic.

## Notes on working with the model

The prompt instructs Claude explicitly to return raw JSON with no markdown code fences. It wrapped the output in fences anyway. Extraction was otherwise correct: seven fields, uppercase ICAO codes, and a `null` date because the source email said "nov 12" without a year.

The fences are stripped in code rather than argued with in the prompt. Prompt instructions are requests; code is a guarantee.

Findings and open defects are logged in [`FINDINGS.md`](FINDINGS.md).

## Structure

```
angel-flight-matcher/
├── src/
│   ├── mission_loader.py    parsing, loading, matching
│   └── extract.py           LLM extraction and schema validation
├── data/
│   ├── missions.csv         synthetic intake file
│   ├── pilots.csv           synthetic pilot roster
│   └── sample_request.txt   free-text coordinator email
├── tests/
├── FINDINGS.md
└── README.md
```

## Background

Three years volunteering with Angel Flight West, assisting a pilot flying free medical transport, plus fifteen years in naval aviation quality assurance. The rejection-reasons design comes from the QA side: a failed inspection that doesn't say what failed is a failed inspection you can't act on.
