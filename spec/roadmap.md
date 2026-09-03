# Server roadmap

This roadmap records API contract and delivery improvements identified while implementing provenance and the running-server regression suite in PR #280.

Legend: [x] done, [~] in progress, [ ] not started

## Contract reliability

- [ ] **R1 - Support mathematically undefined extreme-centile chart points** ([GitHub #285](https://github.com/rcpch/digital-growth-charts-server/issues/285))

  The `eighty-five-percent-centiles` chart data contain 43 `null` values for CDC female weight and 25 for Trisomy 21 male BMI. These values are mathematically correct: for those ages, the inverse Box-Cox transform has no real solution at the 99.99th centile. The server currently declares `Data.y` as a non-nullable `float`, so the two chart requests fail response validation and return 500.

  Change `Data.y` to permit `null`, confirm that every supported React compatibility profile renders a line with gaps safely, and regenerate the two static chart assets if necessary. Remove both cases from the regression suite's known-500 allowlist while retaining them in the case matrix. Acceptance requires valid chart responses, focused tests, all 881 regression cases, and all component compatibility profiles to pass.

- [ ] **R2 - Decide the fate of `extended-who-centiles`**

  `schemas/request_validation_classes.py` accepts `extended-who-centiles`, but the repository has no corresponding static chart assets, so every request for the format returns 422. Determine whether integrations use or require it. Either implement it end to end, including the prerequisite `rcpchgrowth` support for `EXTENDED_WHO_CENTILES`, generated assets, contract tests, and component compatibility, or remove it from the accepted request schema and OpenAPI document.

## Deployment assurance

- [~] **R3 - Complete deployed OpenAPI synchronization with APIM** ([GitHub #229](https://github.com/rcpch/digital-growth-charts-server/issues/229))

  PR #281 added serialized, fail-visible APIM synchronization from the reviewed `openapi.json`, and the live API identifier is configured as `growth-charts`. Complete the staged plan in #229: verify a deployment by its `X-Git-Revision`, import the schema served by that exact healthy revision, trial the import away from live, prove operations and policies are preserved, document rollback, and supervise the first live run. Once that path is reliable, remove the redundant committed `openapi.json`, its import-time generation, and its bumpversion entry.

- [ ] **R4 - Monitor public OpenAPI drift independently**

  Add a scheduled check in `digital-growth-charts-upptime` that compares the public APIM contract with the expected deployed API contract and alerts on drift. This complements deployment-time synchronization by detecting later manual or platform-side changes. Keep production credentials out of the monitor and validate the public surface only.

## Completed findings

- [x] **R5 - Raise router HTTP exceptions instead of returning them**

  PR #280 corrected 18 sites across all six reference routers where returning `HTTPException` caused response-model validation to turn intended 422 responses into 500 responses. The parametrized suite covers missing chart assets and calculation-engine failures.

- [x] **R6 - Use the supported WHO adult age for mid-parental height**

  PR #280 replaced hard-coded age 20 lookups with the reference-specific adult age, restoring the documented WHO path for both sexes.

- [x] **R7 - Keep invalid bulk observations inline**

  PR #280 converted an observation date before birth into a per-item error instead of allowing one invalid observation to fail the entire bulk request. Coverage spans all six reference families.

- [x] **R8 - Return a structured Turner validation error**

  PR #280 replaced the bare-string Turner response for unsupported sex or measurement combinations with the intended 422 response.

- [x] **R9 - Make birth-date measurement errors grammatical**

  PR #280 changed extreme-measurement messages from `of Birth date` to `at birth`, added focused high, low, and non-zero-age tests, and updated 74 affected golden responses.

- [x] **R10 - Protect the observable API and consumer boundary in CI**

  PR #280 converted the broad request sweep into an 881-case running-server golden suite, rejects new 5xx and non-JSON responses, validates required provenance, and runs the same candidate responses through the legacy and provenance-aware React profiles. Manual before-and-after snapshots remain available for focused dependency investigations.
