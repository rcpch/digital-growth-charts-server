---
title: Python package
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# rcpchgrowth Python package

The calculation functions within the dGC API are powered by a self-contained Python package which has been extracted out into a separate repository and is published on [PyPi](https://pypi.org/project/rcpchgrowth/), the Python Package Index. This enables the centile calculation functions to be used in other programs. 

![python_library](../_assets/_images/python_library_carbon.png)

:octicons-mark-github-16: [GitHub Repository](https://github.com/rcpch/rcpchgrowth-python)

:fontawesome-brands-python: [PyPi Package](https://pypi.org/project/rcpchgrowth/)

## Installation

To add rcpchgrowth to your project, install via `pip`

``` bash
pip install rcpchgrowth
```

## License

We have taken the slightly unusual step of licensing the python package under the [GNU Affero General Public License version 3](https://opensource.org/licenses/AGPL-3.0), which may restrict commercial reuse models. We've done this because all of the 'heavy lifting' of the API server depends on this package, and we wanted to protect it from 'unofficial' commercial competing APIs, at least until the model of Royal College-delivered APIs is established and secure.

!!! tip "Helpful licensing"
    If this licensing issue restricts your valid, patient-benefiting, non-profit use-case, then please do reach out to us and we will consider dual-license options or some other arrangement that helps you.

## Feedback

We'd be interested to hear from people who are using the RCPCHGrowth python package, so we can learn more about the use-cases and how we might continue to improve the package. Please do [create issues on our GitHub repo](https://github.com/rcpch/rcpchgrowth-python/issues), or discuss the package in the [dGC Forums](https://openhealthhub.org/c/rcpch-digital-growth-charts)

## Contributing

If you want to contribute to the project, please read the section on [Contributing](/docs/developer/contributing.md).