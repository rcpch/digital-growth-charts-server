# Server roadmap

This roadmap records API contract and delivery improvements identified while implementing provenance and the running-server regression suite in PR #280.

Legend: [x] done, [~] in progress, [ ] not started

## Contract reliability

- [x] **R1 - Support mathematically undefined extreme-centile chart points** ([GitHub #285](https://github.com/rcpch/digital-growth-charts-server/issues/285))

  The `eighty-five-percent-centiles` chart data contain 43 `null` values for CDC female weight and 25 for Trisomy 21 male BMI. These values are mathematically correct: for those ages, the inverse Box-Cox transform has no real solution at the 99.99th centile. The server currently declares `Data.y` as a non-nullable `float`, so the two chart requests fail response validation and return 500.

  Change `Data.y` to permit `null`, confirm that every supported React compatibility profile renders a line with gaps safely, and regenerate the two static chart assets if necessary. Remove both cases from the regression suite's known-500 allowlist while retaining them in the case matrix. Acceptance requires valid chart responses, focused tests, all 881 regression cases, and all component compatibility profiles to pass.

  Completed in PR #290: `Data.y` is nullable, both cases return 200 with null `y` values pinned by a focused contract test, the known-500 allowlist is emptied, and the full regression and compatibility matrices pass.

- [ ] **R2 - Decide the fate of `extended-who-centiles`**

  `schemas/request_validation_classes.py` accepts `extended-who-centiles`, but the repository has no corresponding static chart assets, so every request for the format returns 422. Determine whether integrations use or require it. Either implement it end to end, including the prerequisite `rcpchgrowth` support for `EXTENDED_WHO_CENTILES`, generated assets, contract tests, and component compatibility, or remove it from the accepted request schema and OpenAPI document.

## Deployment assurance

- [~] **R3 - Complete deployed OpenAPI synchronization with APIM** ([GitHub #229](https://github.com/rcpch/digital-growth-charts-server/issues/229))

  PR #281 added serialized, fail-visible APIM synchronization from the reviewed `openapi.json`, and the live API identifier is configured as `growth-charts`. Complete the staged plan in #229: verify a deployment by its `X-Git-Revision`, import the schema served by that exact healthy revision, trial the import away from live, prove operations and policies are preserved, document rollback, and supervise the first live run. Once that path is reliable, remove the redundant committed `openapi.json`, its import-time generation, and its bumpversion entry.

- [ ] **R4 - Monitor public OpenAPI drift independently**

  Add a scheduled check in `digital-growth-charts-upptime` that compares the public APIM contract with the expected deployed API contract and alerts on drift. This complements deployment-time synchronization by detecting later manual or platform-side changes. Keep production credentials out of the monitor and validate the public surface only.

## Chart-data lifecycle

- [ ] **R11 - Replace checked-in generated chart coordinates with an explicit cache strategy**

  The server currently persists generated chart-line coordinates as JSON under `chart-data/`, generates files only when they are absent, and serves existing files instead of recalculating the default centile collections. This makes the files an implicit cache with no invalidation when `rcpchgrowth` changes, as demonstrated by the corrected WHO age step tracked in React component [#224](https://github.com/rcpch/digital-growth-charts-react-component-library/issues/224). The API can calculate these coordinates on demand, while the React component separately bundles them to avoid repeated API calls and tracks dynamic loading in [#99](https://github.com/rcpch/digital-growth-charts-react-component-library/issues/99).

  Inventory why the server-side JSON was introduced and whether measured request cost justifies caching. Prefer on-demand calculation if it is acceptably cheap. If caching is required, make it an explicit runtime or deployment cache keyed and invalidated by calculation-engine identity, reference, centile format, sex, and measurement method rather than source-controlled generated data. Acceptance requires benchmark evidence, removal or documented generation of the checked-in JSON, deterministic tests for cache invalidation and corrected WHO age grids, all API regression cases, and all supported React compatibility profiles to pass.

## Restricted reference removal

- [ ] **R12 - Remove Fenton from every Digital Growth Charts surface**

  Permission to distribute this reference and its source data under the projects' open-source terms is unavailable. Remove it rather than retaining disabled code, empty response structures, fixtures, generated output, publications, ignore rules, or dependencies that contain it. This work must not remove or alter the separately licensed UK-WHO preterm reference.

  Begin in `rcpchgrowth`: remove the reference constants and thresholds, disabled data loader, CDC dispatch and chart branches, tests, `.gitignore` and Binder cleanup rules, roadmap references, and the bundled CDC publication containing its LMS tables. Release the cleaned calculation package before changing downstream repositories.

  Update the server and Chart Component as one reviewed contract migration. Upgrade the server to the cleaned `rcpchgrowth` release; remove the placeholder from CDC chart and mid-parental-height responses; remove the router example; regenerate or delete all affected `chart-data/`, regression goldens, and hand-written fixtures; and validate the intentional response change through the complete regression and compatibility matrices. In the Component, remove the interface property, positional CDC-segment lookup, filtering fallbacks, rendering workaround, test parameters, bundled chart modules, and generated build, Storybook, and cache artifacts. Replace positional assumptions with selection of the remaining named CDC infant and child segments, then publish a cleaned Component release.

  Upgrade the React demo and SMART on FHIR application to the cleaned Component release and rebuild their lockfiles and generated outputs. Re-scan the Node server demo, native client, and other maintained consumers even where the initial audit found no tracked references. In the documentation source, remove the clinician-facing reference claim and retain only this exact explanation in the appropriate developer page: `Fenton is known but excluded because permission/open-source licensing is unavailable.` Rebuild the documentation site and search indexes from the cleaned source.

  Acceptance requires case-insensitive scans of tracked source, repository history-independent build outputs, release packages, installed dependency trees, rendered documentation, and deployed API responses to find no reference name, data, schema key, fixture, or generated artifact except the single approved developer-documentation sentence. Remove the proper-name occurrences from this roadmap item when the work is complete so that the final tracked scan has that one documented exception. Record package versions and cross-repository pull requests as evidence, and require the Python suite, all 881 server regression cases, every supported Component compatibility profile, Component tests and Storybook build, and consumer builds to pass.

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
