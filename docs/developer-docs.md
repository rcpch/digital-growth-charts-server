# Developer Documentation

- [Frequently Asked Questions](https://openhealthhub.org/t/frequently-asked-questions/2328)
- [Centile Advice Strings (legacy)](centile-advice-strings.md)
- [About Calculation of Growth Parameters in Code](calculating-growth-parameters.md)
- [Client Specification](client_specification.md)

---


## Scripts

This folder contains some simple scripts to help with development.  
To run them, ensure they are made executable in your filesystem (they may not be by default depending on your OS).  
You can do that in whatever File > Permissions > Make Executable menu your desktop provides, or for \*nix environments or the WSL you can type
`chmod +x <filename>` to add executable permissions.

## Running the dGC Server in Docker

- `git clone` this repository, if you haven't already, to a suitable place on your local machine.

### Build the Docker image with all required dependencies

- run the `s/build-docker` script which will build the Docker image with all the required dependencies
  This is useful for rapidly getting a development environment set up.  
  Pulls the base Python image, deletes any existing identically-named images, builds the new image.

### Start the Docker container

- run the `s/start-docker` script, which will run the image in a Docker container.
- The dGC server should be running in development mode in the container, and mapped to the port https://localhost:5000

## Running the dGC Server locally with Python

> some of this is obvious to experienced Python developers, but it's documented here so that we all know the _same_ obvious.

### Managing Python versions, and dependencies such as libraries

- We are using Python 3.8.0 currently for these algorithms. There are tools available to help you manage multiple different Python versions on the same machine. We are using `pyenv` here, however there are other ways to solve this problem, and you may already have a preferred method, in which case you should be able to use that.

- Similarly, if you `pip install` all of the dependencies in `requirements.txt` globally on your machine, then you can encounter problems if you develop other Python applications on the same machine, for example if you need different versions of the same library. The solution to this is to use `pyenv-virtualenv` which is an extension to `pyenv` which helps you to manage separate 'environments' for each Python project you work on.

- If you install and set up `pyenv` then the correct Python version will be selected automatically when you navigate to the directory containing this repository, because of the file `.python-version`

### Installing `pyenv`

- [pyenv installer](https://github.com/pyenv/pyenv-installer)
- [pyenv command reference](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local)

### Setup for this repository

- `git clone` this repository into a suitable location on your development machine  
  `$ git clone https://github.com/rcpch/digital-growth-charts-flask-client.git`
- `cd` into the directory  
  `$ cd digital-growth-charts-flask-client`
- Install the correct Python version  
  `$ pyenv install 3.8.0`
- Create a virtualenv for this project 'growth-charts' abbreviated to 'gc-3.8' using Python 3.8.0  
  `$ pyenv virtualenv 3.8.0 gc-3.8`  
  (Using the same name 'gc-3.8' will enable it to be automatically selected when navigating to this repo - but you can call your own virtualenv whatever you like)
- Check virtualenv creation worked  
  `pyenv virtualenvs` should return something like  
  `* gc-3.8 (created from /home/my-user/.pyenv/versions/3.8.0)` (\* asterisk indicates it is selected)
- Activate the virtualenv manually if it's not already selected  
  `$ pyenv activate gc-3.8`
- Install the dependencies to this virtualenv  
  `$ pip install -r requirements.txt`
- Refer to the pyenv command reference link (previous section) if you need further information on `pyenv`

### Extra development packages that may be required on some setups

On some platforms, you may need the additional development header packages. On Ubuntu/Linux Mint this was required when using `pyenv` and thus compiling Python from source. This should not be necessary if you're running a binary Python, it only affects setups which are compiling a specific Python version from source, on demand, such as `pyenv`.

`$ sudo apt-get install liblzma-dev libbz2-dev zlib1g-dev`

and then recompile the Python that `pyenv` built

`$ pyenv install 3.8.0`

## Start the API server natively with default settings

- `$ s/start-server` in the application root

You should then see some messages from the Flask development server, which should look like

```
 * Serving Flask app "app.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: xxx-xxx-xxx
```

There may be some other messages at the end of that output for other processes which run on server startup

If you need to vary any of the parameters passed to Flask, you can either modify the startup script or simply pass the commands to the shell manually.

Scripts are located in the `s/` folder in the application root.



## Support

- Our primary support method is through the forum at https://openhealthhub.org/c/rcpch-digital-growth-charts/

- Commercial support is also available for this API and for integration with your software solution, please contact growth.digital@rcpch.ac.uk
