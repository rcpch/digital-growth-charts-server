---
title: Python package
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# rcpchgrowth Python package

The calculation functions within the dGC API are powered by a self-contained Python package which has been extracted out into a separate repository and is published on [PyPi](https://pypi.org/project/rcpchgrowth/), the Python Package Index. This enables the centile calculation functions to be used in other programs. 

## Installation

To add to your project:

``` bash
pip install rcpchgrowth
```

## License

We have taken the slightly unusual step of licensing the python package under the GNU Affero GPL, which may restrict commercial reuse models. We've done this because all of the 'heavy lifting' of the API server depends on this package, and we wanted to protect it from 'unofficial' commercial competing APIs.

If this licensing issue restricts your valid, patient-benefiting, non-profit use-case, then please do reach out to us and we will consider dual-license options or some other arrangement that helps you.

## Feedback

We'd be interested to hear from people who are using the RCPCHGrowth python package, so we can learn more about the use-cases and how we might continue to improve the package.

## Contributing

If you want to contribute to the project, you will need clone the [repository](https://github.com/rcpch/rcpchgrowth-python) and create a python environment based on 3.8.3:

``` bash
pyenv virtualenv 3.8.3 rcpch-growth-python
```