---
title: Licensing and Copyright
reviewers: Dr Marcus Baw, Dr Anchit Chandran
audience: implementers, developers, clinicians
---

# Licensing and Copyright

## Open Source

As responsible clinicians, the Project Board and Project Team all agreed the growth references and calculation code should be open source, enabling peer review, improving quality, and development of an international community of practice around these clinical tools.

!!! info "Open Source Mythbuster - clarifying common misconceptions"
    **Control**: control over the open source code still remains completely and exclusively under the control of the RCPCH software development team.

    **Modifications**: outside contributors **cannot** make any direct changes to our code. One of the most common myths about open-source software relates to it being insecure because "anyone can change your code". This is simply not true. However, we **can** accept positive improvements and contributions from the community via 'Pull Request' on GitHub. Even then, the development team still control when and how these are introduced. We are under no obligation to accept contributions.

    **Ownership**: the code and intellectual property is still under the full and outright ownership of the RCPCH. This assertion of ownership and copyright is not in **any** way lessened by releasing the code under an open-source license.

    **Licensing**: if necessary, the terms of the licenses we issue *can* be changed for future versions of the software. However, we would only do this for reasons of improving the project. Multiple licensing models can be used simultaneously: this is called a *dual-* (or even *tri*-) licensing arrangement.

    **Security**: allowing outsiders to see the source code does not introduce any security vulnerability. Security does not come from obscurity - hiding your code, as in the closed-source model. It comes from high standards of security practice, using the best industry practices, robust cryptography, and modern tools and approaches, described in Factor III of the ["12-Factor" application development philosophy](https://12factor.net/).

    Other myths exist which imply some weakness about open-source projects. We are happy to discuss them if required in the [dGC Forum](https://forum.rcpch.tech/).

## Copyright Notices

### Software

All code in the Project is Copyright ⓒ 2020-2021 Royal College of Paediatrics and Child Health, except where explicitly stated.

### Algorithms

The 'LMS' method used to create data tables from raw observational data, and to reverse the process, is in the Public Domain, being a widely-published scientific and statistical/mathematical innovation. The RCPCH makes no claim of ownership over this algorithm, neither is the algorithm subject to any of the licensing arrangements herein discussed.

### Growth References

* UK90 Growth References are Copyright ⓒ Royal College of Paediatrics and Child Health.

* Other references, such as those for Turner syndrome and Down Syndrome, are the copyright of their respective owners.

## Licensing summary

For details of licenses, please consult the root folder of the specific software component.

Primarily, we have used two different [Open Source Initiative](https://opensource.org/)-recognised licenses:

### [GNU Affero General Public License version 3](https://opensource.org/licenses/AGPL-3.0)

The RCPCH Digital Growth Charts API Server and its accompanying Python package library is licensed under the Affero GPL, to use the 'copyleft' (also known as 'sharealike') feature within the license. The aim is to ensure any other entities wishing to deploy the API, or Python package code as a web service, are **still required to share all source code modifications they make, back to the community**.

### [The MIT License](https://opensource.org/licenses/MIT)

Components which other organisations would benefit from being able to directly reuse within their own commercial products have been licensed using the MIT License, which permits reuse of this nature, and does not encumber the resulting commercial product with any copyleft or other restrictive conditions. This license is widely used for licensing open-source programming languages, libraries, and other reusable software components, and is considered one of the 'industry standard' licenses for this purpose.

## Open Source Licenses and Software Bill of Materials

| Tool / Framework / Library                                                       | License                                                                     |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [Python](https://github.com/python/cpython/blob/master/LICENSE)                  | [PSF License](https://directory.fsf.org/wiki/License:Python-2.0.1)          |
| [Flask](https://github.com/opentracing-contrib/python-flask/blob/master/LICENSE) | [BSD 3-Clause License](https://directory.fsf.org/wiki/License:BSD-3-Clause) |
| [FastAPI](https://github.com/tiangolo/fastapi#license)                           | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |
| [React](https://github.com/facebook/react/blob/master/LICENSE)                   | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |
| [React-Native](https://github.com/facebook/react-native/blob/master/LICENSE)     | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |
| [MkDocs](https://github.com/squidfunk/mkdocs-material/blob/master/LICENSE)       | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |

All the above licenses are compatible with the AGPL terms of the Digital Growth Charts API Server and Python package part of the project, and the MIT terms of the other parts.

All the above projects remain the copyright of their respective owners.

!!! quote "Further reading on Open Source"
    **[Open Source is the Only Way For Medicine](https://medium.com/@marcus_baw/open-source-is-the-only-way-for-medicine-9e698de0447e)** - a blog post by one of the dGC team, Dr Marcus Baw, describes some reasons why open source is so fundamental for science and medicine in particular.
