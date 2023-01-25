---
title: Writing Documentation
reviewers: Dr Marcus Baw
---

# Writing dGC Documentation

Where possible we have tried to bring together **all** documentation relating to any aspect of the project into this one MkDocs site, which is published at [growth.rcpch.ac.uk](https://growth.rcpch.ac.uk)

## MkDocs

The documentation for the Digital Growth Charts project is created using the MkDocs documentation framework, and uses the theme 'Material for MkDocs', which adds a number of extra features and an more modern appearance than plain MkDocs. We use the Material for MkDocs Insiders edition which allows us to support the project while getting a few neat early-access features.

There is (as you'd expect) some delightful documentation for both projects: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), and for the underlying [MkDocs](https://www.mkdocs.org/) which it's built on. You may need to refer to both at times, for different features.

## Adding or editing documentation

Mostly this just requires creating Markdown files in the `docs/` directory of the [documentation repository](https://github.com/rcpch/digital-growth-charts-documentation).

Use other pages within this repo to get ideas on the style and the features available such as [emoji](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#emoji), [icons](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#using-icons), [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/), etc.

### Continuous Integration via GitHub Actions

Any changes to the `live` branch of the documentation repository trigger a [GitHub Action](https://github.com/rcpch/digital-growth-charts-documentation/blob/live/.github/workflows/build-and-deploy-to-gh-pages-and-azure.yml) which runs Material for MkDocs in a temporary application container, builds the site from the Markdown source into a set of static HTML pages, and [publishes the site to Azure](https://growth.rcpch.ac.uk/), (with a [backup in GitHub Pages](https://rcpch.github.io/digital-growth-charts-documentation/)).

This will occur whether the changes are made using an online editing method or a local, offline editing method.

If you don't want changes to go live right away, use another branch such as `prerelease` or any other branch name of your choosing, this will not trigger updates to live.

!!! note GitHub Branch Protection
    In the near future we will apply GitHub branch protection to `live` so that changes cannot be made directly there but **must** be made through an intermediate branch and then PR'd into `live`.

### Online editing of the Markdown

If you are new to Markdown editing, you can use GitHub's interface itself to edit online, by clicking the 'pencil' edit icon in the top right corner of any source code page. There are also external tools like [Prose.io](http://prose.io/) and [StackEdit](https://stackedit.io/) which give you a nice interface for editing MarkDown online, and will sync the changes with GitHub for you. If you need help getting set up, [contact us in the Signal chat](../about/contact.md).

### Using a text editor and editing locally

More experienced coders can `git clone` the repo and make changes offline on their local machine before pushing to the remote (either the `rcpch` organisation's remote, or their own fork). This allows you to run Material for MkDocs locally and preview the site as it will appear when pushed to `live`

#### Setting up a development environment for the dGC documentation site

Create a virtualenv for the python modules

* For info on setting up Pyenv see [Python setup elsewhere in the documentation](../developer/api-python.md)
* Any recent Python version will do, we tend to use >3.8
* Calling it `mkdocs` will enable Pyenv to automatically select it when you navigate to the directory.

```shell
pyenv virtualenv 3.10.2 mkdocs
```

Install Material for MKDocs some of the other dependencies.

```shell
pip install -r requirements.txt
```

Now start the MkDocs server

```shell
mkdocs serve
```

MkDocs will tell you what URL you can view the site on, this is usually `localhost:8000`. You can vary this in the settings if port 8000 is already in use.

#### Notes

* on some platforms, if you get the error `ModuleNotFoundError: No module named '_ctypes'` then you need to run `sudo apt-get install libffi-dev` or the equivalent on your platform, and then recompile your Python (if using pyenv, simply `pyenv install 3.10.2` will recompile that Python binary)

* Tested Oct 2022 on Linux Mint 21.0

## Adding a new page

* Create a new Markdown file in a subfolder in the `docs` folder. There is now also a template to get you started, in `docs/_utilities/page-template.md`, which you would copy into your new page file.

!!! info
    Because of the way we have set up the left sidebar navigation, new pages are **not** automatically added to the navigation.
    
    (This allows us to have pages which are work-in-progress, available on the live site for review, but not in the navigation, hence only those who have the link would easily find it)
    
    See the next section for how to add pages to the navigation.

### Adding navigation for the page

Add navigation by editing the `nav:` tree element in `mkdocs.yml`. Below is an excerpt from the `nav:` in this project. You can see how the top level Navbar headings Home and About are defined, and how the sidebar headings work. You can nest several levels deep if needed. 

``` yaml
nav:
  - Home: 'index.md'
  - About:
    - 'about/about.md'
    - 'about/overview.md'
```

By manually specifying the navigation in this way, we have control over the precise appearance of subfolder names (which otherwise are rendered in Title Case, but this doesn't work for acronyms) and also we can customise the order of listing of the sidebar headings, which otherwise are simply alphabetically ordered.

### Page title in the navigation

The page title that will be displayed in the left sidebar navigation is set in the YAML front matter:

``` yaml hl_lines="2"
---
title: Some Page Title
reviewers: Dr Reviewer
---
```

### Heading on the page

The heading that will be displayed on the page is set using the first `<h1>` heading (ie one hash `#`)

``` markdown
# Heading, which can be different to the sidebar title
```

### Reviewers

Reviewers are encouraged to add their details to the `reviewers:` section of the YAML front matter, this enables us to evidence that each page has been reviewed by multiple members of the team.

``` yaml
---
title: Some Page Title
reviewers: Dr Marcus Baw, Dr Simon Chapman, Other Reviewer ...
---
```

## Publishing is taken care of, for you

When you push new docs up to the `live` branch on the GitHub remote, a [GitHub Action](https://docs.github.com/en/actions/learn-github-actions) will run automatically which build the static site (takes about 30 seconds) and pushes it to the `gh-pages` branch. So you don't need to do the `mkdocs build` or `mkdocs gh-deploy --force` commands manually, it's done for you.

## Plugins

MkDocs has [many plugins available](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins), some of which we are already using to extend the capabilities of MarkDown and make the documentation look nicer and function better.
