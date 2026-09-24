# Chart-coordinate lifecycle

**Status: discussion draft.** This document plans chart-coordinate deduplication, testing, provenance, and optimisation under roadmap R11.

It does **not** authorise:

- a production migration
- clinical acceptance of changed coordinates
- changes to customer billing

## Goals and constraints

- **Keep the chart-coordinate HTTP endpoints.** There are consumers beyond the standard React component.
- **Keep background curves bundled with the React component.** Don't introduce mandatory chart-data API requests, API-key requirements, or additional billable calls for existing React consumers.
- **Treat the Python calculation engine as the single source of truth.** Server and React outputs should be reproducible from it, not maintained as independent numerical copies.
- **Prefer a deployment-local disk cache, regenerated at server startup**, over an external cache service. Benchmark and validate startup cost before finalising this.
- **Remove generated server coordinates from Git only after** preserving the evidence needed to compare historical and freshly generated output.
- **Treat changed curves as a clinical-data review, not a fixture refresh.** Even expected bug fixes need traceable evidence; unexpected discrepancies need investigation.

## Evidence and assumptions

| Observation | Evidence status | Follow-up |
| --- | --- | --- |
| Most API consumers also use the React component; chart-coordinate requests are infrequent but nonzero. | Maintainer report, based on an initial APIM analytics inspection. | Record the observation period, operations, request counts, and distinct integrations privately. Distinguish customer traffic from automated tests where possible. |
| Bundled React coordinates were ~1.5 MB and contributed little to observed demo load time. | Maintainer-reported prior measurement, not a newly reproduced benchmark. | Re-measure compressed transfer, parsed size, startup cost, and bundle caching on representative devices. |
| API requests are billable. | Commercial constraint, supplied by the maintainer. | No design may silently replace bundled coordinates with mandatory billable requests. |
| Server startup generates files only when absent; existing files are never checked against engine identity. | `main.py`, `generate_and_store_chart_data()`. | Replace existence-only reuse with an explicit startup lifecycle. |
| Named-format requests read files; custom-list requests calculate live using the installed engine. | Reference routers, e.g. `routers/ukwho.py`. | Test equivalence where a named format and a custom list represent the same request. |
| React imports bundled coordinate modules rather than fetching the chart-coordinate endpoint at runtime. | Component `src/functions/getDomainsAndData.ts` and chart renderers. | Establish a repeatable generator for those modules. |
| Chart-coordinate and mid-parental-height responses carry no provenance. | `Centile_Data` and `MidParentalHeightResponse` in `schemas/response_schema_classes.py`. | Design and test provenance for these response contracts. |

Don't attribute the historical design to an individual, or assume its original rationale. Source history may explain it, but current measurements and safety evidence should decide the replacement.

## Deduplication boundary

Deduplicate **generation logic, reference selection, and generation parameters** - not necessarily every distributed byte.

A server disk cache and an offline-capable React bundle can legitimately hold the same generated values for different consumers. Both must be reproducible from the same authoritative engine and an explicit generation specification, which should record:

- reference, sex, measurement method
- named format or custom values
- centile/SDS interpretation
- age-grid rules, units, output precision

Don't assume existing React modules map one-to-one to the server's 164 files - inventory specialised SDS datasets and segment transformations first.

React generation should run at build/release time, using a local engine or local server, with no production credentials and no billable requests. Two open decisions:

- Should generated React source modules stay tracked in Git, or become release artifacts? (Shipping the data in the package is a separate decision from storing it in Git.)
- Existing published component versions are already frozen and must be included in any impact assessment.

## Proposed server startup lifecycle

1. Resolve the installed engine version and build identity, and enumerate the supported coordinate-generation matrix. Explicitly exclude unsupported combinations rather than swallowing generation failures.
2. Generate the complete required set into a fresh staging directory on **every** application-instance startup, even when previous files exist. Use a writable runtime location - don't require a writable source checkout.
3. Validate the output: structure, coverage, finite coordinates (or explicitly permitted nulls), age grids, generation metadata. Nulls representing undefined inverse transforms are not generation failures.
4. Publish the complete validated set atomically, and mark the instance ready only afterward. Failed generation must fail startup/readiness visibly - never silently fall back to stale or partial files.
5. Serve the immutable published set for that instance's lifetime. Custom-list requests stay on-demand unless measurement establishes a reason to cache them separately.

Startup here means **application lifecycle initialisation**, not Python module import. Things that need explicit handling:

- multiple workers
- development reload
- parallel Container App replicas
- overlapping deployments

Prefer instance-local storage over a shared mutable volume. After measuring costs and understanding the process model, choose either one coordinated generator per instance, or isolated generation per worker.

