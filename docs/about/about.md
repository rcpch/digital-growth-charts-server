---
title: About the dGC
reviewers: Dr Marcus Baw, Dr Anchit Chandran
published: true
---

# About the UK RCPCH Growth Chart API Project

## Open Source :material-open-source-initiative:

For transparency, accuracy, and maximum reuse, our Growth Charts API and associated libraries are 100% open source. We welcome code reviews, feedback, issues and pull requests.

[Check us out on GitHub](https://github.com/rcpch) - we're the first Royal College to have clinical code in its own GitHub organisation!

## Gold Standard :material-gold:

Working with the UK's top experts in growth monitoring, growth charts, centile and SDS calculation, and child development, we've created an API that takes away the heavy lifting of calculating child growth parameters. You get instant reliable and safe results.

The API allows the returned structured data to be displayed in a number of different ways, depending on the clinician's needs. It also allows for the data to be saved, charted, and trended within the EPR.

## Demo clients & tools :material-toolbox:

To help you implement the API, our team has built demo clients and tools to help with the tricky business of displaying a standards-compliant Growth Chart. These tools are all **open source** and **permissively licensed** to allow code reuse in your application without affecting the Intellectual Property rights of your developed solution. For more information on licensing see [Licensing and Copyright](../legal/licensing-copyright.md).

## The dGC Story

The RCPCH project team was commissioned by the NHS to produce a 'Minimum Viable Product' API (Application Programming Interface) to generate reliable results for growth data from children aged 1 year and below. The project team began work in May 2020. In development, the project developers found it was feasible and practical to extend the scope of the MVP to include children of **all** ages. Since then, we have been able to develop several demonstration clients to assist customers with integration with the API. The calculation functions of the API have been extracted out as a separate Python package, to help researchers and those working in Trusted Data Access Environments.

## Current Scope

Currently, the specification is to provide reliable growth calculations for children in the UK for height centile, weight centile, body mass index (BMI) centile and head circumference (*'OccipitoFrontal Circumference'* or OFC) centile.

To this base specification, we added bone age, along with Turner and Down syndrome charts.

In addition to providing Standard Deviation Scores (SDS) and centiles, it will also provide basic guidance for users on how to interpret the information received.

## Future Scope

We have plans to incorporate other growth references and tools to the platform in the future.

In future work, the API will be able to handle measurements over multiple occasions, for individual children. This is with a view to interpreting their [growth trajectory and *'thrive lines'*](../developer/rcpchgrowth.md#other-functions).

!!! info "Get involved in setting our roadmap"
    You can create ['issues' on GitHub](https://github.com/rcpch/digital-growth-charts-server/issues) which can help set the agenda for the features we will develop next in the API.
