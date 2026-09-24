# Agent Instructions

This repository provides the HTTP API for the RCPCH Digital Growth Charts. It exposes calculations from `rcpchgrowth`; it does not own the underlying clinical reference data or calculation algorithms.

Read this file before changing anything.

## Read First

- [README.md](README.md) - setup and project overview.
- [tests/regression/README.md](tests/regression/README.md) - API response contract and golden-fixture workflow.
- [compatibility/README.md](compatibility/README.md) - supported React consumer profiles and the local/CI compatibility matrix.
- [pacharanero/house-style](https://github.com/pacharanero/house-style) - adopted cross-repository engineering standards.

## Core Invariants

- Treat status codes, content types, response schemas, and response values as an API contract. Intentional changes require reviewed updates to the goldens under `tests/regression/golden/`.
- An API response change must pass `s/compatibility-test` against every supported immutable Chart Component profile. If the committed component fixtures are affected, run the sibling repository's `s/generate-fixtures` against the updated local server, review and commit the generated fixture changes there, and validate its tests and Storybook build.
- Preserve calculation provenance from `rcpchgrowth` unchanged and keep the API server provenance fields accurate.

## Cross-Repository Impact

This API is the second layer in the product chain: `rcpchgrowth-python` (calculations) → this API (HTTP contract and provenance) → `digital-growth-charts-react-component-library` (plotting) → `digital-growth-charts-react-client` (demo and E2E) → `digital-growth-charts-documentation` (integration, safety and release guidance). Use the [Five-Repository Upgrade Runbook](https://growth.rcpch.ac.uk/developer/five-repository-upgrade-runbook/) whenever a change crosses a repository boundary or affects a public contract.

- If the Python engine changes values, supported ages, boundaries, errors, provenance or exported behavior, test the exact candidate wheel/commit through this server's regression suite and `s/compatibility-test`. Do not update response goldens until the numerical difference is understood and approved.
- If an API response changes, review normalized OpenAPI and real success/error responses. Run compatibility against all supported component profiles; if component fixtures need updating, generate them in the component repository against this server candidate and review its test and Storybook results.
- If the component, demo or published integration guidance changes as a consequence, coordinate the corresponding repository and test the combined versions. Document which repositories are affected and which are not in the upgrade record or PR.
- Test pinned candidate revisions or artifacts, not an assumed local sibling checkout. Confirm what the harness selected and record version/commit identities.

Not every API change needs all five repositories. Record affected and unaffected layers with reasons; a green server-only suite does not establish downstream compatibility.

## Workflow

- `s/up` - build and run the API locally.
- `s/test` - run the full pytest suite against the running container.
- `s/regression-accept` - explicitly regenerate reviewed API goldens after an intentional response change.
- `s/compatibility-test` - run candidate API responses through every supported React component profile.
- `s/pr-check` - run the containerized PR check used by CI.

## Git Workflow

- Use a descriptive branch and pull request; `live` is protected and deploys to Azure when merged.
- Commit and push each validated coherent parcel. Do not force-push or bypass deployment approvals.

## Approval Required

Ask before publishing releases, deleting branches, force-pushing, changing secrets, bypassing branch protection or deployment approvals, or making an externally visible production change.
