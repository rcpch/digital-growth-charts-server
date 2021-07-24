---
title: Licensing and Copyright
reviewers: Dr Marcus Baw
---

# Licensing and Copyright

## Open Source

The Project Board and Project Team all agreed, as responsible clinicians, that the growth references and calculation code should be open source, enabling peer review, improving quality, and developing an international community of practice around these clinical tools .The are published here under GNU Affero GPL3 licence.

!!! info "Clarifying some misconceptions often held about open source software"
    - **Control**. Control over the open source code still remains completely and exclusively under the control of the RCPCH software development team.

    - **Modification**. Outside contributors **cannot** make any direct changes to our code. One of the most commonly heard myths about open source is the accusation that it is inherently insecure because 'anyone can change your code'. This is so far from the actual practical reality of open source that it beggars belief that so-called technology industry professionals do indeed believe it. Nevertheless, some do, through simple ignorance. We **can** however accept positive improvements and contributions from the community via 'Pull Request' on GitHub, but the development team still control when and how these are introduced. We are under no obligation to accept contributions.

    - **Ownership**. The code and intellectual property is still under the full and outright ownership of the RCPCH. This assertion of ownership and copyright is not in **any** way lessened by releasing the code under an open source license.

    - **Licensing**. The terms of the licenses we issue *can* be changed for future versions of the software, if this is necessary. However we would only do this for reasons of improving the project. Multiple licensing models can be used simultaneously, this is called a *dual-* (or even *tri*-) licensing arrangement.

    - **Security**. Allowing outsiders to see the source code does not introduce any security vulnerability whatsoever. Security does not come from hiding your code as in the closed-source model, it comes from high standards of security practice using best industry practice, cryptography, and modern tools.

    - Other myths exist which imply some weakness about open source projects; we are happy to discuss them if required in the [dGC Forum](https://openhealthhub.org/c/rcpch-digital-growth-charts)

## Copyright

### Software

All code in the Project is Copyright ⓒ 2020-2021 Royal College Of Paediatrics and Child Health, except where explicitly stated.

### Algorithms

The 'LMS' method used to create data tables from raw observational data, and to reverse the process, is in the Public Domain, being a widely-published scientific and statistical/mathematical innovation. The RCPCH makes no claim of ownership over this algorithm, neither is the algorithm subject to any of the licensing arrangements herein discussed.

### Growth References

* UK90 Growth References are Copyright ⓒ Royal College Of Paediatrics and Child Health.

* Other references such as those for Turner's syndrome and Trisomy 21 (Down's Syndrome) are the copyright of their respective owners.

## Licensing summary

For details of licenses, please consult the root folder of the specific software component.

Primarily we have used two different [Open Source Initiative](https://opensource.org/)-recognised licenses:

### [GNU Affero General Public License version 3](https://opensource.org/licenses/AGPL-3.0)

The RCPCH dGC API Server and its accompanying Python package library is licensed under the Affero GPL, in order to use the 'copyleft' (also known as 'sharealike') feature within the license. The aim of this is to ensure that any other entities that wish to deploy the the API or python package code as a web service are still required to share all source code modifications they make.

### [The MIT License](https://opensource.org/licenses/MIT)

Components which we believe other organisations would derive benefit from being able to directly reuse within their own commercial products have been licensed using the MIT License, which permits reuse of this nature, and does not encumber the commercial product with copyleft or other restrictive conditions. This license is widely used for licensing open source programming languages, libraries, and other reusable software components, and is considered one of the 'industry standard' licenses for this purpose.

## Third-Party Tools, Libraries and Frameworks Licensing

| Tool / Framework / Library                                                       | License                                                                     |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [Python](https://github.com/python/cpython/blob/master/LICENSE)                  | [PSF License](https://directory.fsf.org/wiki/License:Python-2.0.1)          |
| [Flask](https://github.com/opentracing-contrib/python-flask/blob/master/LICENSE) | [BSD 3-Clause License](https://directory.fsf.org/wiki/License:BSD-3-Clause) |
| [FastAPI](https://github.com/tiangolo/fastapi#license)                           | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |
| [React](https://github.com/facebook/react/blob/master/LICENSE)                   | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |
| [React-Native](https://github.com/facebook/react-native/blob/master/LICENSE)     | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |
| [MkDocs](https://github.com/squidfunk/mkdocs-material/blob/master/LICENSE)       | [MIT License](https://directory.fsf.org/wiki/License:Expat)                 |

All the above licenses are compatible with the AGPL terms of the dGC API Server and python package part of the project, and the MIT terms of the other parts.

All the above projects remain the copyright of their respective owners.

!!! quote "Further reading"
    **[Open Source is the Only Way For Medicine](https://medium.com/@marcus_baw/open-source-is-the-only-way-for-medicine-9e698de0447e)** - a blog post by one of the dGC team, Dr Marcus Baw, describes some of the reasons why open source is so fundamental for science and medicine in particular.
    
