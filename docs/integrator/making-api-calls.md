---
title: Making API Calls
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# Making calls to the Digital Growth Charts API

There are as many ways to make an API call as there are software developers, but here are some common ways. We'll start with using our actual API documentation, then try a super-simple tool called `cURL` but if you prefer a graphical tool then feel free to skip ahead to the section on Postman.


## API Base URL

For all API calls to the Growth Charts API, you should use the baseUrl **`https://api.rcpch.ac.uk/growth/v1`**.

> We have namespaced the API to allow us to use the same `api.rcpch.ac.uk` subdomain for other APIs in the future, and we have versioned the API `v1` to allow for future development without interfering with existing integrations.

## Swagger API documentation

Because we've specified our API documentation in the openAPI3 (formerly known as 'Swagger') format, we can auto-generate documentation for our API, but not only that, the documentation is interactive and lets you actually make calls right there in the documentation site, helping you understand the structure of the API.

The Swagger API reference is [here](/digital-growth-charts-documentation/integrator/api-reference/)

A similar interface is also embedded in our API Management Platform (the developer portal), where you can try similar API calls with your API keys automatically added to the request.

## Using cURL

`cURL` is a very simple and common tool for making web calls from the command line (also known as the 'terminal' or 'command prompt'). Official documentation for cURL can be found [here](https://everything.curl.dev).<br/>

Download cURL [here](https://curl.se/download.html).

<!--
```bash

```

What happened here?
-->


## Postman

Postman is a collaboration platform for API development. It simplifies the steps of building an API, allowing developers to create better APIs -faster. Learn more about Postman [here](https://www.postman.com/api-platform/?utm_source=www&utm_medium=home_hero&utm_campaign=button). <br/>
Official documentation can be found [here](https://learning.postman.com/docs/getting-started/introduction/).<br/>

Download Postman [here](https://learning.postman.com/docs/getting-started/installation-and-updates/).