Azure startup/readiness probes must allow the measured cold-start budget while still detecting failure. Keep the previous healthy deployment available during rollout. A rollback must restore a coherent code/engine/data combination - not copy old coordinates under new provenance.

### Repository layout

- Track `chart-data/README.md`, explaining the directory, startup generation, metadata, failure behaviour, development workflow, and runtime storage location.
- A tracked README already keeps the directory in Git, so `.gitkeep` is unnecessary.
- Ignore generated contents while explicitly retaining the README and any chosen ignore-control file.
- Don't make these ignore changes until the historical comparison (below) has been captured.

## Historical comparison and clinical review

Before deleting or overwriting stored coordinates:

1. **Preserve an immutable baseline** - identified by Git commit, file checksums, server release, and component release. If the original generator identity can't be established, treat it as unknown; don't retrospectively label old data with the currently installed engine version.
2. **Produce a semantic comparison** of historical server files, fresh engine output, and relevant shipped React datasets. Group differences by reference, sex, measurement, centile/SDS series, and age. Report added/removed segments, point counts, changed age grids, null transitions, units, and absolute/relative value deltas. Compare overlapping ages separately from grid changes - don't conceal a changed grid by silently interpolating it.
3. **Classify each difference** as one of: an evidenced upstream correction, a serialization/precision change, a generation-policy change, or an unexplained discrepancy. Expected corrections (e.g. a recently fixed age-grid boundary) need links to the engine change plus independent reference evidence. Magnitude alone isn't a sufficient severity threshold - even a small discontinuity at a clinically significant boundary may matter.
4. **For material or unexplained discrepancies**, retain a restricted internal report and ask the clinical safety lead to assess affected reference/age groups, historical exposure, affected integrations/component releases, and possible clinical consequences. Use aggregated operational evidence, never patient data. Escalate through the internal incident process where indicated - don't assume low endpoint traffic means low impact, or that every numerical difference proves harm. Public documentation should describe the engineering plan and approved findings, not confidential incident details or personal blame.

Don't accept changed goldens wholesale before this classification and review. If previously deployed output is judged unsafe, rollback may not be an acceptable mitigation - the safety lead must decide the response.

### Phase 1 outcome (historical comparison) - complete

Server `chart-data/` and the React component's bundled coordinates were preserved (Git identity, checksums, working-tree copies), then compared against output freshly generated from the published `rcpchgrowth` 4.6.4 wheel.

Every difference exceeding 0.1 units on either side was individually classified. All were attributed to known, already-agreed changes:

- the deliberate CDC age-2 duplicate-age step (a real background-curve step, not a smoothed transition)
- the WHO 5-year age-grid boundary fix
- the UK-WHO 0.0383 transposition fix

One small residual remains unattributed: React `uk90_child` 0.4th-centile height, ~0.12 cm, ages 11.5-19.9y. This should be identified before that bundle is regenerated, but isn't judged clinically significant on its own.

**Maintainer and this review agree: this is continued optimisation, not a clinical safety incident.**

The restricted evidence, per-point classification, and methodology are kept privately under `.private/chart-coordinate-audit/` (gitignored) rather than in this tracked file.

**Next:** visual review of rendered centile lines in the React component against these same datasets, to see the practical magnitude of change on an actual chart background before any regeneration or acceptance decision. That work continues with the Chart Component agent in the sibling repository.

## Testing strategy

| Layer | Required evidence |
| --- | --- |
| Engine correctness | Independent reference vectors, domain boundaries, valid age grids, supported centile/SDS formats, and intentionally undefined points. Comparing two calls to the same generator proves consistency, not clinical correctness. |
| Startup lifecycle | Empty directory; pre-existing stale data; engine change; interrupted generation; invalid/missing output; unwritable storage; concurrent startup; repeatability; readiness withheld until success. Importing application modules must not generate files. |
| Served coordinates | Named-format responses equal the freshly generated approved set. Equivalent custom lists agree where semantics and rounding match. Cover custom lists explicitly in the regression matrix. |
| API regression | Keep reviewed independent goldens for calculated results. Generate runtime cache data during test-server startup, but don't generate expected goldens from that same run during ordinary tests. Intentional changes go through the explicit acceptance workflow. |
| React dataset generation | Reproduce bundled data from recorded engine identity and generation parameters. Compare semantically with the intended engine output, allowing only documented transformations. |
| Rendering compatibility | Feed candidate coordinate datasets into chart renderers explicitly, including changed grids, null gaps, joins, and SDS modes. Existing compatibility tests supply measurements against bundled curves and don't prove coordinate freshness. |
| Provenance | Assert real generator identity and parameters before normalising volatile metadata for golden comparisons. Retain exact metadata in upgrade/safety evidence. |

