---
title: RCPCHGrowth Package
reviewers: Dr Simon Chapman
---

## Overview

The core of the calculations is performed in the RCPCHGrowth package, written in Python 3.8.3.

### Why RCPCHGrowth?

There is a history for different packages. The most influential software in growth was produced by Huiqi Pan and Tim Cole, an add-in for Microsoft Excel, called LMSGrowth. It is still freely [downloadable](https://www.healthforallchildren.com/shop-base/shop/software/lmsgrowth/) and contains the reference tables as .xls. RCPCHGrowth is intended to supercede LMSGrowth and so the name has been chosen.

RCPCHGrowth has been primarily built to work with the UK-WHO dataset, but the LMS calculations can in principle with any LMS data table. In practice, each data table has its own idiosyncracies and is hard to standardise but it is hoped in time that most big references can be included.

### References

The references included are:

1. UK90 dataset - this runs from 23 weeks to 20 years
2. WHO 2006 - this runs from 2 weeks to 4 years
3. Down reference
4. Turner reference

Data tables are stored in the ```data_tables``` folder. They are stored as ```.json```.
There is a separate [repository](https://github.com/rcpch/growth-references) to store references from across the world. Currently they are stored as ```.csv```, ```.json``` and ```.rif``` file types, the latter a standardised format created by @stefvanbuuren.

### Package Structure

#### Constants

Constants have been created for measurement, references and validation.
All are stored in the ```constants``` folder.
All string constants are lower case.
All number constants are stored as upper case.

### Measurement Class

The core class of RCPCHGrowth is the Measurement class. It is initialised with:

```python
birth_date

observation_date

sex ['male', 'female']

measurement_method ['height', 'weight', 'bmi', 'ofc']

observation_value

reference ['ukwho', 'trisomy-21' 'turners-syndrome']
```

The dates are python dates

Calling ```Measurement(...).measurement``` will return a full Measurement object.

The Measurement class calls private methods, which in turn call functions within the package to perform the calculations and construct the Measurement object which is returned to the user as a json object.

### The Measurement Object

This is the return object from the Measurement class. It is made of the following elements:

```json
{
    "birth_data": {
        "birth_date": "Thu, 12 Mar 2020 00:00:00 GMT",
        "estimated_date_delivery": "Thu, 13 Feb 2020 00:00:00 GMT",
        "estimated_date_delivery_string": "Thu 13 February, 2020",
        "gestation_days": 0,
        "gestation_weeks": 44,
        "sex": "male"
    },
    "child_observation_value": {
        "measurement_method": "height",
        "observation_value": 100.0,
        "observation_value_error": null
    },
    "measurement_calculated_values": {
        "chronological_centile": 1,
        "chronological_centile_band": "This height measurement is on or near the 2nd centile.",
        "chronological_measurement_error": null,
        "chronological_sds": -2.1174061157646373,
        "corrected_centile": 1,
        "corrected_centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
        "corrected_measurement_error": null,
        "corrected_sds": -2.2196627616343876
    },
    "measurement_dates": {
        "chronological_calendar_age": "5 years",
        "chronological_decimal_age": 4.999315537303217,
        "chronological_decimal_age_error": null,
        "comments": {
            "clinician_chronological_decimal_age_comment": "It has not been possible to calculate age this time.",
            "clinician_corrected_decimal_age_comment": "It has not been possible to calculate age this time.",
            "lay_chronological_decimal_age_comment": "It has not been possible to calculate age this time.",
            "lay_corrected_decimal_age_comment": "It has not been possible to calculate age this time."
        },
        "corrected_calendar_age": "5 years, 3 weeks and 6 days",
        "corrected_decimal_age": 5.075975359342916,
        "corrected_decimal_age_error": null,
        "corrected_gestational_age": {
            "corrected_gestation_days": null,
            "corrected_gestation_weeks": null
        },
        "observation_date": "Wed, 12 Mar 2025 00:00:00 GMT"
    },
    "plottable_data": {
        "centile_data": {
            "chronological_decimal_age_data": {
                "age_error": null,
                "age_type": "chronological_age",
                "calendar_age": "5 years",
                "centile_band": "This height measurement is on or near the 2nd centile.",
                "clinician_comment": "It has not been possible to calculate age this time.",
                "lay_comment": "It has not been possible to calculate age this time.",
                "observation_error": null,
                "observation_value_error": null,
                "x": 4.999315537303217,
                "y": 100.0
            },
            "corrected_decimal_age_data": {
                "age_error": null,
                "age_type": "corrected_age",
                "calendar_age": "5 years, 3 weeks and 6 days",
                "centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
                "clinician_comment": "It has not been possible to calculate age this time.",
                "corrected_gestational_age": "",
                "lay_comment": "It has not been possible to calculate age this time.",
                "observation_error": null,
                "observation_value_error": null,
                "x": 5.075975359342916,
                "y": 100.0
            }
        },
        "sds_data": {
            "chronological_decimal_age_data": {
                "age_error": null,
                "age_type": "chronological_age",
                "calendar_age": "5 years",
                "centile_band": "This height measurement is on or near the 2nd centile.",
                "clinician_comment": "It has not been possible to calculate age this time.",
                "lay_comment": "It has not been possible to calculate age this time.",
                "observation_value_error": null,
                "x": 4.999315537303217,
                "y": -2.1174061157646373
            },
            "corrected_decimal_age_data": {
                "age_error": null,
                "age_type": "corrected_age",
                "calendar_age": "5 years, 3 weeks and 6 days",
                "centile_band": "This height measurement is between the 0.4th and 2nd centiles.",
                "clinician_comment": "It has not been possible to calculate age this time.",
                "corrected_gestational_age": "",
                "lay_comment": "It has not been possible to calculate age this time.",
                "observation_value_error": null,
                "x": 5.075975359342916,
                "y": -2.2196627616343876
            }
        }
    }
}
```

### Global Functions

#### Date Functions

There are two relevant date calculations, one which takes into account the gestation at birth (```corrected_decimal_age```), and one which does not (```chronological_decimal_age```).

Note that age correction now occurs across the life course, even when term. Age correction is discontinued at 42 weeks gestation. Decimal age is calculated by calculating the difference in days between the two dates using the dateutil package, then dividing this by 365.25. This is because every fourth year is a leap year.

Ages can be calculated as decimal ages, or calendar ages which are returned as a string. Advice relating to age correction is also returned as a string from functions in ```growth_interpretations.py```

#### LMS Calculations

The primary calculation is to generate a z score (SDS) from two dates, a sex, measurement method and observation value, comparing with a reference. As described elsewhere, UK-WHO are made up of 2 references (formerly 3), the UK90 which spans from 23 weeks gestation to 20 y  of age. Because these data contain children who were bottle fed as well as breast fed, the breast fed cohort from the WHO 2006 cohort were deemed more accurate and replaced the UK90 for the 2 week to 4 year age groups. Because the UK90 data are nolonger used for children in this age bracket, they have been removed to create a continuous data set. This has then been broken into the preterm (up top 42 weeks), infants (under 2s), WHO children (< 4 y), UK90 children (4-20y). Where data sets overlap, there are 2 ages at the junction, one from each reference. There is a step at the junction between the data sets.

Each reference comprises an L, M and S value for a decimal age. The decimal ages in the reference data are not separated at uniform intervals - depending on age, they are weeks, months or years apart.

The calculation involves first calculating a decimal age (corrected or chronological), then using this to look up the nearest L, M and S values. If there is no exact match, the intermediate L, M, and S values are calculated using cubic interpolation (if there are 2 values either side of the decimal age requested in the reference data) or linear interpolation (if the age falls at the extremes of a given reference and there is therefore only one value above or below the age provided). The resulting L, M and S values are put into the equation to generate an SDS, which can in turn be used to generate a centile. This latter calcuation is done using the SciPy package.

##### Steps

The functions called by the Measurement class are ```sds_for_measurement``` or its inverse ```measurement_from_sds```, found in the ```global_functions.py``` file.

The correct reference is selected based on the parameter passed in from the user in the function ```lms_value_array_for_measurement_for_reference```. From this the individual L, M and S values are returned using the ```fetch_LMS``` function. This function finds the lowest nearest decimal age in the LMS list (```nearest_lowest_index```) and if there is a match, the L, M and S are returned. If there is no match, interpolation is performed, depending on how many values are present below and above that value in the list. If there are 2 values, ```cubic_interpolation``` can be performed, otherwise ```linear_interpolation``` can be performed.

Note that our cubic interpolation method is subtly different from those in the SciPy and Numpy packages. The code using these functions remains and has been commented out. The library functions we found to be slower and less precise.

The L, M and S are then converted to SDS using the ```lms_to_z``` and returned or converted to centile using the ```centile``` function and then returned.

##### Reference Selection

There are several references, and therefore selection of the correct LMS table is essential before beginning calculation. The references are all stored as JSON files in the ```data_tables``` folder. There are individual files (```uk_who.py```, ```turner.py``` and ```trisomy_21.py```) which select the correct tables and contain error handling, particularly to return meaningful errors to users. For example, weight and head circumference but not length data are available at 23 and 24 weeks gestation. Head circumference in girls stops at 17 y but in boys it stops at 18y. To handle all these idiosyncracies related to each reference, an individual file for table selection has therefore been created.

##### Centile Advice Strings

There was much discussion about these at project board. Found in ```centile_bands.py``` these strings are returned in the Measurement object to guide users on interpretation of the centile values they receive. The project board were very clear they wished to dissuade users from quoting exact centile values, instead to refer to ranges. Further details about this can be found in the clinician information. Although the Measurement object returns an exact centile value, the advice strings are better suited for reporting to users and are rendered in tooltips in the Typescript RCPCHGrowth Chart Component package.

#### Chart Functions

These are for the creation of plottable centile charts. ```chart_functions.py``` contains a ```create_chart``` function which accepts a reference as a parameter and returns a large object with plottable values to render a centile chart, and a label for each centile series. For the UK-WHO references, they form the structure:

```python
"""
    structure:
    UK_WHO generates 4 json objects, each structure as below
    uk90_preterm: {
        male: {
            height: [
                {
                    sds: -2.667,
                    centile: 0.4
                    data: [{l: , x: , y: }, ....]
                }
            ],
            weight: [...]
        },
        female {...}
    }
    uk_who_infant: {...}
    uk_who_child:{...}
    uk90_child: {...}
    """
```

Each centile is created using the ```generate_centile``` function found in ```global_functions```. This creates plottable x and y coordinates (x is decimal age in years, y is the measurement, l is the centile label) at regular time intervals, usually weekly to the age of 2y, monthly there after. It is possible of course to make it more granular, but this is at the cost of a much bigger object, which is more than 1MB even when minified.

There is an endpoint in the API which calls this function and returns the chart for those users who need it. Equally, the Typescript Charting Component (built for React) has the reference data included.

```create_plottable_child_data```, largely deprecated now, receives a list of Measurement objects and returns a PlottableChild object. Earlier versions of the API required 2 API calls - one to make the calculations, one to convert those to a plottable format. This has now been moved into the Measurement object so is only used with older versions of the API.

### Other functions

There are more experimental functions in ```dynamic_growth.py``` which calculate height velocity and acceleration from a list of Measurement objects, and some implementations of thrive lines based using correlation tables in the ```data_tables``` folder. These are features that have significant work and testing still to do and contributions are welcome.
