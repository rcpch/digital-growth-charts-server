"""Regenerate reviewed API response goldens from the running server."""

import argparse
import shutil
from pathlib import Path

import httpx

from tests.regression.cases import all_cases
from tests.regression.golden import (
    API_BASE_URL,
    GOLDEN_DIR,
    KNOWN_SERVER_ERROR_CASES,
    golden_path,
    run_case,
    wait_for_api,
    write_result,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replace committed goldens with responses from the running API."
    )
    parser.add_argument(
        "--accept",
        action="store_true",
        help="confirm that current API responses should replace the goldens",
    )
    args = parser.parse_args()
    if not args.accept:
        parser.error("refusing to replace goldens without --accept")

    cases = all_cases()
    case_ids = [case["id"] for case in cases]
    if len(case_ids) != len(set(case_ids)):
        raise RuntimeError("Regression case IDs must be unique")

    temporary_dir = Path(f"{GOLDEN_DIR}.tmp")
    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)
    temporary_dir.mkdir()

    status_counts: dict[int, int] = {}
    unexpected_server_errors = []
    unexpected_non_json_responses = []
    try:
        with httpx.Client(base_url=API_BASE_URL, timeout=60) as client:
            wait_for_api(client)
            for case in cases:
                result = run_case(client, case)
                status = result["status_code"]
                status_counts[status] = status_counts.get(status, 0) + 1
                if status >= 500 and case["id"] not in KNOWN_SERVER_ERROR_CASES:
                    unexpected_server_errors.append(case["id"])
                if (
                    "__non_json_response__" in result["body"]
                    and case["id"] not in KNOWN_SERVER_ERROR_CASES
                ):
                    unexpected_non_json_responses.append(case["id"])
                write_result(golden_path(case["id"], temporary_dir), result)

        if unexpected_server_errors:
            joined = "\n  - ".join(unexpected_server_errors)
            raise RuntimeError(f"Refusing to accept new server errors:\n  - {joined}")
        if unexpected_non_json_responses:
            joined = "\n  - ".join(unexpected_non_json_responses)
            raise RuntimeError(f"Refusing to accept non-JSON responses:\n  - {joined}")

        if GOLDEN_DIR.exists():
            shutil.rmtree(GOLDEN_DIR)
        temporary_dir.rename(GOLDEN_DIR)
    except Exception:
        shutil.rmtree(temporary_dir, ignore_errors=True)
        raise

    print(f"Accepted {len(cases)} golden responses from {API_BASE_URL}")
    print("Status code distribution:", dict(sorted(status_counts.items())))
    if KNOWN_SERVER_ERROR_CASES:
        print(f"Known 5xx exceptions are tracked in #285: {len(KNOWN_SERVER_ERROR_CASES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
