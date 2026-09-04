"""Shared HTTP and fixture helpers for API response regression tests."""

import json
import os
import time
from pathlib import Path

import httpx


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DIR = Path(__file__).resolve().parent / "golden"
FAILURE_DIR = PROJECT_ROOT / "test-results" / "regression"
API_BASE_URL = os.getenv("REGRESSION_BASE_URL", "http://127.0.0.1:8000")

# These existing defects remain protected by exact goldens but do not permit
# any other case to start returning 5xx. Remove each exception when #285 lands.
# Issue #285 is closed: no known server errors remain.
KNOWN_SERVER_ERROR_CASES: set[str] = set()


def golden_path(case_id: str, root: Path = GOLDEN_DIR) -> Path:
    parts = case_id.split("/")
    if not parts or any(not part or part in {".", ".."} for part in parts):
        raise ValueError(f"Invalid regression case ID: {case_id!r}")
    return root.joinpath(*parts).with_suffix(".json")


def wait_for_api(client: httpx.Client, timeout_seconds: float = 60) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error = None
    while time.monotonic() < deadline:
        try:
            response = client.get("/")
            if response.status_code == 200:
                return
            last_error = f"HTTP {response.status_code}"
        except httpx.HTTPError as error:
            last_error = str(error)
        time.sleep(0.25)
    raise RuntimeError(f"API at {client.base_url} was not ready: {last_error}")


def run_case(client: httpx.Client, case: dict) -> dict:
    url = f"{case['prefix']}{case['endpoint']}"
    response = client.request(case["method"], url, json=case["body"])
    try:
        body = response.json()
    except ValueError:
        body = {"__non_json_response__": response.text}
    return {
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", "").partition(";")[0],
        "body": body,
    }


def write_result(path: Path, result: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
