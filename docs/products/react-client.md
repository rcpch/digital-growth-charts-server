---
title: React Demo Client
reviewers: Dr Marcus Baw, Dr Anchit Chandran
---

# React Demo Client

{% set repository_name="rcpch/digital-growth-charts-react-client" -%}

[![Github Issues](https://img.shields.io/github/issues/{{ repository_name }})](https://github.com/{{ repository_name }}/issues)
[![Github Stars](https://img.shields.io/github/stars/{{ repository_name }})](https://github.com/{{ repository_name }}/stargazers)
[![Github Forks](https://img.shields.io/github/forks/{{ repository_name }})](https://github.com/{{ repository_name }}/network/members)
[![Github Licence](https://img.shields.io/github/license/{{ repository_name }})](https://github.com/{{ repository_name }}/blob/live/LICENSE)
[![GitHub Pages Build & Deploy](https://github.com/rcpch/digital-growth-charts-react-client/actions/workflows/deploy-react-app-gh-pages.yml/badge.svg)](https://github.com/rcpch/digital-growth-charts-react-client/actions/workflows/deploy-react-app-gh-pages.yml)

[:octicons-mark-github-16: GitHub repository](https://github.com/{{ repository_name }})

[:material-web: Online Demo](https://growth.rcpch.ac.uk/)

--8<--
docs/_assets/_snippets/htn-award.md
--8<--

This client, written in React.js, is for demonstration of the API and the chart library component. This is now the main focus of development for our RCPCH Digital Growth Charts Demo Client. We previously built a [Flask-based client](https://github.com/rcpch/digital-growth-charts-flask-client) (which used Flask only because that client actually split off from the original API development). The Flask client code is still available as an educational tool, however it is considered deprecated and will not receive updates.

We have attempted to build the very best of growth chart theory and practice into the React client, including guidance given to us by the RCPCH Digital Growth Charts Project Board, and accepted best practice from the days of paper growth charts.

## Notes regarding the React client

### Colours for the charts have been updated

It was felt that representing boys' charts with blue lines and girls' charts with pink lines did not necessarily fit with 21st Century sensibilities of sex and gender. A Project Board decision was made to make the default chart colour monochrome black/grey.

'Traditional' growth chart pink and blue colours are available as an option, and we have created som other colour options named after James Tanner who pioneered the study of childrens' growth, showing off the capability of the chart component to be customised.

### Other documentation

- [Clinician documentation](../clinician/how-the-api-works.md)
- [Integrator documentation](../integrator/getting-started.md)
- [API documentation](../integrator/api-reference.md)
- [Developer documentation](../developer/react-client.md)
- [Contributor documentation](../developer/start-here.md)

--8<--
docs/_assets/_snippets/docs-contributions.md
--8<--
