---
title: dGC API Server
reviewers: Dr Marcus Baw
---

# dGC API Server


{% set repository_name="rcpch/digital-growth-charts-server" -%}

[![Github Issues](https://img.shields.io/github/issues/{{ repository_name }})](https://github.com/{{ repository_name }}/issues)
[![Github Stars](https://img.shields.io/github/stars/{{ repository_name }})](https://github.com/{{ repository_name }}/stargazers)
[![Github Forks](https://img.shields.io/github/forks/{{ repository_name }})](https://github.com/{{ repository_name }}/network/members)
[![Github Licence](https://img.shields.io/github/license/{{ repository_name }})](https://github.com/{{repository_name }}/blob/live/LICENSE)

[![Build and deploy Python app to Azure Web App - rcpch-dgc-server-live](https://github.com/rcpch/digital-growth-charts-server/actions/workflows/live-deploy-to-server-on-release.yml/badge.svg)](https://github.com/rcpch/digital-growth-charts-server/actions/workflows/live-deploy-to-server-on-release.yml)

![Uptime](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/rcpch/upptime-rcpch-web-services/master/api/check-get-api-rcpch-ac-uk-without-auth-returns-401/uptime.json)
[![DOI](https://zenodo.org/badge/261587883.svg)](https://zenodo.org/badge/latestdoi/261587883)

:octicons-mark-github-16: [GitHub repository](https://github.com/{{ repository_name }})

:octicons-code-review-24: [Developer Portal](https://dev.rcpch.ac.uk) (Sign up and get API keys here)  

:material-api: [API Gateway BASEURL](https://api.rcpch.ac.uk) (NB: Without API key will always respond with 404)

![api_server_postman](../_assets/_images/api_server_postman.png)

## Getting Started

If you want to integrate the RCPCH Digital Growth Charts API into an application, then start [here](../integrator/getting-started.md)

## API details

The API is written in Python. Mathematical and statistical calculations are made using the [SciPy](https://www.scipy.org/) and [NumPy](https://numpy.org/) libraries. Server middleware used is [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/), with autogeneration of the openAPI3 specification documents using the Marshmallow plugin for Flask.

We use the Microsoft Azure API Management Platform to handle authorization, rate limits and quotas.