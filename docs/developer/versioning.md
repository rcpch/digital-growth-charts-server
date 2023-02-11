---
title: Versioning
reviewers: Dr Marcus Baw, Dr Anchit Chandran
---

# Versioning the API Server's code 

We distinguish between:

1. The API version itself
2. The server code which creates API responses

All of this documentation relates to **Version 1** of the RCPCH Digital Growth Charts API.

Server code versions may vary.

## Semantic Versioning

We use [Semantic Versioning (SemVer)](https://semver.org/) to ensure server versions are systematically applied.

## Bump2version

We use  `bump2version` tool to simplify versioning in the `digital-growth-charts-server` and `rcpchgrowth-python` packages.
