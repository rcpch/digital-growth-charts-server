---
title: Writing Documentation
reviewers: Dr Marcus Baw, Dr Anchit Chandran
---

# Writing dGC Documentation

Where possible, we have tried to bring together **all** documentation relating to any aspect of the project into this one MkDocs site, published at [growth.rcpch.ac.uk](https://growth.rcpch.ac.uk)

## Material for MkDocs

The documentation for the Digital Growth Charts project is created using the MkDocs documentation framework. It uses the '*Material for MkDocs*' theme, which adds a number of extra features and a more modern appearance. We use the *Material for MkDocs Insiders* edition, allowing us to support the project, whilst getting a few neat early-access features.

As you’d expect, there is delightful documentation for both projects: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), and for the underlying [MkDocs](https://www.mkdocs.org/), on which it’s built. At times, you may need to refer to both for different features.

## Adding or editing documentation

Mostly this just requires creating Markdown files in the `docs/` directory of the [documentation repository](https://github.com/rcpch/digital-growth-charts-documentation).

Use other pages within this repo to get ideas on the style and the features available such as [emoji](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#emoji), [icons](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#using-icons), [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/).

### Continuous Integration via GitHub Actions

Any changes to the `live` branch of the documentation repository trigger a [GitHub Action](https://github.com/rcpch/digital-growth-charts-documentation/blob/live/.github/workflows/build-and-deploy-to-gh-pages-and-azure.yml). This runs Material for MkDocs in a temporary application container, builds the site from the Markdown source into a set of static HTML pages, and [publishes the site to Azure](https://growth.rcpch.ac.uk/), with a [backup in GitHub Pages](https://rcpch.github.io/digital-growth-charts-documentation/).

This occurs whether changes are made using online or local, offline editing methods.

!!! note "GitHub Branch Protection"

    Ensure you make Pull Requests to `prerelease`, or any other branch name of your choosing, but not `live`.

    We have enabled GitHub branch protection to `live` so changes cannot be made directly there but **must** be made through an intermediate branch, and then Pull Requested into `live`.

### Online editing of the Markdown

If you are new to Markdown editing, you can use GitHub's interface itself to edit online, by clicking the 'pencil' edit icon in the top right corner of any source code page. There are also external tools like [Prose.io](http://prose.io/) and [StackEdit](https://stackedit.io/) which give you a nice interface for editing MarkDown online, and will sync the changes with GitHub for you.

If you need help getting set up, [contact us in the Signal chat](../about/contact.md).

### Using a text editor and editing locally

More experienced coders can `git clone` the repo and make changes offline on their local machine before pushing to the remote to either the `rcpch` organisation's remote, or their own fork. This allows you to run Material for MkDocs locally and preview the site as it will appear when pushed to `live`.

#### (Mac / Linux) Setting up a development environment for the dGC documentation site

Create a virtualenv for the Python modules:

* For info on setting up Pyenv see [Python setup](../developer/api-python.md)
* Any recent Python version works, we tend to use 3.11
* Calling it `mkdocs-3.11` will enable Pyenv to automatically select it when you navigate to the directory, because this will match the contents of the `.python-version` file in the root of the project.

```console
pyenv virtualenv 3.11 mkdocs-3.11
```

!!! info "MkDocs **Insiders** Edition"

    This project uses Material for MkDocs **Insiders** Edition. To install this, you will need a GitHub token which is available (for RCPCH team only) from Marcus Baw (pacharanero). If you have the token, you can manually run the following command to install Insiders. If you can't access the token, see the comments in the `requirements.txt` file.

```console
pip install git+https://<INSERT_GH_TOKEN_HERE>@github.com/squidfunk/mkdocs-material-insiders.git
pip install -r requirements.txt
```

Start the MkDocs server:

```console
mkdocs serve
```

MkDocs will tell you what URL you can view the site on, which is usually `localhost:8000`. You can vary this in the settings, if port `8000` is already in use.

#### (Windows) Setting up a development environment for the dGC documentation site

Create a virtual environment with `virtualenv`. See [Windows - install virtualenv](api-python.md#windows---installing-virtualenv) if you need help setting up.

Then, with [GitHub Desktop](https://desktop.github.com/), clone the repo using the following url

```console
https://github.com/rcpch/digital-growth-charts-documentation.git
```

`cd` into the directory (ensuring you are using your virtual environment)

```console
cd digital-growth-charts-documentation
```

Install the dependencies.

!!! info "MkDocs **Insiders** Edition"

    This project uses Material for MkDocs **Insiders** Edition. To install this, you will need a GitHub token which is available (for RCPCH team only) from Marcus Baw (pacharanero). If you have the token, you can manually run this command to install Insiders:

```console
pip install git+https://<INSERT_GH_TOKEN_HERE>@github.com/squidfunk/mkdocs-material-insiders.git
pip install -r requirements.txt
```

If you can't get access to the token, please see the comments in the `requirements.txt` file and run:

```console
pip install -r requirements.txt
```

Finally, start the MkDocs server

```console
mkdocs serve
```

MkDocs will tell you what URL you can view the site on, which is usually localhost:8000. You can vary this in the settings, if port 8000 is already in use.

#### `git-committers` and `mkdocs-with-pdf` plugins

These plugins can add 10-15 seconds of build time to the site, so when developing locally, they are disabled by default. They are enabled by using environment variables, if you want to test that they work locally before pushing to the remote:

```console
export ENABLE_GIT_COMMITTERS=true; mkdocs serve
export ENABLE_PDF_EXPORT=true; mkdocs serve
```

You should always build the site at least once with both PDF export and Git Committers enabled, to ensure there are no issues, before pushing to the remote.

#### Notes

* On some platforms, if you get the error `ModuleNotFoundError: No module named '_ctypes'`, then you need to run `sudo apt-get install libffi-dev`, or the equivalent on your platform. Then, recompile your Python (if using pyenv, simply `pyenv install 3.10.2` will recompile that Python binary).

* Tested Oct 2022 on Linux Mint 21.0

## Adding a new page

* Create a new Markdown file in a subfolder in the `docs` folder. There is now also a template to get you started, in `docs/_utilities/page-template.md`, which you would copy into your new page file.

!!! info
    Because of the way we have set up the left sidebar navigation, new pages are **not** automatically added to the navigation.

    (This allows us to have pages which are work-in-progress, available on the live site for review, but not in the navigation, hence only those who have the link would easily find it)
    
    See the next section for how to add pages to the navigation.

### Adding navigation for the page

Add navigation by editing the `nav:` tree element in `mkdocs.yml`. Below is an excerpt from the `nav:` in this project. You can see how the top level Navbar headings `Home` and About `are` defined, and how the sidebar headings work. You can nest several levels deep, if needed. 

``` yaml
nav:
  - Home: 'index.md'
  - About:
    - 'about/about.md'
    - 'about/overview.md'
```

By manually specifying the navigation in this way, we have control over the precise appearance of subfolder names (which are otherwise rendered in Title Case, but this doesn't work for acronyms). Also, we can customise the order of listing of sidebar headings, which would otherwise be ordered alphabetically.

### Page title in the navigation

The page title that will be displayed in the left sidebar navigation is set in the YAML front matter:

``` yaml hl_lines="2"
---
title: Some Page Title
reviewers: Dr Reviewer
---
```

### Heading on the page

The heading that will be displayed on the page is set using the first `<h1>` heading (i.e. one hashtag `#`)

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

## Publishing is automated

When you push new changes to ANY branch of this repo, or it you open a Pull Request, Azure will automatically build a version of the site for review. You need to visit [this Static Web App deployment resource on the Azure portal](https://portal.azure.com/#@rcpch.ac.uk/resource/subscriptions/99e313f5-79fe-4480-b867-8daf2800cf22/resourceGroups/RCPCH-Dev-API-Growth/providers/Microsoft.Web/staticSites/documentation-demo-static-site/environments) to see the URL of the deployment, as it depends on the branch name. To obtain Azure access contact Marcus Baw of the RCPCH developer team.

Therefore, you don't need to do `mkdocs build` or `mkdocs gh-deploy --force` commands manually or locally - it’s done for you if you push to branches or PRs on GitHub.

## Plugins

MkDocs has [many plugins available](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins). We already use some to extend the capabilities of MarkDown, making the documentation look nicer and function better.
