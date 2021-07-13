---
title: About the dGC
reviewers: Dr Marcus Baw
published: true
---

# About the UK RCPCH Growth Chart API Project

## Open Source :material-open-source-initiative:

For transparency, accuracy, and maximum reuse, our Growth Charts API and associated libraries are 100% open source. We welcome code reviews, feedback, issues and pull requests. Check us out on GitHub - we're the first Royal College to have clinical code in it's own GitHub organisation!

## Gold Standard :material-gold:

Working with the UK's top experts in growth monitoring, growth charts, centile and SDS calculation, and child development, we've created an API that takes away the heavy lifting of calculating child growth parameters. You get reliable, safe results instantly.

## Demo clients & tools :material-toolbox:

To help you implement the API we've built demo clients and tools to help with charting. These are all open source and permissively licensed to allow code reuse in your application without affecting the Intellectual Property rights of your developed solution.


## The dGC Story

The RCPCH project team was commissioned by NHSX to produce a 'Minimum Viable Product' API (Application Programming Interface) to generate reliable results for growth data from children 1 year and below. The project team began work in May 2020. In development, the project developers found it was feasible and practical to extend the scope of the MVP to include children of **all** ages, which is what we did. Since then, we have been able to develop several demonstration clients to assist customers with integration with the API. The calculation functions of the API have been extracted out as a separate Python package, to help researchers and those working in Trusted Data Access Environments.

## Current Scope

Currently the "minimum viable product" specification is to provide reliable calculations for children in the UK for height centile, weight centile, body mass index (BMI) centile and head circumference ('occipitofrontal circumference' - OFC) centile.

In addition to providing standard deviation scores (SDS) and centiles, it will also provide basic guidance for users on how to interpret the information received.

## Future Scope

It is envisaged that once established and validated, other growth references and tools may be added.

It is planned that the API will in future be able to handle measurements over multiple occasions for individual children, with a view to interpreting their growth trajectory, as well as _'thrive lines'_[5][6](#references)

!!! info "Get involved in setting our roadmap"
    You can create ['issues' on GitHub](https://github.com/rcpch/digital-growth-charts-server/issues) which can help set the agenda for the features we will develop next in the API.