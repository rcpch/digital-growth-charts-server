---
title: Testing the API
reviewers: Dr Marcus Baw
---

# Testing the API

Using the Postman collection runner for tests

Postman, the API creation and testing tool, has a command line version of the tooling called [newman]() which you can run locally from the command line to test a locally-running version of the dGC API against all our standard queries.

At present this checks only for a 200 (OK) response, not the actual content of the response, but we are going to improve this in the near future.

```bash
newman run https://www.getpostman.com/collections/e1ac5fe1fef92761c2ed --env-var "baseUrl=localhost:8000"
```

This command gets the Collection information from our public RCPCH Postman workspace, and runs it against the local server.