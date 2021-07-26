---
title: Python development
reviewers: Dr Marcus Baw
---

# Running locally with Python

## Scripts

The `scripts/` folder contains some simple scripts to help with development. To run them, ensure they are made executable in your filesystem (they may not be by default depending on your OS).

You can do that in whatever File > Permissions > Make Executable menu your desktop provides, or for \*nix environments or the WSL you can type `chmod +x <filename>` to add executable permissions.

Run all scripts from the root of the project, or they won't work.

## Running the dGC Server locally with Python

!!! note
    Some of this setup is obvious to experienced Python developers, but it's documented here so that we all know the _same_ obvious. :grin: This helps us reduce development difficulty and speeds up onboarding of new team members.

### Managing Python versions, and dependencies such as libraries

#### Managing Python versions

We are using Python 3.8.3 currently for these algorithms. There are tools available to help you manage multiple different Python versions on the same machine. We are using `pyenv` here, however there are other ways to solve this problem, and you may already have a preferred method, in which case you should be able to use that.

#### Managing library / dependencies versions

If you `pip install` all of the dependencies in `requirements.txt` **globally** on your machine, then you can encounter problems if you develop other Python applications on the same machine, for example if ydifferent projects need different versions of the same library.

The solution we have chosen is to use `pyenv-virtualenv` which is an extension to `pyenv` which helps you to manage separate 'environments' for each Python project you work on. (again, other solutions are available)

If you install and set up `pyenv` then the correct Python version will be selected automatically when you navigate to the directory containing this repository, because of the file `.python-version`

### Installing `pyenv`

[pyenv installer](https://github.com/pyenv/pyenv-installer)

### Example setup commands for this repository

`git clone` this repository into a suitable location on your development machine

```bash
git clone https://github.com/rcpch/digital-growth-charts-server.git
```

`cd` into the directory

```bash
cd digital-growth-charts-flask-client
```

Install the correct Python version

```bash
pyenv install 3.8.0
```

Create a virtualenv for this project 'growth-charts' abbreviated to 'gc-3.8' using Python 3.8.0

```bash
pyenv virtualenv 3.8.0 dgc-flask-app
```

!!! tip "Auto-selection of Python and virtualenv"
    Using the same name 'dgc-flask-app' will enable it to be automatically selected when navigating to this repo (but you _can_ call your own virtualenv whatever you like). This all works using the `.python-version` file in the project root, which can contain either a Python version name which `pyenv` recognises, or it can contain a virtualenv name, which `pyenv` will select for you, and of course this automatically selects the Python version too. A helpful article about this is here <https://realpython.com/intro-to-pyenv/#activating-your-versions>

Check virtualenv creation worked.

`pyenv virtualenvs` should return something like:

```bash
dgc-flask-app (created from /home/my-user/.pyenv/versions/3.8.0)
```

Activate the virtualenv manually if it's not already selected

```bash
pyenv activate dgc-flask-app
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

from the application's root directory, type

```bash
s/start-server
```

You should then see some messages from the Flask development server, which should look like:

```bash
 * Serving Flask app "app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

There may be some other messages at the end of that output for other processes which run on server startup.

If you need to vary any of the parameters passed to Flask, you can either modify the startup script or, using the commands in the startup script as a guide, pass the commands to the shell manually.
