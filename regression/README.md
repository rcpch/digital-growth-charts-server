# API response regression sweep

This is not the pytest suite. `tests/` proves specific fixtures return specific values; it is deliberately narrow and hand-picked. This tool asks a different question: **across a wide sweep of inputs, does anything change when a dependency (chiefly `rcpchgrowth`) is upgraded?**

It exists because the server delegates almost all clinical and numerical behaviour to `rcpchgrowth`, and the existing test suite does not cover enough of the input space to catch every regression a version bump could introduce. It complements, and does not replace, `tests/`. It is not run in CI and does not gate anything by itself; it is a manual pre-upgrade and post-upgrade check.

## How it works

1. `generate_snapshot.py` boots the app in-process with `TestClient`, runs every case in `cases.py` against the live endpoints (`calculation`, `bulk-calculation`, `chart-coordinates`, `fictional-child-data`, `utilities/mid-parental-height`), and writes the full status code and parsed JSON response for each case to a dated snapshot file, along with the installed `rcpchgrowth` version.
2. `compare_snapshots.py` loads two snapshot files and reports every case whose status code or response differs, field by field. A clean diff means nothing at all changed for that case; an empty diff overall means the sweep found no observable difference.

## Using it before a dependency bump

```sh
# 1. Baseline against the currently pinned version.
s/regression-snapshot before-bump.json

# 2. Bump rcpchgrowth in requirements/common-requirements.txt, rebuild the image.

# 3. Snapshot again against the new version.
s/regression-snapshot after-bump.json

# 4. Diff. Anything printed here needs a human decision before merging the bump.
s/regression-diff regression/snapshots/before-bump.json regression/snapshots/after-bump.json
```

## What this does and does not prove

**Does:** catches any change in status code, response shape, or response value across the case matrix in `cases.py`, including the boundary ages the [Rust port spec](https://github.com/rcpch/rcpchgrowth-rust) flags as highest-risk: the 42-week, 2-year, 4-year, and 1856-day reference transitions, and the exact ±8/±15 SD validation limits.

**Does not:** prove correctness. A clean diff means "nothing changed", not "everything is right" - if today's behaviour already contains a defect, this tool will faithfully preserve it across the bump rather than flag it. See `.private/python-defect-triage.md` in `rcpchgrowth-python` for known defects this sweep will not surface.

**Does not:** replace clinical review of an intentional behaviour change. If the dependency bump is expected to change output, for example fixing `chronological_percentage_median_bmi`, the diff for those cases is expected and should be reviewed against the change, not treated as a failure.

## Extending the case matrix

`cases.py` is deliberately data, not code, so cases can be added without touching the runner. See the module docstring for the case shape. Add a case whenever a new boundary, reference, or endpoint combination should be protected against silent drift.
