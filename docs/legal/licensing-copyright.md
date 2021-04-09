
# Licensing and Copyright

## Open Source

The Project Board and Project Team all agreed, as responsible clinicians, that the growth references and the algorithms that generate reliable results should all be open source. They are published here under GNU Affero GPL3 licence.

!!! info "Clarifying some misconceptions often held about open source software"
    - Control over the open source code still remains completely and exclusively under the control of the RCPCH software development team.
    - Outside contributors cannot make any direct changes to the code. We can however accept positive improvements and contributions from the community via 'Pull Request' on GitHub, but the development team still control when and how these are introduced. We are under no obligation to accept contributions.
    - The code and intellectual property is still under the full and outright ownership of the RCPCH.
    - The terms of the licenses we issue *can* be changed for future versions of the software, if this is necessary. However we would only do this for reasons of improving the project.

## Copyright

### Software

All code in the Project is Copyright ⓒ 2020-2021 Royal College Of Paediatrics and Child Health, except where explicitly stated.

### Algorithms

The 'LMS' method used to create data tables from raw observational data, and to reverse the process, is in the Public Domain, being a widely-published scientific and statistical/mathematical innovation. The RCPCH makes no claim of ownership over this algorithm.

### Growth References

UK90 Growth References are Copyright ⓒ Royal College Of Paediatrics and Child Health.

Other references? Turner/Trisomy?

## Licensing summary

For details of licenses, please consult the root folder of the specific software component.

Primarily we have used two different [Open Source Initiative (OSI)](https://opensource.org/)-recognised licenses.

### [GNU Affero General Public License version 3](https://opensource.org/licenses/AGPL-3.0)

The RCPCH dGC API Server is licensed under the Affero GPL, in order to protect the 'copyleft' (also known as 'sharealike') feature within the license. This is to ensure that any other entities that wish to use the code as a web service are still required to share all source codemodifications they make.

### [The MIT License](https://opensource.org/licenses/MIT)

Components which we believe other organisations would derive benefit from being able to reuse in their own commercial products have been licensed using the MIT License which permits reuse of this nature and does not encumber the commercial product with copyleft or other conditions. This license is widely used for licensing open source programming languages, libraries, and other reusable software components, and is considered one of the 'industry standard' licenses for this purpose.

### RCPCHGrowth

The Python package within the `rcpchgrowth` folder in the dGC API Server which calculates the results served by the API, is eventually going to be released as a separate Python package, which may be under a different license to the Server itself (AGPL). It is likely to be released under an MIT license.

## Third-Party Tools, Libraries and Frameworks Licensing

* [Python](https://github.com/python/cpython/blob/master/LICENSE): [PSF License](https://directory.fsf.org/wiki/License:Python-2.0.1)

* [Flask](https://github.com/opentracing-contrib/python-flask/blob/master/LICENSE): [BSD 3-Clause License](https://directory.fsf.org/wiki/License:BSD-3-Clause)

* [React](https://github.com/facebook/react/blob/master/LICENSE): [MIT License](https://directory.fsf.org/wiki/License:Expat)

* [React-Native](https://github.com/facebook/react-native/blob/master/LICENSE): [MIT License](https://directory.fsf.org/wiki/License:Expat)

* [MkDocs](https://github.com/squidfunk/mkdocs-material/blob/master/LICENSE): [MIT License](https://directory.fsf.org/wiki/License:Expat)

(All the above licenses are compatible with the AGPL terms of the dgC API Server part of the project)
