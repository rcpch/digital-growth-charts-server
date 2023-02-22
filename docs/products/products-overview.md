---
title: Products Overview
reviewers: Dr Marcus Baw, Dr Anchit Chandran
---

# Products Overview

--8<--
docs/_assets/_snippets/htn-award.md
--8<--

## The RCPCH Digital Growth Charts (dGC) Platform

It's important to understand the architecture of the Digital Growth Charts Platform. It is not built as a single 'app' or product. For important reasons of interoperability and reusability of the code, it is split into functional units:

### [The Digital Growth Charts API Server](../products/api-server.md)

The **RCPCH Digital Growth Charts** (**RCPCH dGC**) platform centres around a 'backend' REST API which provides **calculated growth parameters** derived from **supplied child measurements** such as **height** and **weight**. It accepts growth data in a JSON format and returns Growth Chart Calculations in a JSON format, all over REST. The response from the API contains everything needed to display a graphical Growth Chart, as well as many other parameters which are helpful to clinicians caring for children.

### [The React.js chart component](../products/react-component.md)

This can be thought of as the complementary 'frontend' to the 'backend' server previously mentioned. It is designed as a React.js component library written in Typescript (a superset of Javascript), making it relatively easy to use in third-party applications, significantly reducing the work involved in displaying a standard chart. It can also be used as a 'template' to help implement charting in another programming language or framework.

!!! info "Commercial Support"
    The RCPCH can provide commercial support to aid in the development of charting in other languages and frameworks.

### [The Digital Growth Charts demonstration client](../products/react-client.md)

This demo in React.js shows the main features of the API and serves as 'living documentation' of the standard chart view. It uses both the backend server and the frontend charting library, serving as a reference implementation, which can assist with future implementations.

You can see and test out the charts on our live demo site: [growth.rcpch.ac.uk](https://growth.rcpch.ac.uk).

### [`rcpch-growth` Python package](../products/python-library.md)

This is the API 'calculation engine' extracted out of the API so that it can be used as a standalone utility in other Python programs, such as in large-scale growth research or academia.

### [The Digital Growth Charts command line utility](../products/command-line-client.md)

This is a CLI which wraps the `rcpch-python` package. It makes it easy to use the growth calculation functions of the python packages in the command line.

### [Documentation](/)

All documentation for the project is completely in the open and is primarily here on this documentation site. At present, a small amount of further documentation remains at the Azure API Management Developer Portal at [dev.rcpch.ac.uk](https://dev.rcpch.ac.uk), however we are working to bring all documentation into this site.

### [Clinical Safety documentation](../safety/overview.md)

Including our complete Clinical Safety Management File for the development/manufacture (DCB0129) of the API and associated clients, libraries and tools, and for implementers to use as an information source for their own clinical safety cases.
