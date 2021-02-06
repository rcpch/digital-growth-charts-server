# Developer Documentation

<!-- TOC -->

- [Developer Documentation](#developer-documentation)
  - [Why Python?](#why-python)
  - [Running the dGC Server in Docker](#running-the-dgc-server-in-docker)
  - [Running the dGC Server locally with Python](#running-the-dgc-server-locally-with-python)
    - [Managing Python versions, and dependencies such as libraries](#managing-python-versions-and-dependencies-such-as-libraries)
    - [Installing `pyenv`](#installing-pyenv)
    - [Setup for this repository](#setup-for-this-repository)
    - [Extra development packages that may be required on some setups](#extra-development-packages-that-may-be-required-on-some-setups)
  - [Running the API server application in development](#running-the-api-server-application-in-development)
  - [Contributing](#contributing)
    - [How to contribute](#how-to-contribute)
    - [Coding style](#coding-style)
  - [Intellectual Property (IP)](#intellectual-property-ip)

<!-- /TOC -->

- [Frequently Asked Questions](frequently-asked-questions.md)
- [Centile Advice Strings (legacy)](centile-advice-strings.md)
- [About Calculation of Growth Parameters in Code](about-calculating-growth-parameters.md)
- [Client Specification](client_specification.md)
- [Technical Acknowledgements](technical-acknowledgements.md)
- TODO: Alternative growth reference data
- TODO: Adding new calculations to the API
- TODO: Testing the API

---

## Why Python?

- Python has become the de-facto language of the scientifica and bioinformatics communities.
- Most of the packages we needed were '1st party' ie maintained by the PSF
- We think it's a nice language to use.
- It's accessible to clinicians who want to learn to code, and it's easy enough to learn that it's taught in schools.
- It has everything we needed for building an API and web layers we needed.

## Running the dGC Server in Docker

- Install Docker. How to do this varies by platform so go to https://www.docker.com/get-started to find out more
- `git clone` this repository, if you haven't already, to a suitable place on your local machine.
- run the `s/rebuild-docker` script which will build the Docker image.
- run the `s/start-docker` script, which will run the image in a Docker container.
- The dGC server should be running in development mode on https://localhost:5000

TODO: #124 Prebuilt Docker image on Docker Hub

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

## Running the API server application in development

Simply type
`$ s/start-server` in the application root

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

If you need to vary any of the parameters passed to Flask, you can either modify the startup script or simply pass the commands to the shell manually.

Scripts are located in the `s/` folder in the application root.

## Contributing

We're a friendly bunch and we're happy to chat. You can get in touch with the primary developers to talk about the project using:
marcusbaw@gmail.com (Marcus Baw) or eatyourpeasapps@gmail.com (Simon Chapman)

We aim to eventually have an RCPCH forum up and running which you will also be able to use to talk about the project.

### How to contribute

- Fork the repository to your own GitHub account
- Set up your development environment (ideally using our instructions [here](python-development.md) for maximum compatibility with our own development environments)
- Ideally, you should have discussed with our team what you are proposing to change, because we can only accept pull requests where there is an accepted need for that new feature or fix.
- We can discuss with you how we would recommend to implement the new feature, for maximum potential 'mergeability' of your PR.
- Once the work is ready to show us, create a pull request on our repo, detailing what the change is and details about the fix or feature. PRs that affect the calculations or any other 'mission critical' part of the code will need suitable tests which we can run.
- We will endeavour to review and merge in a reasonable time frame, but will usually not merge straight into `master`, rather we will merge into an upcoming release branch.

### Coding style

- We are not Python experts but we would encourage use of Python best practices where possible.
- We are not going to get too pedantic over style though.
- Some helpful sources of information on Python style are:  
  <https://www.python.org/dev/peps/pep-0008>  
  <https://google.github.io/styleguide/pyguide.html>

## Intellectual Property (IP)

- The copyright over the IP in this and other Growth Chart related repositories is owned by the Royal College of Paediatrics and Child Health, which releases it under an open source license. Consult the individual repository for specifics on which license we have used.
- If you submit a contribution to the repository, you agree to transfer all IP rights over the contribution, both now and in the future, to the Royal College of Paediatrics and Child Health, in perpetuity. This clause is purely to allow RCPCH to continue to exert an unchallenged copyright over the work.
- For larger contributions we may require a Contributor Covenant to support this agreement over transfer of title, however for small contributions it is probably sufficient that you should have read and understood this document, and that the act of submitting a PR is acceptance of these terms.
- All contributors will, of course, proudly be acknowledged in the [Acknowledgements](acknowledgements.md) section.