Keep the current API regression and supported React profile gates, but add the missing coordinate-specific gates - don't assume the existing matrix already covers them. Review coordinate regeneration and provenance response changes separately where practical.

## Provenance across endpoints

Currently:

- chart-coordinate responses contain only `centile_data` (no provenance)
- mid-parental-height responses also lack provenance
- calculation, bulk-measurement, and fictional-measurement responses already carry measurement provenance

**Goal: traceability for every calculated result, including utilities.**

For cached coordinates, distinguish two kinds of provenance:

- **generation provenance** - the engine identity and generation specification that produced the artifact
- **serving provenance** - the API build that's returning it

For React bundles, retain the original generation identity alongside the component release identity. Never imply that the currently running engine generated an older cached or bundled artifact.

Before implementation, design the exact response schema:

- Reuse established producer identities where appropriate - don't invent a calculation-engine identity for a utility that never calls the engine.
- Inventory every operation and decide where metadata belongs: an envelope, each measurement, a bundle manifest, or response headers.
- Define explicit treatment for error responses and the OpenAPI/health endpoint.
- Avoid recursively embedding the schema in its own provenance, or breaking existing array/error contracts merely to add an envelope.

Adding JSON fields can affect strict consumers, signatures, snapshots, and payload size even when nominally additive. Before shipping: validate OpenAPI/APIM import, supported consumers, and golden normalisation; update documentation; agree release/versioning and communication requirements. Metadata must never reveal credentials, internal infrastructure addresses, or patient data.

## Benchmark plan: `s/benchmark`

A small **opt-in** benchmark suite, not a production load test.

- Default to a local test deployment and synthetic inputs.
- Production execution needs separate explicit authorisation, a request budget, and awareness of billing/rate limits.
- Never commit API keys or patient payloads.

**Coverage** - every operation family and reference, with representative valid, boundary, and validation-error requests: single calculations, bulk calculations at several bounded sizes, named chart formats, custom chart lists, fictional series of several bounded lengths, mid-parental height, and schema retrieval.

Keep these four measurements separate, so disk-cache performance isn't mistaken for engine performance:

- fresh coordinate-generation timing
- whole startup time
- first-request latency
- warm HTTP latency

**Record:**

- warmups, repetitions, serial/concurrent mode
- payload/response size, status counts
- median/p95 latency, throughput where meaningful, sample counts
- engine/API commits, dependency environment
- hardware/container resource limits, worker count
- whether timings include network/APIM overhead
- startup CPU, peak memory, disk size where available

Keep machine-readable results plus a concise human summary. Start with before/after comparisons, not arbitrary CI performance thresholds on noisy shared runners.

Use results to identify bottlenecks and set a startup budget. If full startup generation is too costly, revisit generation granularity or deployment-time precomputation with explicit identity checks - don't silently keep the current existence-only cache.

## Proposed sequence and decision gates

1. Inventory consumers, datasets, generation variants, response shapes, and deployment process/storage constraints. Preserve historical evidence first.
2. Build the opt-in benchmark harness and semantic comparison tooling. Produce a baseline and classify discrepancies with clinical input as needed.
3. Agree startup failure/readiness semantics, the generation matrix, and the metadata contract. Resolve R2's unsupported named format rather than unintentionally enabling it as a side effect.
4. Implement and test startup regeneration, then remove generated server files from Git with the README/ignore rules. Review coordinate golden changes against the comparison report.
5. Make React data generation reproducible while preserving offline bundled curves and the existing no-extra-API-calls behaviour. Validate actual curve rendering, not only measurement compatibility.
6. Extend provenance contracts across coordinate and utility outputs, with explicit compatibility review. Coordinate with R12's reference removal, but keep numerical/schema diffs separate so each has an explainable cause.
7. Roll out through reviewed releases and staged deployment. Record the generation manifest and timings, verify freshness through HTTP, and monitor readiness and endpoint errors. Keep commercial behaviour unchanged.

## Questions for discussion

- What period and customer population should the APIM usage inventory cover, and who owns it?
- What is the acceptable cold-start/readiness budget under current Azure resources and worker configuration?
- Which exact React generation transformations and datasets should become part of the shared generation specification?
- Should React generated modules remain tracked for reviewability, or be produced during release with a manifest and independent fixtures?
- Which provenance fields belong in coordinate/utility JSON versus artifact manifests or headers, and which consumers require compatibility testing?
- Who owns the clinical comparison review and internal incident escalation, and what evidence is needed before releasing changed curves?
- What benchmark corpus, repetitions, and hardware baseline make performance comparisons useful without turning CI into a noisy timing gate?

## Definition of done

This planning document claims none of these as done. Completion requires evidence for:

- freshness
- reviewed numerical changes
- reproducible React bundles
- no added billable calls
- provenance correctness
- startup failure handling
- representative benchmark results
