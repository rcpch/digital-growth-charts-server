# Google Sheets Plugin (stable)

To make accurate centile calculation accessible to researchers, hobbyists and enthusiasts, a google sheets plugin has been developed which makes API calls for up to 1000 data points.

## Format

Columns must be in the order and labelled in lower case

| birth_date | observation_date | gestation_weeks | gestation_days | sex | observation_value |
|------------|------------------|-----------------|----------------|-----|-------------------|
|            |                  |                 |                |     |                   |

Dates must be supplied in the format YYYY-MM-DD
sex is lowercase 'male' or 'female'
Currently only UK-WHO is supported but in time Trisomy 21 and Turner's will be added.