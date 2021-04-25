---
title: Overview
reviewers: Dr Marcus Baw
---

# Project Overview

-----

<p align="center">
  <a href="https://www.thehtn.co.uk/health-tech-awards-2020-live/">
    <img width="150px" src="../../_assets/htn-awards-winner-202-logo.jpg"
      alt="Best Health Solution 2020 - Health Tech Awards" />
  </a>
</p>
<p align="center">Winner Best Health Tech Solution HTN Health Teach Awards 2020</p>


-----
## The RCPCH Digital Growth Charts (dGC) Project consists of


* a [Digital Growth Charts API Server](../products/api-server.md), which accepts growth data and returns Growth Chart Calculations over REST.
  
* a demonstration client in React.js which shows the main features of the API and serves as 'living documentation' of the standard chart view [growth.rcpch.ac.uk](https://growth.rcpch.ac.uk).

* a [React.js chart component](../products/react-component.md), which is what is used in our React demo client, extracted out into its own library, which can be used as a standalone component in third-party applications to reduce the work involved in displaying a standard chart. It can also be used as a 'template' to help implement charting in another language or framework. (The RCPCH can provide commercial support to aid in the development of charting in other languages and frameworks)
  
* [Clinical Safety documentation](../safety/overview.md) including our complete Clinical Safety Management File for the development (DCB0129) and deployment (DCB0160) of the API and associated clients, libraries and tools, and for implementers to use as an information source for their own clinical safety cases.

* Documentation for the project is primarily here on this documentation site. At present a small amount of further documentation remains at the Azure API Managament Developer Portal at [dev.rcpch.ac.uk](https://dev.rcpch.ac.uk), however we are working to bring all documentation into this site.

* a [Python package](../products/python-library.md) which is the API 'calculation engine' extracted out of the API so that it can be used as a standalone utility in other Python programs, such as in large-scale growth research or academia.

* a [command line utility](../products/command-line-client.md) which wraps the Python package and makes it easy to use the growth calculation functions of the python packages in the command line.