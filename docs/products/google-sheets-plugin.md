---
title: Google Sheets extension
reviewers: Dr Marcus Baw
---

# Google Sheets Plugin

:octicons-mark-github-16: 
:material-web:

To make accurate centile calculation accessible to researchers, hobbyists and enthusiasts, a Google Sheets extension has been developed using [Google Apps Script](https://developers.google.com/apps-script/guides/sheets), which makes API calls for up to 1000 data points.

## Format

Columns must be in the order and labelled in lower case

| birth_date | observation_date | gestation_weeks | gestation_days | sex | observation_value |
|------------|------------------|-----------------|----------------|-----|-------------------|
|            |                  |                 |                |     |                   |

Dates must be supplied in the format YYYY-MM-DD
sex is lowercase 'male' or 'female'
Currently only UK-WHO is supported but in time Trisomy 21 and Turner's will be added.

## Installation