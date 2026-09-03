# API response regression suite

This suite protects the running server's observable HTTP contract across a broad, boundary-focused matrix of API requests. It complements the narrower hand-written tests in `tests/`: those tests explain specific requirements and defects, while this suite detects any unreviewed change in status, content type, response shape, or response value.

It exists because the server delegates almost all clinical and numerical behaviour to `rcpchgrowth`. A change to the package, schemas, routers, framework, or serialization can otherwise alter API output without a focused test noticing.

## How it works

1. `cases.py` generates stable, human-readable cases for the calculation, bulk-calculation, chart-coordinate, fictional-child, and mid-parental-height endpoints.
2. `test_api_regression.py` sends each case over HTTP to the Uvicorn server running in Docker. Each case is an independent parametrized pytest test.
3. The status code, response content type, and parsed JSON body are compared semantically with the corresponding file under `golden/`.
4. A mismatch prints a bounded field-level diff and writes the complete actual response under the gitignored `test-results/regression/` directory.
5. The complete suite runs in every pull request through the existing `s/pr-check` workflow.

The golden fixture path mirrors the case ID. For example, `calc/uk-who/female/height/term_at_2y` is stored as `golden/calc/uk-who/female/height/term_at_2y.json`.

## Intentional API changes

Normal test runs never update goldens. When an API response must change deliberately:

```sh
# Start the current server if it is not already running.
s/up

# Replace all goldens with responses from that running server.
s/regression-accept

# Review every changed fixture alongside the implementation.
git diff -- tests/regression/golden

# Prove the accepted contract is stable.
s/test tests/regression/test_api_regression.py
```

`s/regression-accept` requires an explicit acceptance flag internally, replaces stale fixtures, and refuses to accept any new 5xx or non-JSON response. Two pre-existing 500 cases are temporarily allowlisted and tracked by [issue #285](https://github.com/rcpch/digital-growth-charts-server/issues/285); their exact current responses remain protected by goldens and no other server errors are permitted. The only build-dependent response value is `provenance.api_server.commit`: comparisons permit one valid 40-character Git commit to replace another, while still requiring the field, its format, and all other provenance values.

Golden changes are evidence of an observable contract change, not proof that the new output is correct. Numerical changes need clinical or reference evidence, and intentional schema/error changes need an explanation in the pull request.

## Before-and-after snapshots

The dated snapshot tools remain available for investigations that need to compare two environments or dependency versions independently of the committed contract. They now use the same real HTTP transport as the CI suite.

## Using it before a dependency bump

```sh
# 1. Baseline against the currently pinned version.
s/regression-snapshot before-bump.json

# 2. Bump rcpchgrowth in requirements/common-requirements.txt, rebuild the image.

# 3. Snapshot again against the new version.
s/regression-snapshot after-bump.json

# 4. Diff. Anything printed here needs a human decision before merging the bump.
s/regression-diff before-bump.json after-bump.json
```

## What this proves

The committed golden suite catches any change in status code, JSON content type, response shape, or response value across the case matrix in `cases.py`, including the boundary ages the [Rust port spec](https://github.com/rcpch/rcpchgrowth-rust) flags as highest-risk: the 42-week, 2-year, 4-year, and 1856-day reference transitions, and the exact ±8/±15 SD validation limits. It also exercises the running ASGI server over TCP rather than invoking the application in-process.

## What this does not prove

A clean run means the running server produced the reviewed contract for every protected case. It does not prove that the reviewed behaviour is clinically correct, cover inputs absent from the matrix, exercise Azure APIM, or replace clinical review of intentional changes. A baseline can preserve a pre-existing defect, which is why known defects require explicit issues and focused correctness tests.

## Extending the case matrix

`cases.py` is deliberately data, not code, so cases can be added without touching the runner. See the module docstring for the case shape. Add a case whenever a new boundary, reference, or endpoint combination should be protected against silent drift.
