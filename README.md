<p align="center">
  <a href="https://www.thehtn.co.uk/health-tech-awards-2020-live/"><img width="150px" src="static/htn-awards-winner-202-logo.jpg" alt="Best Health Solution 2020 - Health Tech Awards" /></a>
</p>

<p align="center">
  <img width="200" src="https://github.com/rcpch/digital-growth-charts-server/raw/alpha/static/rcpch-logo.png">
</p>

# RCPCH Digital Growth Charts API Server

An API server and suite of tools which calculates growth centiles and other growth related data for children. This is the basis of the RCPCH Digital Growth Charts API.

API documentation can be found at <dev.rcpch.ac.uk>
A demo client in React can be seen at <growth.rcpch.ac.uk>

This is the main documentation for the project

<!-- TOC -->

- [RCPCH Digital Growth Charts API Server](#rcpch-digital-growth-charts-api-server)
- [About the UK RCPCH Growth Chart API Project](#about-the-uk-rcpch-growth-chart-api-project)
- [API](#api)
  - [API Documentation](#api-documentation)
  - [Postman tooling](#postman-tooling)
- [Demo Clients](#demo-clients)
  - [React/Javascript demo client](#reactjavascript-demo-client)
  - [React Charting Component](#react-charting-component)
  - [Flask/Python demo client (deprecated)](#flaskpython-demo-client-deprecated)
- [Software Licensing](#software-licensing)
- [DISCLAIMER](#disclaimer)
- [RCPCHGrowth Python Package](#rcpchgrowth-python-package)
- [Build Status](#build-status)
- [Date and Age Calculations](#date-and-age-calculations)
  - [Decimal Age](#decimal-age)
  - [Gestational Age / Post-menstrual Age](#gestational-age--post-menstrual-age)
  - [Chronological Decimal Age](#chronological-decimal-age)
  - [Corrected Decimal Age](#corrected-decimal-age)
  - [Scope](#scope)
  - [Copyright and License](#copyright-and-license)
  - [Developer documentation](#developer-documentation)
  - [The dGC Team Members](#the-dgc-team-members)
    - [Project Board](#project-board)
    - [RCPCH Staff](#rcpch-staff)
    - [Development Team](#development-team)
- [Growth Charting Introduction](#growth-charting-introduction)
  - [The LMS Method](#the-lms-method)
    - [How the LMS method is used](#how-the-lms-method-is-used)
  - [Growth References](#growth-references)
- [Privacy](#privacy)
  - [Privacy Policy](#privacy-policy)
  - [Stateless API](#stateless-api)

<!-- /TOC -->

# About the UK RCPCH Growth Chart API Project

The project team was commissioned by NHS England to produce, in the first instance, an MVP (Minimum Viable Product) API (Application Programming Interface) to generate reliable results for growth data from children 1 y and below. The project team began work in May 2020. In development, the project found it was feasible to extend the scope of the MVP to include all children of all ages.

# API

The API is written in Python 3.8. Mathematical and statistical calculations are made using the [SciPy](https://www.scipy.org/) and [NumPy](https://numpy.org/) libraries. [Pandas](https://pandas.pydata.org/) and [Xlrd](https://pypi.org/project/xlrd/) are used for data analysis.

Server middleware used is [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/).

We use the Microsoft Azure API Management Platform to handle authorization, rate limits and quotas.

## API Documentation

All API-related documentation is hosted on our developer portal <https://dev.rcpch.ac.uk/>. For consumers of the API service who want to implement it, this is the best starting point.

## Postman tooling

We have used Postman extensively in the development of the dGC API. We have created Postman collections to help with understanding the API in use. You can use these 'example' API transactions to learn about how the API responds to requests.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/6b1137d60067b8aedfea#?env%5Blocalhost%3A5000-testing%5D=W3sia2V5IjoiYmFzZVVybCIsInZhbHVlIjoibG9jYWxob3N0OjUwMDAiLCJlbmFibGVkIjp0cnVlfV0=)

# Demo Clients

See associated repositories. There are currently two demo clients offered as examples of implementation for users to follow. Please be aware that rendering of charts and reporting of results must adhere to strict guidance to comply with the licensing agreement for use. This advice is published elsewhere in the repository and forms consensus opinion of the UK Growth Chart Reference Group and the Clinical Board.

## React/Javascript demo client

All information about the React demo client can be found at the repository
<https://github.com/rcpch/digital-growth-charts-react-client>

## React Charting Component

A permissively-licensed open-source React component has been created which aims to simplify the process of creating a chart from the chart data received from the API. It makes the job of drawing a vector-graphic centile chart much easier.

https://github.com/rcpch/digital-growth-charts-react-component-library

You can use the component as-is in a React app, or even include it in part of an SPA which uses another type of front-end framework.

If you need us to develop a charting component in a different language or framework, we may be able to do this with you/your company, however there will be some cost to this service and you should be aware that all such RCPCH-developed artefacts will also be open source.

## Flask/Python demo client (deprecated)

All information about the deprecated Flask/Python demo client can be found at the repository
<https://github.com/rcpch/digital-growth-charts-flask-client>

# Software Licensing

The project team agree that the growth references and the algorithms that generate reliable results should all exist in the public domain. They are published here under GNU Affero GPL3 licence.

The code within the dGC API Server which calculates the centiles is eventually going to be released as a separate Python package.

# DISCLAIMER

> **DISCLAIMER: It should be noted that the only version of the dGC API which is warranted to be correct for clinical use is that which is served by the RCPCH itself. While it is _possible_ to use our open source code to set up a server providing dGC API calculations, we specifically and strongly advise _against_ doing this, except for testing, verification, or development purposes. Any version of this API running outside our controlled environment must be independently clinically assured for safety, must be independently technically verified for safe and correct deployment, and must be independently registered as a Medical Device with the MHRA. For NHS use it would also independently need to undergo all relevant DCB0129 and DCB0160 certification with NHS Digital.**

# RCPCHGrowth Python Package

The methods and functions performing the calculations are in the python package RCPCHGrowth. This will be published on PyPi but for the moment is embedded in the Server codebase.

# Build Status

![rcpch-dgc-server-alpha](https://github.com/rcpch/digital-growth-charts-server/workflows/Build%20and%20deploy%20Python%20app%20to%20Azure%20Web%20App%20-%20rcpch-dgc-server-alpha/badge.svg?branch=alpha)

![rcpch-dgc-server-unstable](https://github.com/rcpch/digital-growth-charts-server/workflows/Build%20and%20deploy%20Python%20app%20to%20Azure%20Web%20App%20-%20rcpch-dgc-server-unstable/badge.svg?branch=unstable)

# Date and Age Calculations

## Decimal Age

Decimal ages are expressed as a decimal fraction in years. This is the number of days of life / 365.25. The extra 0.25 is to account for the leap year which comes round every 4 years.

A pregnancy lasts 40 weeks (280 days). This is calculated from the date of the baby's mother's last menstrual period. In fact, from that date, ovulation will occur midway through the following cycle (on average 14 days into a 28 day cycle). This means that from conception, a pregnancy actually lasts only 266 days. Babies are considered to have been born 'Term' if delivered anywhere from 37 to 42 weeks gestation (3 weeks before to 2 weeks after due date).

The due date is referred to as the Estimated Date of Delivery (EDD).

## Gestational Age / Post-menstrual Age

This is the gestation at which the infant was born and represents the number of weeks (and extra days) since last menstrual period.

After delivery, the gestational age of preterm infants it is often tracked by clinicians in addition to chronological age (sometimes referred to at that point as 'corrected gestational age').

## Chronological Decimal Age

This is the time elapsed since birth, in years, irrespective of gestation at birth. A baby born at 24 weeks would be 16 weeks old at 40 weeks gestation (16 x 7)/365.25 y

## Corrected Decimal Age

This is the age of a child that was born preterm calculated from their _due date_, rather than from their actual _birth date_, which would have occurred significantly eariler than their due date. This allows for some comparison between preterm and term babies. This process is referred to as 'Gestational Age Correction' (GAC) and prior to digital growth charts it was a _manual_ process.

Prior to digital growth charts, the convention was that Gestational Age Correction (GAC) would be applied for all babies born before 37 weeks. Above 32 weeks, GAC was applied for 1 year. Below 32 weeks GAC was applied for 2 years.

Now that GAC is automatically applied by the API, the Project Board took the view that it made no sense to have an arbitrary cutoff for GAC and we would apply GAC throughout life. (Of course, the difference between a corrected and uncorrect age becomes less apparent as the child gets older)

A further Project Board decision was made that we would apply GAC for all children, even those born at term, and we would remove the 'averaging' reference which was applied across the genstations 37-42 weeks, instead applying the normal LMS function to these according to corrected age.

## Scope

Currently the minimum viable product is to provide reliable calculations for all children in the UK under the age of 1 year for height, weight, body mass index (BMI) and head circumference ('occipitofrontal circumference' - OFC).

In addition to providing standard deviation scores (SDS) and centiles, it will also provide basic guidance for users on how to interpret the information received.

It is envisaged that once established and validated, older age groups can be included, and other growth references.

It is planned that the API will in future be able to receive longitudinal growth data of individual children as an array, with a view to making some interpretations on their growth pattern and trajectory, as well as _'thrive lines'_[5][6](#references)

## Copyright and License

This work is copyrighted ⓒ2020 The Royal College of Paediatrics and Child Health, and released under the GNU Affero Public License. Our [license file](./LICENSE.md) is included in this repository, with further details available here https://www.gnu.org/licenses/agpl-3.0.en.html

## Developer documentation

If you are reviewing, developing, extending or simply curious about the RCPCH dGC API server, then the developer documentation is here.
[Developer documentation](docs/README.md)

## The dGC Team Members

### Project Board

- Prof Helen Bedford, Professor of Children's Health, University College London, Great Ormond Street Institute of Child Health, London
- Dr Simon Chapman, Consultant in Paediatric Endocrinology, King's College Hospital, London
- Prof Tim Cole, Professor of Medical Statistics, Faculty of Population Health Sciences, UCL GOS Institute of Child Health, London.
- Prof Mary Fewtrell, Professor of Paediatric Nutrition. Population, Policy & Practice Dept. UCL GOS Institute of Child Health, London
- Victoria Jackson, Project Coordinator, Institute of Health Visiting
- Liz Marder, Consultant Paediatrician in Community Child Health and Neurodisability, Nottingham Children's Hospital
- Charlotte Weldon,
- Prof Charlotte Wright, Professor of Community Child Health (Medicine), University of Glasgow

### RCPCH Staff

- Rachel McKeown, Policy Lead & Project Manager, Royal College of Paediatrics and Child Health (RCPCH)
- Jonathan Miall, Director of Membership and Development, Royal College of Paediatrics and Child Health (RCPCH)
- Magdalena Umerska. Digital Platform Commercial Manager, Royal College of Paediatrics and Child Health (RCPCH)

### Development Team

- Dr Marcus Baw, General Hacktitioner, Developer and Informatician, Yorkshire and The Internet.
- Dr Simon Chapman, Consultant in Paediatric Endocrinology, King's College Hospital, London
- Prof. Tim Cole, Professor of Medical Statistics, Faculty of Population Health Sciences, UCL GOS Institute of Child Health, London.
- Joanne Hatton, Enterprise Systems Manager, Royal College of Paediatrics and Child Health, London
- Andrew Palmer, Head of Information Systems, Royal College of Paediatrics and Child Health, London

# Growth Charting Introduction

The UK-WHO 0-4 year old charts were officially launched on May 11th 2009. Any child born after that date should be plotted on a UK-WHO Growth chart. Children born before May 11th 2009 are plotted on British 1990 (UK90) charts and subsequent measurements must be plotted using those charts. After age 4 we revert to using UK90 charts.

## The LMS Method

It is now common practice to express child growth status in the form of SD scores - the number of standard deviations away from the mean.

The LMS method provides a way of obtaining normalized growth centile standards from a relatively small original dataset, applying smoothing and extrapolation such that the resulting L, M and S curves contain the information to draw **any** centile curve, and to convert measurements (even extreme values) into exact SD scores.

### How the LMS method is used

- Look up in the LMS table for the relevant measurement (eg height) the age and sex-specific values of L, M and S for the child. If the child's age falls between the ages references available, use cubic interpolation to create L, M amd S values interpolated to the child's exact age..

- To obtain the z-score, plug the LMS values with the child's measurement into the formula:
  ![formula](https://latex.codecogs.com/svg.latex?\=z={[(Measurement / M)-1] \over L S})

## Growth References

This is a growing list of growth references for children. These cover a number of specific medical conditions as well as a range of different physiological parameters. It will continue to be added to as more data becomes available. As a side-project of this work we are interested in collating an international library of growth references in computable format, which is at https://github.com/rcpch/growth-references and further details are available in that repository.

If you have a reference which you would like us to add, please contact us on growth.digital@rcpch.ac.uk

# Privacy

## Privacy Policy

Our RCPCH dGC API Privacy Policy can be viewed on our Developer Portal

https://dev.rcpch.ac.uk/privacy

## Stateless API

The server has been designed with privacy and information security in mind.

The API is 'stateless', meaning it does **not** persist information between the web requests that are made of it. Each request from the API-consuming application contains all the information required to calculate a set of centile data. The response we send back contains this data, and it is never saved on the server. Some information about requests is kept for a few days in the logs of our server, to enable us to monitor performance and to debug problems, however this information is anonymous.

Any 'persistence' (data saving) must happen in the application which is consuming the API, which is the natural place to persist data anyway, since this is the DPCHR, the GP system, the hospital EPR - which already likely persists lots of data about the patient.

In view of the stateless nature of the server, we don't handle any Patient Identifiable Data. We have reviewed the privacy implications of our application and we don't believe it currently requires a Data Privacy Impact Assessment, according to our review of [current Information Commissioner's Office guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-impact-assessments/#dpia3).
