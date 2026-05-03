# tests/test_pipeline_debug.py

"""
End-to-end pipeline debug runner.

What this script does:
1. Uploads a CSV file
2. Captures upload_id
3. Polls debug endpoint
4. Prints every pipeline stage live
5. Stops when ingestion completes

Run:
    python tests/test_pipeline_debug.py
"""

import time
from pathlib import Path

import requests


# =========================
# Configuration
# =========================
BASE_URL = "http://localhost:8000"
UPLOAD_URL = f"{BASE_URL}/uploads/csv"
DEBUG_URL = f"{BASE_URL}/debug/uploads"

CSV_FILE_PATH = Path("indian_data.csv")   # change if needed
POLL_INTERVAL_SECONDS = 2
MAX_WAIT_SECONDS = 60


# =========================
# Helpers
# =========================
def upload_csv() -> str:
    """
    Upload CSV file and return upload_id.
    """
    if not CSV_FILE_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE_PATH}")

    with open(CSV_FILE_PATH, "rb") as f:
        files = {"file": (CSV_FILE_PATH.name, f, "text/csv")}
        response = requests.post(UPLOAD_URL, files=files)

    response.raise_for_status()

    payload = response.json()
    upload_id = payload["upload_id"]

    print("=" * 80)
    print("UPLOAD ACCEPTED")
    print("=" * 80)
    print(f"Upload ID : {upload_id}")
    print(f"Status    : {payload['status']}")
    print()

    return upload_id


def fetch_debug_state(upload_id: str) -> dict:
    """
    Fetch current pipeline state from debug endpoint.
    """
    response = requests.get(f"{DEBUG_URL}/{upload_id}")
    response.raise_for_status()
    return response.json()


def print_stage(state: dict) -> None:
    """
    Pretty print current pipeline state.
    """
    upload = state["upload"]
    staging_rows = state["staging_rows"]
    final_rows = state["final_rows"]

    print("=" * 80)
    print(f"UPLOAD ID : {upload['id']}")
    print(f"FILE      : {upload['original_name']}")
    print(f"STATUS    : {upload['status']}")
    print(f"SIZE      : {upload['file_size_bytes']} bytes")
    print(f"CREATED   : {upload['created_at']}")
    print("-" * 80)
    print(f"STAGING ROWS : {len(staging_rows)}")
    for row in staging_rows:
        print(
            f"  [STAGING] id={row['id']} name={row['name']} email={row['email']} age={row['age']}")
    print("-" * 80)
    print(f"FINAL ROWS   : {len(final_rows)}")
    for row in final_rows:
        print(
            f"  [FINAL]   id={row['id']} name={row['name']} email={row['email']} age={row['age']}")
    print("=" * 80)
    print()


def wait_for_completion(upload_id: str) -> None:
    """
    Poll pipeline state until completed or timeout.
    """
    start = time.time()

    while True:
        state = fetch_debug_state(upload_id)
        print_stage(state)

        status = state["upload"]["status"]

        if status == "completed":
            print("PIPELINE COMPLETED SUCCESSFULLY")
            return

        if time.time() - start > MAX_WAIT_SECONDS:
            raise TimeoutError("Pipeline did not complete in time")

        # time.sleep(POLL_INTERVAL_SECONDS)


# =========================
# Main Runner
# =========================
def main() -> None:
    upload_id = upload_csv()
    wait_for_completion(upload_id)


if __name__ == "__main__":
    main()
