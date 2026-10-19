import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

EXTRACTION_PROMPT = """
You are a flight mission coordination assistant. Extract mission parameters from an unstructured coordinator email into a single valid JSON object.

### Extraction rules

1. Extract values only from the text provided. Do not infer, estimate, or guess.
2. Airport codes: if a four-letter ICAO code appears in the text, extract it in uppercase. If only a city or airport name is given with no code, return null — do not look up or derive the code.
3. Dates: return ISO format (YYYY-MM-DD) only if the year is stated in the text. If no year is given, return null.
4. If any field is missing or ambiguous, set its value to null.
5. Output only the raw JSON object. No markdown code fences, no explanation, no text before or after.

### Schema

{
  "mission_id": string | null,
  "pickup_airport": string | null,
  "drop_off_airport": string | null,
  "outbound_date": string | null,
  "passenger_count": integer | null,
  "total_weight": number | null,
  "flight_distance_nm": number | null
}

### Example

Email:
"Need help moving a patient out of Asheville on March 8, 2027 — KAVL to KCLT, one passenger plus a caregiver, call it 310 pounds with their bag. Short run, about 75 nm."

Output:
{
  "mission_id": null,
  "pickup_airport": "KAVL",
  "drop_off_airport": "KCLT",
  "outbound_date": "2027-03-08",
  "passenger_count": 2,
  "total_weight": 310,
  "flight_distance_nm": 75
}

### Input email

"""


def extract_mission(email_text):
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": EXTRACTION_PROMPT + email_text}]
    )

    raw_output = response.content[0].text

    cleaned = raw_output.strip()
    cleaned = cleaned.removeprefix("```json")
    cleaned = cleaned.removesuffix("```")
    cleaned = cleaned.strip()

    return json.loads(cleaned)


def validate_extraction(mission):
    required_fields = ["mission_id", "pickup_airport", "drop_off_airport", "outbound_date",
                       "passenger_count", "total_weight", "flight_distance_nm"]
    for field in required_fields:
        if field not in mission or mission[field] is None:
            print(f"Missing or invalid field: {field}")
            return None
    return mission


if __name__ == "__main__":
    with open("data/sample_request.txt") as request_file:
        email_text = request_file.read()

    mission = extract_mission(email_text)
    print(mission)

    validated = validate_extraction(mission)
    print(validated)
