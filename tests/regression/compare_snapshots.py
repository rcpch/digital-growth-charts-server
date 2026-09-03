"""
Compares two snapshot files produced by `generate_snapshot.py` and reports
every case whose status code or response body differs.

Usage:

    python -m tests.regression.compare_snapshots <before.json> <after.json>

Exit code is 0 if there are no differences, 1 if there are, 2 on usage
error. This makes it usable as a CI-style gate later; today it is a manual
check.
"""

import json
import math
import re
import sys
from pathlib import Path

SNAPSHOT_DIR = Path(__file__).resolve().parent / "snapshots"
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def resolve(path_str: str) -> Path:
    path = Path(path_str)
    if path.exists():
        return path
    candidate = SNAPSHOT_DIR / path_str
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"No such snapshot file: {path_str}")


def diff_value(before, after, path=""):
    """Yield (path, before, after) for every leaf-level difference."""
    if (
        path.endswith(".provenance.api_server.commit")
        and isinstance(before, str)
        and isinstance(after, str)
        and COMMIT_PATTERN.fullmatch(before)
        and COMMIT_PATTERN.fullmatch(after)
    ):
        return
    if isinstance(before, dict) and isinstance(after, dict):
        keys = sorted(set(before) | set(after))
        for key in keys:
            child_path = f"{path}.{key}" if path else key
            if key not in before:
                yield (child_path, "<absent>", after[key])
            elif key not in after:
                yield (child_path, before[key], "<absent>")
            else:
                yield from diff_value(before[key], after[key], child_path)
    elif isinstance(before, list) and isinstance(after, list):
        if len(before) != len(after):
            yield (f"{path}[length]", len(before), len(after))
        for i, (b, a) in enumerate(zip(before, after)):
            yield from diff_value(b, a, f"{path}[{i}]")
    elif (
        isinstance(before, (int, float))
        and not isinstance(before, bool)
        and isinstance(after, (int, float))
        and not isinstance(after, bool)
    ):
        # Last-bit differences vary across CPU/libm implementations and are not
        # observable clinical changes. Keep the tolerance far below API precision.
        if not math.isclose(before, after, rel_tol=1e-12, abs_tol=1e-12):
            yield (path, before, after)
    else:
        if before != after:
            yield (path, before, after)


def main(before_path: str, after_path: str) -> int:
    before = json.loads(resolve(before_path).read_text())
    after = json.loads(resolve(after_path).read_text())

    before_by_id = {r["id"]: r for r in before["results"]}
    after_by_id = {r["id"]: r for r in after["results"]}

    print(f"Before: rcpchgrowth {before['metadata']['dependency_versions']['rcpchgrowth']}"
          f" ({before['metadata']['case_count']} cases, generated {before['metadata']['generated_at']})")
    print(f"After:  rcpchgrowth {after['metadata']['dependency_versions']['rcpchgrowth']}"
          f" ({after['metadata']['case_count']} cases, generated {after['metadata']['generated_at']})")
    print()

    ids_only_before = set(before_by_id) - set(after_by_id)
    ids_only_after = set(after_by_id) - set(before_by_id)
    if ids_only_before:
        print(f"{len(ids_only_before)} case(s) present before but missing after:")
        for cid in sorted(ids_only_before):
            print(f"  - {cid}")
    if ids_only_after:
        print(f"{len(ids_only_after)} case(s) present after but missing before:")
        for cid in sorted(ids_only_after):
            print(f"  + {cid}")

    changed = 0
    for case_id in sorted(set(before_by_id) & set(after_by_id)):
        b = before_by_id[case_id]["response"]
        a = after_by_id[case_id]["response"]
        diffs = list(diff_value(b, a))
        if diffs:
            changed += 1
            print(f"\nCHANGED: {case_id}")
            for field_path, b_val, a_val in diffs:
                print(f"    {field_path}:")
                print(f"      before: {b_val!r}")
                print(f"      after:  {a_val!r}")

    print(f"\n{changed} of {len(set(before_by_id) & set(after_by_id))} shared cases changed.")
    if changed or ids_only_before or ids_only_after:
        return 1
    print("No differences found.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python -m tests.regression.compare_snapshots <before.json> <after.json>",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
