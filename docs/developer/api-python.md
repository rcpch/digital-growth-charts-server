---
title: Python development
reviewers: Dr Marcus Baw, Dr Anchit Chandran
---

# Running locally with Python

## Scripts

The `scripts/` folder contains some simple scripts to help with development. To run them, ensure they are made executable in your filesystem (they may not be by default depending on your OS).

You can do that in whichever File > Permissions > Make Executable menu your desktop provides.

For \*nix environments or the WSL, you can type `chmod +x <filename>` to add executable permissions.

Run all scripts from the root of the project, or they won't work.

## Running the dGC Server locally with Python

!!! note
    Some of this setup is obvious to experienced Python developers, but it's documented here so we all know the _same_ obvious :grin:. This helps us reduce development difficulty and speeds up onboarding of new team members.

### Managing Python versions, and dependencies such as libraries

#### Managing Python versions

Currently, we use Python 3.8.3 for these algorithms.

There are tools available to help you manage multiple different Python versions on the same machine. We use `pyenv` here, however, there are other ways to solve this problem. If you already have a preferred method, you should be able to use that.

#### Managing library / dependencies versions

If you `pip install` every dependency in `requirements.txt` **globally** on your machine, you can encounter problems if you develop other Python applications on the same machine. For example, different projects may need different versions of the same library.

Our solution is to use `pyenv-virtualenv` which is an extension to `pyenv` which helps you to manage separate 'environments' for each Python project you work on. Other solutions are available if preferred.

After installing and setting up `pyenv`, the correct Python version will be automatically selected when you navigate to the directory containing this repository, because of the  `.python-version` file.

### Installing `pyenv`

[pyenv installer](https://github.com/pyenv/pyenv-installer)

### Example setup commands for this repository

`git clone` this repository into a suitable location on your development machine

```bash
git clone https://github.com/rcpch/digital-growth-charts-server.git
```

`cd` into the directory

```bash
cd digital-growth-charts-server
```

Install the correct Python version

```bash
pyenv install 3.8.0
```

Create a virtualenv for this project 'growth-charts', abbreviated to 'gc-3.8' using Python 3.8.0

```bash
pyenv virtualenv 3.8.0 dgc-server
```

!!! tip "Auto-selection of Python and virtualenv"
    Using 'dgc-server' as the name will enable it to be automatically selected when navigating to this repo (but you _can_ call your own virtualenv whatever you like). This all works using the `.python-version` file in the project root. This can contain either a Python version name which `pyenv` recognises, or it can contain a virtualenv name, which `pyenv` will select for you (and this automatically selects the Python version too).

    A helpful article about this is here: <https://realpython.com/intro-to-pyenv/#activating-your-versions>.

#### Check virtualenv creation worked

`pyenv virtualenv`s should return something like:

```bash
dgc-server (created from /home/my-user/.pyenv/versions/3.8.0)
```

Activate the virtualenv manually if it's not already selected

```bash
pyenv activate dgc-server
```

Install the dependencies inside this virtualenv

```bash
pip install -r requirements.txt
```

Refer to the [pyenv command reference](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local) if you need further information on `pyenv`

!!! tip "Extra development packages that may be required on some setups"
    On some platforms, you may need the additional development header packages. On Ubuntu/Linux Mint this was required when using `pyenv` and thus compiling Python from source. This should not be necessary if you're running a binary Python, it only affects setups which are compiling a specific Python version from source, on demand, such as `pyenv`.

    ```bash
    sudo apt-get install liblzma-dev libbz2-dev zlib1g-dev
    ```

    and then recompile the Python that `pyenv` built earlier

    ```bash
    pyenv install 3.8.3
    ```

!!! note "If installing on macOS Big Sur, pyenv install of python 3.8.0 and requirements.txt may fail"
    To install 3.8.3 via pyenv, set the following 2 environment variables (requires homebrew installed versions of bzip2, openssl and zlib):

```bash
export CFLAGS="-I$(brew --prefix openssl)/include -I$(brew --prefix bzip2)/include -I$(brew --prefix readline)/include -I$(xcrun --show-sdk-path)/usr/include"
export LDFLAGS="-L$(brew --prefix openssl)/lib -L$(brew --prefix readline)/lib -L$(brew --prefix zlib)/lib -L$(brew --prefix bzip2)/lib"
```

Now, run the pyenv install with a patch for Big Sur:

```bash
pyenv install --patch 3.8.0 < <(curl -sSL https://github.com/python/cpython/commit/8ea6353.patch\?full_index\=1)
```

Now, once ready to install requirements.txt with pip, set one more environment variable:

```bash
export SYSTEM_VERSION_COMPAT=1
```

## Start the API server natively with default settings

From the application's root directory, type

```bash
s/uvicorn-start
```

You should see messages from the uvicorn development server like:

```bash
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [61645] using watchgod
INFO:     Started server process [61647]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

There may be other messages at the end of the output for other processes which run on server start-up.

If you need to vary any of the parameters passed, you can either:

1. Modify the start-up script
2. Manually pass the commands to the shell, using the commands in the start-up script as a guide 