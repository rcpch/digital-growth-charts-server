---
title: About the dGC
reviewers: Dr Marcus Baw
---

# About the UK RCPCH Growth Chart API Project

The project team was commissioned by NHS England to produce a 'Minimum Viable Product' API (Application Programming Interface) to generate reliable results for growth data from children 1 year and below. The project team began work in May 2020. In development, the project developers found it was feasible and practical to extend the scope of the MVP to include children of **all** ages.

Further we have been able to develop several demonstration clients showing ease of integration with the API. The calculation functions of the API have been extracted out as a separate Python package

## Scope

Currently the minimum viable product is to provide reliable calculations for all children in the UK for height, weight, body mass index (BMI) and head circumference ('occipitofrontal circumference' - OFC).

In addition to providing standard deviation scores (SDS) and centiles, it will also provide basic guidance for users on how to interpret the information received.

It is envisaged that once established and validated, older age groups will be included, and also other growth references.

It is planned that the API will in future be able to handle measurements over multiple occasions for individual children, with a view to interpreting their growth trajectory, as well as _'thrive lines'_[5][6](#references)
