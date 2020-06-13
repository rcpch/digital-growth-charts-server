## Developing with Python

> some of this is obvious to Python developers, but it's documented here so that we all know the _same_ obvious.

### Managing Python versions, and dependencies such as libraries

* We are using Python 3.8.0 currently for these algorithms. There are tools available to help you manage multiple different Python versions on the same machine. We are using `pyenv` here, however there are other ways to solve this problem, and you may already have a preferred method, in which case you should be able to use that.
* Similarly, if you `pip install` all of the dependencies in `requirements.txt` globally on your machine, then you can encounter problems if you develop other Python applications on the same machine, for example if you need different versions of the same library. The solution to this is to use `pyenv-virtualenv` which is an extension to `pyenv` which helps you to manage separate 'environments' for each Python project you work on.
* If you install and set up `pyenv` then the correct Python version will be selected automatically when you navigate to the directory containing this repository, because of the file `.python-version`

### Installing `pyenv`

* [pyenv installer](https://github.com/pyenv/pyenv-installer)
* [pyenv command reference](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md#pyenv-local)

### Setup for this repository

* Install the correct Python version  
`$ pyenv install 3.8.0`  
* Create a virtualenv for this project 'growth-charts' abbreviated to 'gc-3.8' using Python 3.8.0  
`$ pyenv virtualenv 3.8.0 gc-3.8`  
(Using the same name 'gc-3.8' will enable it to be automatically selected when navigating to this repo - but you can call your own virtualenv whatever you like)  
* Check virtualenv creation worked  
`pyenv virtualenvs` should return something like  
`* gc-3.8 (created from /home/my-user/.pyenv/versions/3.8.0)` (* asterisk indicates it is selected)  
* Activate the virtualenv manually if it's not already selected  
`$ pyenv activate gc-3.8` 
* Install the dependencies to this virtualenv  
`$ pip install -r requirements.txt`  
* Refer to the pyenv command reference link (previous section) if you need further information on `pyenv`  

> NEXT: [Running the Growth Chart API in development](running-in-development.md)
