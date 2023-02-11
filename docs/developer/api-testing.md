---
title: Testing the API
reviewers: Dr Marcus Baw, Dr Anchit Chandran
---

# Testing the API

## Using the Postman collection runner for tests

**Postman**, the API creation and testing tool, has a command line version of the tooling called [Newman](https://learning.postman.com/docs/running-collections/using-newman-cli/installing-running-newman/). Newman can run locally from the command line to test a locally-running version of the Digital Growth Charts API against all our standard queries.

At present, this only checks for a 200 (OK) response, not the actual content of the response. This will be improved in the near future.

```bash
newman run https://www.getpostman.com/collections/e1ac5fe1fef92761c2ed --env-var "baseUrl=localhost:8000"
```

This command gets the Collection information from our public RCPCH Postman workspace, and runs it against the local server.
