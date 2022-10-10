<p align="center">
    <img width="200px" src="https://github.com/rcpch/digital-growth-charts-documentation/raw/live/docs/_assets/_images/rcpch_logo.png"/>
    <p align="center">Designed and built by the RCPCH, by clinicians for clinicians.</p>
</p>
<p align="center">
    <img align="center" width="100px" src="https://github.com/rcpch/digital-growth-charts-documentation/raw/live/docs/_assets/_images/htn-awards-winner-2020-logo.jpg"/>
    <img align="center" width="100px" src="https://github.com/rcpch/digital-growth-charts-documentation/raw/live/docs/_assets/_images/logo-block-outline-sm.png"/>
    <p align="center">Winner 2020 HTN Health Tech Awards - Best Health Tech Solution</p>
    <p align="center">This project is part of the <a href="https://publicmoneypubliccode.org.uk/">Public Money Public Code</a> community</p>
</p>

# RCPCH dGC Project Documentation Site

This site is built with [Material for MKDocs](https://squidfunk.github.io/mkdocs-material/) and contains all documentation for all parts of the RCPCH Digital Growth Charts Project.

<a href="https://growth.rcpch.ac.uk/"><img src="docs/_assets/_images/2021-07-24-13-58-40-screenshot.png" width="100%"></a>

Click the image or see the documentation here <https://growth.rcpch.ac.uk/>

-----

BACKUP SITE: <https://rcpch.github.io/digital-growth-charts-documentation/>


### License

All content of this documentation repository is Copyright ⓒ 2020-2021 Royal College Of Paediatrics and Child Health and released under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License](https://creativecommons.org/licenses/by-sa/4.0/)

For licensing of the other parts of the project, see [Licensing and Copyright](https://growth.rcpch.ac.uk/legal/licensing-copyright/) in the documentation site.

## Setting up a development environment for the dGC documentation site

Create a virtualenv for the python modules
```
pyenv virtualenv 3.10.2 mkdocs
```

Install Material for MKDocs and the Swagger plugin
```
pip install mkdocs-material mkdocs-render-swagger-plugin
```

Now start the server
```
mkdocs serve
```

### Notes

* on some platforms, if you get the error `ModuleNotFoundError: No module named '_ctypes'` then you need to run `sudo apt-get install libffi-dev` or the equivalent on your platform, and then recompile your Python (if using pyenv, simply `pyenv install 3.10.2` will recompile that Python binary)

* Tested Oct 2022 on Linux Mint 21.0
