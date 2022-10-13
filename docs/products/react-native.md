---
title: React Native Client
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# React Native Client (experimental, pre-alpha)

{% set repository_name="rcpch/digital-growth-charts-react-native-client" -%}

[![Github Issues](https://img.shields.io/github/issues/{{ repository_name }})](https://github.com/{{ repository_name }}/issues)
[![Github Stars](https://img.shields.io/github/stars/{{ repository_name }})](https://github.com/{{ repository_name }}/stargazers)
[![Github Forks](https://img.shields.io/github/forks/{{ repository_name }})](https://github.com/{{ repository_name }}/network/members)
[![Github Licence](https://img.shields.io/github/license/{{ repository_name }})](https://github.com/{{repository_name }}/blob/live/LICENSE)

:octicons-mark-github-16: [Github repository](https://github.com/{{ repository_name }})

<!-- :material-web: (link to follow) -->

<!-- ![image](image) -->

This is a modern dGC client for mobile, written in React Native by Dr Charles van Lennep. React Native is a cross platform native app development platform, and can therefore run on Android or iOS.

The need for a separate React Native codebase for mobile is to optimise the viewport for a mobile device display, and enable touch-dependent features such as scrolling, zooming, and selecting tooltips to work properly.

It uses the same [React Chart Component Library](../products/react-component.md) code for its charting.

We are hoping to be able to develop the React Native client into a useful RCPCH-approved clinical digital multi-tool, containing other calculations used every day in clinical practice, and backed by future APIs.
