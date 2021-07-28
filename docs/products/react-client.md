---
title: React Demo Client
reviewers: Dr Marcus Baw
---

# React Demo Client

![Github Issues](https://img.shields.io/github/issues/rcpch/digital-growth-charts-react-client) ![Github Stars](https://img.shields.io/github/stars/rcpch/digital-growth-charts-react-client) ![Github Forks](https://img.shields.io/github/forks/rcpch/digital-growth-charts-react-client) ![Github Licence](https://img.shields.io/github/license/rcpch/digital-growth-charts-react-client)
<!--![Actions Status](https://github.com/rcpch/digital-growth-charts-server/actions/workflows/alpha_rcpch-dgc-server-alpha.yml/badge.svg?branch=alpha)-->

:octicons-mark-github-16: [Github repository](https://github.com/rcpch/digital-growth-charts-react-client)

:material-web: [Website](https://growth.rcpch.ac.uk/)

<!--
![Logo](../_assets/_images/rcpch-logo.png){ align = center; : style="height:200px;width:200px"}-->

![HTN Awards](../_assets/_images/htn-awards-winner-2020-logo.jpg){: style="height:200px;width:200px"}
 

This client, written in React.js, is for demonstration of the API and the chart library component. This is now the main focus of development for our RCPCH Digital Growth Charts Demo Client. We previously built a [Flask-based client](https://github.com/rcpch/digital-growth-charts-flask-client) (which used Flask only because that client actually split off from the original API development). The Flask client code is still available as an educational tool, however it is considered deprecated and updating it is not a high priority.

We have attempted to build into the React client the best of growth chart theory and practice, including guidance given to us by the RCPCH Digital Growth Charts Project Board.

## Clinical notes regarding the React client

### Pink and Blue no longer used for the charts

- It was felt that representing boys' charts with blue lines and girls' charts with pink lines did not really fit with 21st Century sensibilities of sex and gender. A Project Board decision was made to remove these colours and simply render the charts in monochrome black/grey.

## Documentation

- API documentation can be found [here](../integrator/api-reference.md) 

- If you spot errors or inconsistencies in any documentation, please do point them out to us either by creating an Issue in the relevant repository, or by making a pull request with a fix. We will [acknowledge](../about/acknowledgements) all contributors.

## Developer documentation

Built in React using Semantic UI React.

### Set Up

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

1. Install React [here](https://reactjs.org/docs/getting-started.html)
1. Clone the repo
1. Navigate to the root of the folder
1. `npm login --registry=https://npm.pkg.github.com` and
1. `npm install`
1. `npm start`

### Style

- We recommend the use of the Prettier Javascript linter

## Other documentation

- [Integrator documentation](../integrator/getting-started.md)
- [Contributor documentation](../developer/start-here.md)
- [Clinician documentation](../clinician/how-the-api-works.md)
