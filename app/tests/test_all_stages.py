# tests/test_all_stages.py

import time
from pathlib import Path

import requests

BASE_URL = "http://localhost:8000"
UPLOAD_URL = f"{BASE_URL}/uploads/csv"
DEBUG_URL = f"{BASE_URL}/debug/uploads"

CSV_FILE_PATH = Path("indian_data.csv")
POLL_INTERVAL_SECONDS = 0.2
MAX_WAIT_SECONDS = 60


def upload_csv() -> str:
    with open(CSV_FILE_PATH, "rb") as f:
        files = {"file": (CSV_FILE_PATH.name, f, "text/csv")}
        response = requests.post(UPLOAD_URL, files=files)

    response.raise_for_status()
    payload = response.json()

    print("=" * 80)
    print("UPLOAD ACCEPTED")
    print("=" * 80)
    print(f"Upload ID : {payload['upload_id']}")
    print(f"Status    : {payload['status']}")
    print()

    return payload["upload_id"]


def fetch_state(upload_id: str) -> dict:
    response = requests.get(f"{DEBUG_URL}/{upload_id}")
    response.raise_for_status()
    return response.json()


def main() -> None:
    upload_id = upload_csv()

    start = time.time()

    while True:
        state = fetch_state(upload_id)

        if state["upload"]["status"] == "completed":
            print("=" * 80)
            print("FULL STAGE HISTORY")
            print("=" * 80)

            for event in state["stage_events"]:
                print(f"{event['created_at']}  ->  {event['stage']}")

            print("=" * 80)
            print(f"FINAL ROWS: {len(state['final_rows'])}")
            print("PIPELINE COMPLETED SUCCESSFULLY")
            return

        if time.time() - start > MAX_WAIT_SECONDS:
            raise TimeoutError("Pipeline did not complete in time")

        # time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
