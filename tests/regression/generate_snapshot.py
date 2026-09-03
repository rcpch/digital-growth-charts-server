"""
Runs every case in `cases.py` against the HTTP API and writes a snapshot
file: the exact status code and parsed JSON response for each case, plus the
installed dependency versions, so snapshots taken before and after a
dependency bump can be diffed by `compare_snapshots.py`.

Usage (inside the container, matching the `tests/` convention):

    python -m tests.regression.generate_snapshot <output-filename>

`<output-filename>` is written under `tests/regression/snapshots/`.
"""

import json
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import httpx

from tests.regression.cases import all_cases
from tests.regression.golden import API_BASE_URL, run_case, wait_for_api

SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"


def _version_or_unknown(package_name: str) -> str:
    """Same fallback as rcpchgrowth's own provenance code (measurement.py):
    a locally symlinked/editable install has no dist-info to read a version
    from, and that is a legitimate state (e.g. testing an unreleased fix
    in-place) rather than an error worth crashing the sweep over."""
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "unknown"


def main(output_filename: str) -> None:
    cases = all_cases()
    with httpx.Client(base_url=API_BASE_URL, timeout=60) as client:
        wait_for_api(client)
        results = [
            {
                "id": case["id"],
                "request": {
                    "url": f"{case['prefix']}{case['endpoint']}",
                    "body": case["body"],
                },
                "response": run_case(client, case),
            }
            for case in cases
        ]

    snapshot = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "case_count": len(results),
            "dependency_versions": {
                "rcpchgrowth": _version_or_unknown("rcpchgrowth"),
                "fastapi": _version_or_unknown("fastapi"),
                "pydantic": _version_or_unknown("pydantic"),
            },
        },
        "results": results,
    }

    SNAPSHOT_DIR.mkdir(exist_ok=True)
    output_path = SNAPSHOT_DIR / output_filename
    output_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True, default=str))

    status_counts: dict[int, int] = {}
    for r in results:
        code = r["response"]["status_code"]
        status_counts[code] = status_counts.get(code, 0) + 1

    print(f"Wrote {len(results)} cases to {output_path}")
    print(f"rcpchgrowth version: {snapshot['metadata']['dependency_versions']['rcpchgrowth']}")
    print("Status code distribution:", dict(sorted(status_counts.items())))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python -m tests.regression.generate_snapshot <output-filename>",
            file=sys.stderr,
        )
        sys.exit(2)
    main(sys.argv[1])
