# Component compatibility matrix

This local-first matrix proves that responses from the candidate API remain consumable by every supported generation of the React chart component. The API repository owns the profiles, scenarios, runner, and pass/fail decision; GitHub Actions invokes the same `s/compatibility-test` command used by developers.

## Profiles

`profiles.json` pins each supported consumer to an immutable Git revision. `legacy-7.5.2` is the final pre-provenance component boundary. `provenance-v1` is the first supported provenance-aware generation. A profile revision never moves: add a new profile when a materially different consumer generation becomes supported. Review each profile by `reviewAfter`; set `status` to `deprecated` and record the agreed `sunset` date when announcing the end of support, then set it to `retired` only after that date. Supported and deprecated profiles remain in the default matrix; retired profiles do not.

The runner prefers a read-only sibling checkout at `../digital-growth-charts-react-component-library` when it contains the pinned revision. This allows local testing of committed component work before it is pushed. Otherwise it clones the declared GitHub repository, which is the CI path. A newly pinned revision must be available from that remote before the server change lands, or CI will correctly fail because it cannot reproduce the profile.

## Run locally

```sh
# Build and start the candidate API, then run every active profile.
s/compatibility-test

# Run one profile while developing the harness.
s/compatibility-test --profile legacy-7.5.2

# Keep the temporary component checkout in the Docker cache volume.
s/compatibility-test --keep
```

The default command rebuilds the candidate API image so dependency changes cannot accidentally be tested against a stale engine. It leaves an already-running Compose API running and stops an API it started. `s/pr-check` uses `--reuse-api` because it owns that service's lifecycle. Set `COMPATIBILITY_API_BASE_URL`, using a URL reachable from Docker such as `http://host.docker.internal:8000`, to test another API without starting the local service.

Results and the exact candidate responses are written under the gitignored `test-results/compatibility/` directory. Component Git checkouts and npm downloads use the `compatibility-cache` Docker volume.

## What runs

The runner requests 45 deterministic response scenarios covering every supported reference, sex, and measurement method plus preterm, bone-age/event, and duplicate paths. It derives a multiple-method SDS case from those responses. Every profile runs the same injected Jest suite inside its own temporary checkout and must render every response without the production error fallback or unexpected console errors.

The final capability probe deliberately changes one UK-WHO measurement to recognised CDC provenance. The legacy profile must continue rendering it, while the provenance-aware profile must suppress it and display the warning. This ensures each pinned revision actually has the capability its profile declares.

The matrix complements rather than replaces `tests/regression/`: regression goldens protect exact HTTP behaviour over a much broader boundary-focused request set, while this suite protects compatibility at the API-to-component boundary.

## CI

`s/pr-check` starts the candidate API, runs pytest and API regression goldens, then invokes `s/compatibility-test --reuse-api`. The workflow contains no separate matrix definition, so local and CI behaviour cannot drift. Parallel GitHub Actions jobs can be introduced later by invoking `--profile`, without changing the source-of-truth profile registry.
