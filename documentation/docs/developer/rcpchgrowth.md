---
title: RCPCHGrowth library
reviewers: Dr Simon Chapman, Dr Anchit Chandran
audience: developers
---

## Overview

The centile and SDS calculations are performed in our separate [RCPCHGrowth Python package](https://pypi.org/project/rcpchgrowth/).

As we developed the Digital Growth Charts codebase, we felt it was necessary to extract the centile calculation code into a separate package for easier reuse elsewhere.

### Background

There have been several packages that calculate centiles.

The most influential software in growth, produced by *Huiqi Pan* and *Tim Cole*, was an add-in for Microsoft Excel, called **LMSGrowth**. It is still freely [downloadable](https://www.healthforallchildren.com/shop-base/shop/software/lmsgrowth/) and contains the reference tables as `.xls`.

The name, *RCPCHGrowth*, was chosen as it is intended to supersede LMSGrowth.

RCPCHGrowth has been primarily built to work with the UK-WHO dataset. LMS calculations can theoretically work with any LMS data table. In practice, each data table has its own idiosyncrasies and is hard to standardise. In time, it is hoped the most mature and stable references can be included.

### Growth Reference data

The references included are:

1. UK90 dataset – runs from 23 weeks to 20 years
2. WHO 2006 – runs from 2 weeks to 4 years
3. Down reference
4. Turner reference

Data tables are stored in the ```data_tables``` folder as ```.json```. There is a separate [repository](https://github.com/rcpch/growth-references) to store references from across the world. Currently, they are stored as ```.csv```, ```.json``` and ```.rif``` file types.

*`.rif` is a standardised format created by @stefvanbuuren.*

### Package Structure

#### Constants

Constants have been created for measurement, references and validation. All are stored in the ```constants``` folder. All string constants are lower case. All number constants are upper case.

### Measurement Class

#### Required parameters

The core class of RCPCHGrowth is `Measurement`.

The following parameters are **required** for `Measurement` on initialisation:

```python
birth_date: datetime.date

observation_date: datetime.date

sex: ['male', 'female']

measurement_method: ['height', 'weight', 'bmi', 'ofc']

observation_value: float

reference: ['uk-who', 'trisomy-21' 'turners-syndrome']
```

#### Optional parameters

The following **optional parameters** default to `None` if not provided:

```python
bone_age: float

bone_age_centile: float

bone_age_sds: float

bone_age_text: str

bone_age_type ["greulich-pyle", 'tanner-whitehouse-ii', 'tanner-whitehouse-iii', 'fels']

events_text: list of str
```

`bone_age`, `bone_age_centile`, `bone_age_sds`

- No formatting is performed. Returned in the `Measurement` Class as provided. The chart plugin is optimised to recognise them.

```bone_age_text```

- Contextual information to describe the bone age. It may be a radiology report or author comment.

```events_text```

- List of `str`ings
- Events to tag the measurement with: e.g. starting a treatment or receiving a diagnosis.

### The Measurement Object

The `Measurement.measurement` attribute will return a full `Measurement` object.

The `Measurement` Class calls private methods and other package functions to perform calculations, leading to the construction of the `Measurement` object.

The `Measurement` object is returned to the user as `json` in the following example structure:

```json
{
    "birth_data": {
        "birth_date": "2020-04-12",
        "gestation_weeks": 40,
        "gestation_days": 0,
        "estimated_date_delivery": "2020-04-12",
        "estimated_date_delivery_string": "Sun 12 April, 2020",
        "sex": "female"
    },
    "measurement_dates": {
        "observation_date": "2028-06-12",
        "chronological_decimal_age": 8.167008898015059,
        "corrected_decimal_age": 8.167008898015059,
        "chronological_calendar_age": "8 years and 2 months",
        "corrected_calendar_age": "8 years and 2 months",
        "corrected_gestational_age": {
            "corrected_gestation_weeks": null,
            "corrected_gestation_days": null
        },
        "comments": {
            "clinician_corrected_decimal_age_comment": "Born at term. No correction has been made for gestation.",
            "lay_corrected_decimal_age_comment": "Your baby was born on their due date.",
            "clinician_chronological_decimal_age_comment": "Born Term. No correction has been made for gestation.",
            "lay_chronological_decimal_age_comment": "Your baby was born on their due date."
        },
        "corrected_decimal_age_error": null,
        "chronological_decimal_age_error": null
    },
    "child_observation_value": {
        "measurement_method": "height",
        "observation_value": 115.0,
        "observation_value_error": null
    },
    "measurement_calculated_values": {
        "corrected_sds": -2.406593606646068,
        "corrected_centile": 0.8,
        "corrected_centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
        "chronological_sds": -2.406593606646068,
        "chronological_centile": 0.8,
        "chronological_centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
        "corrected_measurement_error": null,
        "chronological_measurement_error": null,
        "corrected_percentage_median_bmi": null,
        "chronological_percentage_median_bmi": null
    },
    "plottable_data": {
        "centile_data": {
            "chronological_decimal_age_data": {
                "x": 8.167008898015059,
                "y": 115.0,
                "b": 10.0,
                "events_text": [
                    "Growth hormone start",
                    "Growth Hormone Deficiency diagnosis"
                ],
                "bone_age_label": "This bone age is advanced",
                "bone_age_type": "greulich-pyle",
                "bone_age_sds": 2.0,
                "bone_age_centile": 98.0,
                "observation_error": null,
                "age_type": "chronological_age",
                "calendar_age": "8 years and 2 months",
                "lay_comment": "Your baby was born on their due date.",
                "clinician_comment": "Born Term. No correction has been made for gestation.",
                "age_error": null,
                "centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
                "observation_value_error": null
            },
            "corrected_decimal_age_data": {
                "x": 8.167008898015059,
                "y": 115.0,
                "b": 10.0,
                "events_text": [
                    "Growth hormone start",
                    "Growth Hormone Deficiency diagnosis"
                ],
                "bone_age_label": "This bone age is advanced",
                "bone_age_type": "greulich-pyle",
                "bone_age_sds": 2.0,
                "bone_age_centile": 98.0,
                "observation_error": null,
                "age_type": "corrected_age",
                "corrected_gestational_age": "",
                "calendar_age": "8 years and 2 months",
                "lay_comment": "Your baby was born on their due date.",
                "clinician_comment": "Born at term. No correction has been made for gestation.",
                "age_error": null,
                "centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
                "observation_value_error": null
            }
        },
        "sds_data": {
            "chronological_decimal_age_data": {
                "x": 8.167008898015059,
                "y": -2.406593606646068,
                "b": 10.0,
                "events_text": [
                    "Growth hormone start",
                    "Growth Hormone Deficiency diagnosis"
                ],
                "bone_age_label": "This bone age is advanced",
                "bone_age_type": "greulich-pyle",
                "bone_age_sds": 2.0,
                "bone_age_centile": 98.0,
                "age_type": "chronological_age",
                "calendar_age": "8 years and 2 months",
                "lay_comment": "Your baby was born on their due date.",
                "clinician_comment": "Born Term. No correction has been made for gestation.",
                "age_error": null,
                "centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
                "observation_value_error": null
            },
            "corrected_decimal_age_data": {
                "x": 8.167008898015059,
                "y": -2.406593606646068,
                "b": 10.0,
                "events_text": [
                    "Growth hormone start",
                    "Growth Hormone Deficiency diagnosis"
                ],
                "bone_age_label": "This bone age is advanced",
                "bone_age_type": "greulich-pyle",
                "bone_age_sds": 2.0,
                "bone_age_centile": 98.0,
                "age_type": "corrected_age",
                "corrected_gestational_age": "",
                "calendar_age": "8 years and 2 months",
                "lay_comment": "Your baby was born on their due date.",
                "clinician_comment": "Born at term. No correction has been made for gestation.",
                "age_error": null,
                "centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
                "observation_value_error": null
            }
        }
    },
    "bone_age": {
        "bone_age": 10.0,
        "bone_age_type": "greulich-pyle",
        "bone_age_sds": 2.0,
        "bone_age_centile": 98.0,
        "bone_age_text": "This bone age is advanced"
    },
    "events_data": {
        "events_text": [
            "Growth hormone start",
            "Growth Hormone Deficiency diagnosis"
        ]
    }
}
```

### Global Functions

#### Date Functions

There are **two** relevant date calculations:

1. ```corrected_decimal_age```: takes into account gestational age at birth
2. ```chronological_decimal_age```: does *not* take into account gestational age at birth

Note that age correction now occurs across the life course, even when term. Age correction is discontinued at *42 weeks* gestation.

Decimal age is calculated by calculating the difference in days between the two dates using the `dateutil` package, then dividing this by `365.25` (as every fourth year is a leap year).

Ages can be calculated as decimal ages, or calendar ages which are returned as a string. Advice relating to age correction is also returned as a string from functions in ```growth_interpretations.py```.

#### LMS Calculations

The primary calculation is to generate a z-score (SDS) from two dates, sex, measurement method, and observation value, comparing against a reference, detailed in [How the UK-WHO Charts Work](/clinician/chart-information-health-staff/#how-the-uk-who-charts-work).

Each reference comprises an L, M and S value for a decimal age. The decimal ages in the reference data are not separated at uniform intervals. Depending on age, intervals are weeks, months or years apart.

The calculation involves first calculating a decimal age (corrected or chronological), then using this to look up the nearest L, M and S values. If there is no exact match, the intermediate L, M, and S values are calculated using *cubic interpolation* (if there are 2 values either side of the decimal age requested in the reference data) or *linear interpolation* (if the age falls at the extremes of a given reference and there is therefore only one value above or below the age provided). The resulting L, M and S values are put into the equation to generate an *SDS*, which is used to generate a centile.

This latter calculation is done using the SciPy package.

##### Steps

The functions called by the Measurement class are ```sds_for_measurement```, or its inverse ```measurement_from_sds```, found in the ```global_functions.py``` file.

The correct reference is selected based on the parameter passed in from the user in the function ```lms_value_array_for_measurement_for_reference```.

From this, the individual L, M and S values are returned using the ```fetch_LMS``` function. This function finds the lowest nearest decimal age in the LMS list (```nearest_lowest_index```), and if there is a match, the L, M and S are returned. If there is no match, interpolation is performed, depending on how many values are present below and above that value in the list. If there are 2 values, ```cubic_interpolation``` can be performed, otherwise ```linear_interpolation``` can be performed.

Note that our cubic interpolation method is subtly different from those in the SciPy and NumPy packages. The code using these functions remains and has been commented out. We found the library functions to be slower and less precise.

The L, M and S are then converted to SDS using the ```lms_to_z``` and either returned, or converted to centile using the ```centile``` function and then returned.

##### Reference Selection

As there are several references, the selection of the correct LMS table is essential before beginning calculation. The references are all stored as JSON files in the ```data_tables``` folder. There are individual files (```uk_who.py```, ```turner.py``` and ```trisomy_21.py```) which select the correct tables and contain error handling, particularly to return meaningful errors to users. For example, weight and head circumference but not length data are available at 23 and 24 weeks gestation. Head circumference in girls stops at 17 years but in boys it stops at 18 years. To handle all these idiosyncrasies, an individual file for table selection has been created.

##### Centile Advice Strings

There was much discussion about these at project board. Found in ```centile_bands.py```, these strings are returned in the `Measurement` object to guide users on interpretation of the centile values they receive. The Project Board were very clear they wished to dissuade users from quoting exact centile values, instead to refer to ranges. Further details can be found in the clinician information. Although the `Measurement` object returns an exact centile value, the advice strings are better suited for reporting to users and are rendered in tooltips in the Typescript RCPCHGrowth Chart Component package.

#### Chart Functions

These are for the creation of plottable centile charts.

```chart_functions.py``` contains a ```create_chart``` function which accepts a reference as a parameter and returns a large object with plottable values to render a centile chart, and a label for each centile series.

For the UK-WHO references, there are 4 `json` objects generated, with the following structure:

```shell
uk90_preterm: {
  male: {
      height: [
          {
              sds: -2.667,
              centile: 0.4,
              data: [{l: , x: , y: }, ...]
          }
      ],
      weight: [...]
  },
  female: {...}
}
uk_who_infant: {...}
uk_who_child:{...}
uk90_child: {...}
```

Each centile is created using the ```generate_centile``` function found in ```global_functions```. This creates plottable x and y coordinates (x is decimal age in years, y is the measurement, l is the centile label) at regular time intervals, usually weekly to the age of 2y, and monthly thereafter. This could be more granular, but at the cost of a much bigger object, which is more than 1MB, even when minified.

There is an endpoint in the API which calls this function and returns the chart for those users who need it. Equally, the Typescript Charting Component (built for React) has the reference data included.

```create_plottable_child_data```, largely deprecated now, receives a list of Measurement objects and returns a `PlottableChild` object. Earlier versions of the API required 2 API calls - one to make the calculations, one to convert those to a plottable format. This has now been moved into the Measurement object so is only used with older versions of the API.

### Other functions

There are more experimental functions in ```dynamic_growth.py``` which calculate height velocity and acceleration from a list of Measurement objects, and some implementations of thrive lines based using correlation tables in the ```data_tables``` folder. These features still have significant work and testing required - contributions are welcome.
