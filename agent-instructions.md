# Agent Instructions

This repository provides the HTTP API for the RCPCH Digital Growth Charts. It exposes calculations from `rcpchgrowth`; it does not own the underlying clinical reference data or calculation algorithms.

Read this file before changing anything.

## Read First

- [README.md](README.md) - setup and project overview.
- [tests/regression/README.md](tests/regression/README.md) - API response contract and golden-fixture workflow.
- [pacharanero/house-style](https://github.com/pacharanero/house-style) - adopted cross-repository engineering standards.

## Core Invariants

- Treat status codes, content types, response schemas, and response values as an API contract. Intentional changes require reviewed updates to the goldens under `tests/regression/golden/`.
- An API response change must also prompt a compatibility check against the Storybook and test fixtures in the sibling Chart Component repository, `../digital-growth-charts-react-component-library`. If affected, run its `scripts/generate-fixtures.mjs` against the updated local server, review and commit the generated fixture changes in that repository, and validate its tests and Storybook build. Do not consider the server response change complete until the Chart Component fixtures are updated or the server PR records why they are unaffected.
- Preserve calculation provenance from `rcpchgrowth` unchanged and keep the API server provenance fields accurate.

## Workflow

- `s/up` - build and run the API locally.
- `s/test` - run the full pytest suite against the running container.
- `s/regression-accept` - explicitly regenerate reviewed API goldens after an intentional response change.
- `s/pr-check` - run the containerized PR check used by CI.

## Git Workflow

- Use a descriptive branch and pull request; `live` is protected and deploys to Azure when merged.
- Commit and push each validated coherent parcel. Do not force-push or bypass deployment approvals.

## Approval Required

Ask before publishing releases, deleting branches, force-pushing, changing secrets, bypassing branch protection or deployment approvals, or making an externally visible production change.
