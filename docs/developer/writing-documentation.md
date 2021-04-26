---
title: Writing Documentation
reviewers: Dr Marcus Baw
---

# Writing dGC Documentation

Where possible we have tried to bring together all documentation relating to any aspect of the project into this one MkDocs site.

## MkDocs

The documentation for the dGC project is created using the MkDocs documentation framework, and uses the theme 'Material for MkDocs'.

There is (as you'd expect) some delightful documentation for it at
<https://squidfunk.github.io/mkdocs-material/>, and for the underlying MkDocs framework <https://www.mkdocs.org/>.

## Adding or editing documentation

Mostly this just requires creating MarkDown files in the `docs/` directory of the <https://github.com/rcpch/digital-growth-charts-documentation> repository.

Use other pages within this repo to get ideas on the style and the features available such as emoji, icons, admonitions, etc.

### Adding a page

Create a new Markdown file in a subfolder in the `docs` folder.
MkDocs automatically adds it to the site. See below for how to customise its exact appearance in the Navbar

### Adding navigation for the page

Add navigation by editing the `nav:` element in `mkdocs.yml`. Below is an excerpt from the `nav:` in this project. You can see how the top level Navbar headings Home and About are defined, and how the sidebar headings work. You can nest several levels deep if needed.

``` yaml
nav:
  - Home: 'index.md'
  - About:
    - 'about/about.md'
    - 'about/overview.md'
```

By manually specifying the navigation in this way, we have control over the precise appearance of subfolder names (which otherwise are rendered in Title Case, but this doesn't work for acronyms) and also the order of display of the sidebar headings.

### Page title in the navigation

The page title taht will be displayed in the sidebar is set in the YAML front matter:

``` yaml
---
title: Some Page Title
---
```

### Heading on the page

The heading that will be displayed on the page is set using the first `<h1>` heading (ie one hash `#`)

``` markdown
# Heading, which can be different to the sidebar title
```

### Reviewers

Reviewers are encouraged to add their details to the `reviewers:` section of the YAML front matter:

``` yaml
---
title: Some Page Title
reviewers: Dr Marcus Baw, Dr Simon Chapman, Other Reviewer ...
---
```

## Publishing

When you push new docs to the `live` branch, a [GitHub Action](https://docs.github.com/en/actions/learn-github-actions) will run automatically which build the static site (takes about 30 seconds) and pushes it to the `gh-pages` branch. So you don't need to do the `mkdocs build` or `mkdocs gh-deploy --force` commands manually, it's done for you.

## Plugins

MkDocs has many plugins available <https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins>, some of which we are already using to extend the capabilities of MarkDown and make the documentation look nicer and function better.
