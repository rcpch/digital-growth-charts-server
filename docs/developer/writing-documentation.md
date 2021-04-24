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

## Reviewers

Reviewers are encouraged to add their details to the `reviewers:` section of the YAML front matter:

``` yaml
---
title: Some Page
reviewers: Dr Marcus Baw, Dr Simon Chapman, Other Reviewer ...
```

## Publishing

When you push new docs to the `alpha` branch, a [GitHub Action](https://docs.github.com/en/actions/learn-github-actions) will run automatically which build the static site (takes about 30 seconds) and pushes it to the `gh-pages` branch. So you don't need to do the `mkdocs build` or `mkdocs gh-deploy --force` commands.

## Plugins

MkDocs has many plugins available <https://github.com/mkdocs/mkdocs/wiki/MkDocs-Plugins>, some of which we are already using to extend the capabilities of MarkDown and make the documentation look nicer and function better.



