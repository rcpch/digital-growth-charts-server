# CALCULATIONS FOR GROWTH CHARTS USING UK-WHO GROWTH REFERENCES

##Usage

All responses will have the form

```json
{
    "data": "mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

### Calculate static SDS and Centile values for child anthropometric measurements

**Definition**

`POST /calculate`

**Arguments**
# Naming base on PEP 8 standards
- `"birth_date": date` date as datetimestamp (mandatory)
- `"observation_date": date` date as datetimestamp (mandatory)
- `"sex": string` MALE or FEMALE or UNCLASSIFIED or INDETERMINATE (mandatory)
- `"gestation_weeks": int` length of pregnancy in weeks (optional)
- `"gestation_days": int` days additional to length of pregnancy in weeks (optional)
- `"gestation_total_days": int` length of pregnancy in days from conception (optional)
- `"observation_type": string` HEIGHT / WEIGHT / OFC / BMI (/ SKIN_FOLDS / PEFR) lower case (mandatory)
- `"observation_units": string` CM / M / G / KGM2 / CM3SEC (mandatory)
- `"observation: decimal"` observation to 2 dp (mandatory)

**Questions**
 - `scope of measurements` do we offer BP?

-`201 Created` on success
```json
{
    "dates": {
            "birth_date": '02/05/2009',
            "obs_date": '03/01/2011',
            "gestation_weeks": 40,
            "gestation_days": 0,
            "chronological_decimal_age": 1.62,
            "chronological_calendar_age": "one year, 8 months and 2 days",
            "corrected_decimal_age": 3.52,
            "corrected_calendar_age": "three years, 6 months and 2 days",
            "clinician_comment": "This is an age which has been corrected for prematurity.",
            "lay_comment": "This takes into account your child's prematurity"
    },
    "patient": {
        "height": 76.0,
        "weight": 8.2,
        "bmi": 15.3,
        "ofc": 43.1
    },
    "measurements": {
            "height_sds": 1.20,
            "height_centile": 85.34,
            "clinician_height_commment": "This is in the top 15%. Serial data needed for comparison",
            "lay_height_comment": "Your child is tall for their age but in the normal range",
            "weight_sds":  1.30,
            "weight_centile": 88.21,
            "clinician_height_commment": "This is in the top 15%. Serial data needed for comparison",
            "lay_height_comment": "Your child has a higher weight for their age than average but is in the normal range",
            "ofc_sds":  0.50,
            "ofc_centile": 67.50,
            "clinician_ofc_commment": "This is average. Serial data essential for comparison.",
            "lay_ofc_comment": "Your child's head circumference is in the normal range. It is important to compare measurements over time.",
    }
}
```

- `"decimal_age_in_years": decimal` age to 3 d.p. calculated as the difference in days between date of birth at 00:00 and date of observation at 00:00 divided by 365.25 (to account for leap years every 4 years)
- `"chronological_calendar_age": string` human readable representation of age in years, months, weeks, days or hours
- `"corrected"`
