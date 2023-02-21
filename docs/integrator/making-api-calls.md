---
title: Making API Calls
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# Making calls to the Digital Growth Charts API

There are as many ways to make an API call as there are software developers, but here are some common ways.

We'll start by using `cURL` but if you prefer a graphical tool, then feel free to skip ahead to the Postman section.

!!! tip "API base URL"

    For all API calls to the Growth Charts API, you should use the base URL **`https://api.rcpch.ac.uk/growth/v1`**.

    Our API naming policy is designed to allow the same `api.rcpch.ac.uk` sub-domain for non-growth APIs in the future. We have versioned the API `v1` to allow for future development without interfering with existing integrations.

## cURL

`cURL` is a very simple and common tool for making web requests from the command line (also known as the 'terminal' or 'command prompt'). Official documentation for cURL can be found [here](https://everything.curl.dev).

### Installing cURL

Download cURL [here](https://curl.se/download.html). Scroll to the correction download for your Operating System.

!!! tip "Windows download, install, and usage"

    For Windows, please see [this guide](https://linuxhint.com/install-use-curl-windows/) on how to download and install cURL.

    Use the **Git Bash** command line to save headaches regarding formatting.

### Using cURL to make a test request

Copy and paste the following cURL request into your command line, inserting your `Primary key`:

```bash hl_lines="3"
curl --location --request POST 'https://api.rcpch.ac.uk/growth/v1/uk-who/calculation' \
--header 'Origin: https://growth.rcpch.ac.uk/' \
--header 'Subscription-Key: YOUR_PRIMARY_API_KEY_GOES_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
    "birth_date": "2020-04-12",
    "observation_date": "2028-06-12",
    "observation_value": 115,
    "sex": "female",
    "gestation_weeks": 40,
    "gestation_days": 0,
    "measurement_method": "height",
    "bone_age": 10,
    "bone_age_centile": 98,
    "bone_age_sds": 2.0,
    "bone_age_text": "This bone age is advanced",
    "bone_age_type": "greulich-pyle",
    "events_text": ["Growth hormone start", "Growth Hormone Deficiency diagnosis"]
}'
```

The response should be a large JSON response like the following (truncated):

```bash
{"birth_data":{"birth_date":"2020-04-12", ... :{"events_text":["Growth hormone start","Growth Hormone Deficiency diagnosis"]}}
```

!!! tip "`jq`"
    A neat tool for pretty-printing JSON in the command line is [`jq`](https://stedolan.github.io/jq/download/). With `jq` installed, you can pipe the `cURL` output to `jq` and get a much easier-to-read response:

```bash hl_lines="19"
curl --location --request POST 'https://api.rcpch.ac.uk/growth/v1/uk-who/calculation' \
--header 'Origin: https://growth.rcpch.ac.uk/' \
--header 'Subscription-Key: YOUR_PRIMARY_API_KEY_GOES_HERE' \
--header 'Content-Type: application/json' \
--data-raw '{
    "birth_date": "2020-04-12",
    "observation_date": "2028-06-12",
    "observation_value": 115,
    "sex": "female",
    "gestation_weeks": 40,
    "gestation_days": 0,
    "measurement_method": "height",
    "bone_age": 10,
    "bone_age_centile": 98,
    "bone_age_sds": 2.0,
    "bone_age_text": "This bone age is advanced",
    "bone_age_type": "greulich-pyle",
    "events_text": ["Growth hormone start", "Growth Hormone Deficiency diagnosis"]
}' | jq
```

You should get a nicely formatted JSON response object:

```bash
{
  "birth_data": {
    "birth_date": "2020-04-12",
    "gestation_weeks": 40,
... # truncated
    "events_text": [
        "Growth hormone start",
        "Growth Hormone Deficiency diagnosis"
    ]
  }
}
```



## Using Postman :simple-postman:

Postman is a tool for API development. The RCPCH team used Postman extensively during the API development and testing process.

Download Postman [here](https://learning.postman.com/docs/getting-started/installation-and-updates/).

We have produced a set of Postman Collections and Environments which can help you explore the dGC API.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/202702-d1daf1c6-3a4c-469d-be2a-e2fcf3d84090?action=collection%2Ffork&collection-url=entityId%3D202702-d1daf1c6-3a4c-469d-be2a-e2fcf3d84090%26entityType%3Dcollection%26workspaceId%3Dd868b72e-0677-4b67-9283-112363b1f5ac#?env%5BLIVE%20api.rcpch.ac.uk%5D=W3sia2V5IjoiYmFzZVVybCIsInZhbHVlIjoiaHR0cHM6Ly9hcGkucmNwY2guYWMudWsvZ3Jvd3RoL3YxIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJodHRwczovL2FwaS5yY3BjaC5hYy51ay9ncm93dGgvdjEiLCJzZXNzaW9uSW5kZXgiOjB9LHsia2V5IjoiYXBpS2V5IiwidmFsdWUiOiJJTlNFUlRfWU9VUl9BUElfS0VZX0hFUkUiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoic2VjcmV0Iiwic2Vzc2lvblZhbHVlIjoiSU5TRVJUX1lPVVJfQVBJX0tFWV9IRVJFIiwic2Vzc2lvbkluZGV4IjoxfV0=)

## openAPI3 (Swagger) API documentation :simple-swagger:

As we've specified our API documentation in the openAPI3 (formerly known as 'Swagger') format, we can auto-generate interactive API documentation, which allows you to actually make requests in the documentation site.

The Swagger API reference is [here](api-reference.md).

A similar interface is also embedded in our API Management Platform (the developer portal), where you can try API calls with your keys being automatically added to the request.
