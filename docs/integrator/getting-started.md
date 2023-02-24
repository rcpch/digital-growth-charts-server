---
title: Getting Started
reviewers: Dr Marcus Baw, Dr Anchit Chandran
---
# Getting Started integrating Digital Growth Charts

The RCPCH Digital Growth Charts platform centres around a REST API which provides calculated growth parameters derived from supplied child measurements such as height and weight.

The next few pages will take you through the process of using the API. If you are an experienced user of REST APIs, this should be straightforward. We have deliberately designed this API to be simple and clear.

## Sign up for the API service

To use the Digital Growth Charts API, you need to sign up for an account and obtain **API keys**.

These API keys allow us to manage usage of the API and prevent abuse. For exploring the platform, the Free Tier gives instant access. More information on pricing is available [here](../products/pricing.md).

> At present this sign-up step is on an external website because we use the Microsoft Azure API management platform. In the future, this may become a more streamlined on-boarding workflow.

[Go to dev.rcpch.ac.uk to sign up :octicons-link-external-16:](https://dev.rcpch.ac.uk/signup){ .md-button .md-button--primary}

**Once signed up, come back here to follow the rest of the Getting Started tutorial.**
## Choose a Product and Create an App

!!! tip "Onboarding support"
    If you have any issues with getting the Tier you need, please [contact us](../about/contact.md).

1. Navigate to the [Products](https://dev.rcpch.ac.uk/product) menu item, and choose the Tier of the API subscription that you require.

    !!! warning "**IMPORTANT: ONLY THE FREE TIER GIVES YOU INSTANT ACCESS**"
        Other tiers require waiting for **approval**, onboarding, and payment verification. Initially, we recommend the **Free Tier** for everyone. You can create multiple Free Tier apps, however, the usage is shared.

2. Select a Tier from the 'Tiers' drop-down to get started.

3. Create a unique name for your application. It doesn't matter what you call it as long as it has meaning for you, and it can be changed later in the Account part of the portal.

4. Click 'Subscribe' to create the app.

![create-an-app](../_assets/_images/create-an-app.png)

!!! tip "Improving these docs"
    We're always looking for feedback on our documentation, so that we maintain clear, unambiguous guides for all parts of the platform. If something isn't clear please let us know, by [talking about it on our forums](https://openhealthhub.org/c/rcpch-digital-growth-charts), or creating an [issue on GitHub](https://github.com/rcpch/digital-growth-charts-documentation/issues). Please include enough description of the problem so we can fix it. Screenshots and links are super helpful for this.

    You can also directly edit the docs and submit changes back to us for inclusion: click on the :material-pencil: button in the top left of any main text pane, which will take you to the source on GitHub. You will need to make your own GitHub fork of the documentation. Make your changes there and submit a pull request back to us. See [Contributing](../developer/contributing.md) for more info.

-----

## Next: [Getting API keys](../integrator/api-keys.md)