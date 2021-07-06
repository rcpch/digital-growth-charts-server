---
title: Writing Documentation
reviewers: Dr Marcus Baw
---

# Writing dGC Documentation

Where possible we have tried to bring together **all** documentation relating to any aspect of the project into this one MkDocs site, which is published at [growth.rcpch.ac.uk](https://growth.rcpch.ac.uk)

## MkDocs

The documentation for the dGC project is created using the MkDocs documentation framework, and uses the theme 'Material for MkDocs', which adds a number of extra features and an more modern appearance than plain MkDocs.

There is (as you'd expect) some delightful documentation for it: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), and for the underlying [MkDocs](https://www.mkdocs.org/) which it's built on. You may need to refer to both at times, for different features.

## Adding or editing documentation

Mostly this just requires creating MarkDown files in the `docs/` directory of the [documentation repository](https://github.com/rcpch/digital-growth-charts-documentation).

If you are new to this, you can use GitHub's interface itself to edit online, by clicking the 'pencil' edit icon in the top right corner of any source code page. There are also external tools like [Prose.io](http://prose.io/) which give you a nice interface for editing MarkDown online, and will sync the changes ith GitHub for you.

More experienced coders can `git clone` the repo and make changes offline on their local machine before pushing to the remote (either the `rcpch` organisation's remote, or their own fork)

Use other pages within this repo to get ideas on the style and the features available such as [emoji](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#emoji), [icons](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/#using-icons), [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/), etc.

### Adding a page

* Create a new Markdown file in a subfolder in the `docs` folder. There is now also a template to get you started, in `docs/utilities/page-template.md`, which you would copy into your new page file.

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

By manually specifying the navigation in this way, we have control over the precise appearance of subfolder names (which otherwise are rendered in Title Case, but this doesn't work for acronyms) and also the order of display of the sidebar headings.

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
