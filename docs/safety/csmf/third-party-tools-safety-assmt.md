---
title: Third Party Tools Safety
reviewers: Dr Marcus Baw
---

# Third Party Tools Safety

This section documents the steps taken in order to minimise risk incurred from using third party tools in our software stack. Each of the tools is selected 

## List of Third Party Tools

Python 
Flask
statistical libraries ...
validation libraries ...

## Cloud Services Providers

Microsoft Azure
GitHub

## Gravitee.io API Management Platform

Our Digital Growth Charts API uses the open source Gravitee.io API Management Platform to handle API requests to the Digital Growth Charts API. This platform filters requests, and only proxies onward the successful, valid and authorised requests to the backend API.

Gravitee.io is not vulnerable to the Spring4Shell vulnerability (CVE-2022-22965)
<https://community.gravitee.io/t/gravitee-not-impacted-no-action-currently-required-update-on-the-spring4shell-cve-2022-22965-cvss-8-1-vulnerability/380>
