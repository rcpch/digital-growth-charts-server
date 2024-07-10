---
title: Getting Started
reviewers: Dr Marcus Baw, Dr Anchit Chandran, Michael Barton
audience: integrators, implementers, technical-architects
---
# Getting Started integrating Digital Growth Charts

The RCPCH Digital Growth Charts platform centres around a REST API which provides calculated growth parameters derived from supplied child measurements such as height and weight.

The next few pages will take you through the process of using the API. If you are an experienced user of REST APIs, this should be straightforward. We have deliberately designed this API to be simple and clear.

## Sign up for a free tier API key

To use the Digital Growth Charts API, you need to sign up for an account and obtain **API keys**.

These API keys allow us to manage usage of the API and prevent abuse. We have a perpetually free tier of access for testing and exploring the platform.
It has full access to the API but the number of requests are limited.

1. Sign up to our support forum at [https://forum.rcpch.tech/](https://forum.rcpch.tech/)

!!! tip Approval required
    Sign up to the forum is subject to our approval process, please [contact us](../about/contact.md) if you are not approved automatically

1. Navigate to your user summary page using the drop down in the top right hand menu

![forum-user-summary-link](../_assets/_images/forum-user-summary-link.png)

1. Click on the API keys tab

1. Click Generate API key

![forum-user-api-keys](../_assets/_images/forum-user-api-keys.png)

!!! danger "API keys are secrets!"
    API keys identify you to the API, so they should be considered *'secrets'*. If someone else can access and use your API keys, then they **are** effectively 'you' as far as our servers are concerned. Therefore, you must keep your API keys private, especially when using keys in a real application.

    The most common cause of accidental API key exposure is inadvertently committing a hard-coded API key to version control, such as Git, and then pushing it to a public site such as GitHub.

!!! tip Production tiers
    To launch your integration we offer a wide range of paid access tiers that do not have the restrictions of the free tier.
    See our [pricing](https://www.rcpch.ac.uk/resources/growth-charts/digital/about#subscriptions-and-pricing).

-----

## Next: [Making API calls](../integrator/making-api-calls.md)
