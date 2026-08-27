"""
Runs every case in `cases.py` against the app in-process and writes a
snapshot file: the exact status code and parsed JSON response for each
case, plus the installed dependency versions, so two snapshots taken
before and after a dependency bump can be diffed by `compare_snapshots.py`.

Usage (inside the container, matching the `tests/` convention):

    python -m regression.generate_snapshot <output-filename>

`<output-filename>` is written under `regression/snapshots/`.
"""

import json
import sys
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app  # noqa: E402
from regression.cases import all_cases  # noqa: E402

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


def run_case(client: TestClient, case: dict) -> dict:
    url = f"{case['prefix']}{case['endpoint']}"
    response = client.post(url, json=case["body"])
    try:
        body = response.json()
    except Exception:
        body = {"__non_json_response__": response.text}
    return {
        "id": case["id"],
        "request": {"url": url, "body": case["body"]},
        "response": {"status_code": response.status_code, "body": body},
    }


def main(output_filename: str) -> None:
    client = TestClient(app, raise_server_exceptions=False)
    cases = all_cases()

    results = [run_case(client, case) for case in cases]

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
        print("Usage: python -m regression.generate_snapshot <output-filename>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
