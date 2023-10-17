---
title: React Chart Component
reviewers: Dr Marcus Baw, Dr Simon Chapman, Dr Anchit Chandran
---

# React Chart Component

{% set repository_name="rcpch/digital-growth-charts-react-component-library" -%}
[:octicons-mark-github-16: GitHub repository](https://github.com/{{ repository_name }})

[:material-web: Online Demo](https://growth.rcpch.ac.uk/)

## Features

* Calculation and display of height, weight, BMI, head circumference, and BMI centiles.
* Support for Trisomy 21 (Down syndrome) and Turner syndrome.
* Automatic gestational age correction, throughout the life course.
* Zoomable, scrollable charts.
* Event logging - clinical events can be associated with measurements.
* Bone age integration.
* Mid-parental heights with mid-parental centile lines (at +2 and -2 SDS).
* SDS (Standard Deviation Score) charts.
* Decimal age support.
* Customisable chart colours.
* Save chart image to clipboard.
* Tooltip information which can be optimised for clinicians or families.
* 'Whole Life Course' toggle to view only measurements or whole chart.

![height-chart-girl-component](../_assets/_images/height-chart-girl-component.png)

## Digital Growth Charts React Client Component Library

In the process of building the API, we realised the difficulty of building a graphically pleasing, clinically accurate growth chart representation, especially for non-clinician developers, who might be unfamiliar with growth charts.

As a simple example, charts typically have 9 main curved centile lines (though there are other formats), each of which can be rendered as a series. However, the UK-WHO chart is made of several growth references, each from different datasets, and it is a stipulation that they must not overlap. This means that for the four datasets which make up UK-WHO, the developer must render 36 separate 'sections' of centile lines, marrying them up correctly, including leaving a 'step' where the datasets change.

Even then, there are certain rules which are key, published by the RCPCH project board. These relate to usability of the charts. For example, the 50th centile should be de-emphasised. These and other rules are listed on the [Client Specification](../integrator/client-specification.md).

Given the complexity, we decided to create a React component library for your developers to use. We designed it to be customisable for direct use, but also as a demonstration for developers wanting to build the charts from the ground up. We do not, however, recommend developing your own growth charts from scratch, as it is a complex task. Using the component library will save you time and effort, and result in a more standardised and clinically-assured product.

The dGC React Chart Component is a permissively-licensed, open-source React component, which aims to simplify the process of creating a chart from the chart data received from the API. It makes the job of drawing a vector-graphic centile chart much easier. **The chart component natively 'understands' an array of the JSON objects returned by the API, without any transforms or parsing required.**

If you want to see an example implementation, we have built a full demo client for the RCPCHGrowth API in React, which uses this component library, and can be found [here](https://github.com/rcpch/digital-growth-charts-react-client). You are welcome to reuse any of the code in this client, or use it as a reference implementation.

## Licensing

This chart component software is is subject to copyright and is owned by the RCPCH, but is released under the MIT license.
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

There is important chart line rendering data bundled in the component, which subject to copyright and is owned by the RCPCH. It is specifically excluded from the MIT license mentioned above. If you wish to use this software, please [contact the RCPCH](../about/contact.md) so we can ensure you have the correct license for use. Subscribers to the Digital Growth Charts API will automatically be assigned licenses for the chart plotting data.
