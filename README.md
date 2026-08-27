# RCPCH Digital Growth Charts API Server

Please go to <https://growth.rcpch.ac.uk/products/api-server/> for all documentation

Issues can be raised here <https://github.com/rcpch/digital-growth-charts-server/issues>

## Local development

```sh
s/up      # start the server in Docker
s/test    # run the pytest suite
s/down    # stop it
```

## Checking a dependency upgrade before it ships

The pytest suite (`s/test`) proves specific, hand-picked fixtures return specific values. It does not sweep the input space, so a change in the pinned `rcpchgrowth` version could alter server behaviour somewhere the fixtures do not cover, without any test noticing.

`tests/regression/` runs hundreds of requests over HTTP against the running Dockerized server across the reference families, sexes, measurement methods, and clinically significant age boundaries. Every response is compared with a committed golden fixture in each pull request, so an observable API change must be reviewed and accepted deliberately. Dated before-and-after snapshots remain available for dependency investigations.

**Before bumping `rcpchgrowth` in `requirements/`:**

```sh
s/up
s/regression-snapshot before-bump.json
```

**Make the change** - update the pinned version, rebuild the image (`s/rebuild`, or `docker compose build`).

**After the bump:**

```sh
s/regression-snapshot after-bump.json
s/regression-diff before-bump.json after-bump.json
```

The diff prints every case whose status code or response changed, field by field, with the exact before and after value. Exit code `0` means nothing at all changed across the sweep; `1` means something did.

**Reading the result:**

- **No differences** is a strong, but not complete, signal that the upgrade is safe to merge for the cases this sweep covers. It does not prove correctness - if a case in the sweep already returns a wrong value today, an unchanged diff means the upgrade preserved that wrong value, not that it is right.
- **Differences appear** for every case this exercise expects to change. Before merging, check that every reported difference matches what the change was supposed to do, and nothing else. An unexplained difference in a case unrelated to the change is exactly the kind of silent regression this tool exists to catch.

Full detail on what is covered, how to extend the case list, how to accept an intentional response change, and the limits of what a clean run proves: [`tests/regression/README.md`](tests/regression/README.md).
