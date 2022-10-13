---
title: RCPCHGrowth CLI
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# Developing the RCPCH CLI tools

Setup and installation of Python proceeds in a similar way to how it is described in [Python setup](./api-python.md)

## Get the code
Git clone the repository to your development machine, and `cd` into it
``` console
git clone https://github.com/rcpch/rcpchgrowth-python-cli.git
```

## Virtualenv
We recommend the use of Pyenv and a virtual environment. Any recent python version should be fine.
```
pyenv virtualenv 3.10.2 rcpchgrowth-python-cli
```

Using the same name `rcpchgrowth-python-cli` for your virtualenv will enable pyenv to automatically select it when you navigate to the directory, this magic uses the `.python-version` dotfile int he project root.

## Locally install for testing
To install the development version of the library locally so you can test out your changes, you can use
```
pip install -e .
```

Now any changes you make to the local code will immediately be reflected in the CLI tool

## Versioning

We use a package called `bump2version` which is a maintained fork of the original but abandoned `bumpversion`.

You need to start with a clean commit status, ie any new changes are committed in Git

To update the version with a small patch change or fix, use

``` console
bumpversion patch
```

For 'minor' version changes use

``` console
bumpversion minor
```

And for a 'major' version use
``` console
bumpversion major
```

Bump2version will update the version in `setup.py` and will create a new commit and tag.