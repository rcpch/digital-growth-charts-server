---
title: Getting API keys
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# Getting your dGC API keys

Following on from [Getting Started](../integrator/getting-started.md), in which we signed up for the platform and created an application, now let's get an API key and start making queries to the API.

## API keys

We will need an API key in order to authenticate that calls made to the API are valid. The API key is what allows us to validate that calls are genuine, and that you have enough **quota** (number of allowed calls per unit time, eg 250 calls per month) and you are not exceeding the **rate limit** (again, number of calls per unit time but over a shorter period, eg a maximum of X calls per hour).

!!! danger "API keys are secrets!"
    API keys identify you to the API, so they should be considered to be 'secrets' - this means that if someone else can access and use your API keys then they **are** effectively 'you' as far as our servers are concerned. Hence you need to take care not to disclose the API keys, especially later on when you use the keys in a real application.

    The commonest cause of accidental API key exposure is inadvertently committing a hard-coded API key to version control such as Git and then pushing it to a public site such as GitHub.
    
    Many stategies are available to help you avoid this, one of the most common being to put 'secrets' in Environment Variables and use a `[dotenv](https://medium.com/@thejasonfile/using-dotenv-package-to-create-environment-variables-33da4ac4ea8f)` tool to manage them. (I've linked to a tutorial on the node/javascript version of `dotenv` but it is available in many other languages too)

## Obtaining API keys in the developer platform

1. Click on the 'Account' menu item to see your develop account.

1. You can see the details of each of the Applications you have created.

1. Click on the 'Show/Hide' link to reveal the actual API key code.

1. Copy this API key to the clipboard (Select it all with the mouse and then press ++ctrl+c++ )

![getting-api-keys](../_assets/_images/getting-api-keys.png)

-----

## Next: [Making an API call](../integrator/making-api-calls.md)