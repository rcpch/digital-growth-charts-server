![RCPCH Logo](https://www.rcpch.ac.uk/themes/rcpch/images/logo-desktop.svg)
# CALCULATIONS FOR GROWTH CHARTS USING UK-WHO GROWTH REFERENCES 
Marcus Baw, Simon Chapman, Tim Cole, Andy Palmer, Charlotte Weldon, Magdalena Umerska

## Clinical Aspects
### Introduction
#### The Charts
The UK-WHO 0-4 year old charts were officially launched on May 11th 2009. Any child born after that date should be plotted on a UK-WHO Growth chart.  Children born before May 11th 2009 are already plotted on British 1990 (UK90) charts and subsequent measurements must be plotted using those charts. There should be no switch over of existing children to the new UK-WHO Charts.  After age 4 we revert to using UK90 charts. The source data for these charts are included in two spreadsheets as LMS tables. Together they define the UK-WHO growth charts, containing LMS values by age.  Also included are data not yet incorporated into a paper chart - for example, head circumference beyond 2 years.  These data can be freely used without charge as long as their source is acknowledged in any publications or products using them. Users may not claim any IP rights over them, derive financial gain from supplying the data to others, seek to restrict use of the data by others or use them for the purposes of advertising or promoting other products. Notwithstanding this limited grant of rights, the original copyright notices must continue to be reproduced in any copies of these materials.

#### The UK RCPCH Growth Chart Application Program Interface (API) Project
This is the first national effort to produce validated and reliable SDS and Centile scores from UK Children's growth data. The project team was commissioned by NHS England to produce, in the first instance, an API (application program interface) to generate reliable results for growth data from children 1 y and below. The project team began work in May 2020.

### The LMS Method
It is now common practice to express child growth status in the form of SD scores. The LMS method provides a way of obtaining normalized growth centile standards which simplifies this assessment, and which deals quite generally with skewness which may be present in the distribution of the measurement (eg height, weight, circumferences or skinfolds). It assumes that the data can be normalized by using a power transformation, which stretches one tail of the distribution and shrinks the other, removing the skewness. The optimal power to obtain normality is calculated for each of a series of age groups and the trend summarized by a smooth (L) curve. Trends in the mean (M) and coefficient of variation (S) are similarly smoothed. The resulting L, M and S curves contain the information to draw any centile curve, and to convert measurements (even extreme values) into exact SD scores.

### How the LMS method is used
1.    Look up in the LMS table for the relevant measurement (height or weight etc) the age-sex-specific values of L, M and S for the child, using either linear or cubic interpolation to get the exact age.  
2.    To obtain the z-score, plug the LMS values with the child's measurement into the formula:
> ![formula](https://latex.codecogs.com/svg.latex?\=z={[(Measurement / M)-1] \over L S})
3. The algorithm for the reverse process, from z-score or centile back to measurement, is as follows: 
4.    Repeat step 1 to obtain the LMS values for the child’s measurement, age and sex. 
5.    The z-score is then converted back to a measurement with the formula:
> ![formula](https://latex.codecogs.com/svg.latex?\=Measurement= M (1+LSz)^{1/L})
6. This conversion is useful for example to obtain centiles to plot growth charts, where each centile is defined by its corresponding z-score. 

### UK Growth References
This is a growing list of growth references for children. It will continue to be added to as more data becomes available.
1. _British1990.xls_: length/height & BMI for ages -0.13 to 23 yr; 
weight -0.33 to 23 yr; head circumference -0.33 to 18 or 17 yr 
(males/females); sitting height & leg length 0 to 23 yr; waist 
circumference 3 to 17 yr.

2. *_UK_WHO_term.xls*: Average values at birth for weight, length and head circumference (not BMI) for all term births (gestations 37 to 42 weeks) computed from the UK90 reference data base.[1](#references),[2](#references)Acknowledgement statements using these data should specify the data source as: *“British 1990 reference data, reanalysed 2009”*.  This is combined with the WHO standard for weight, BMI and head circumference from 2 weeks to 4 years, for length 2 weeks to 2 years and height 2-4 years. It is shown by week to 13 weeks and then bycalendar month. They are exactly the same data as the LMS tables accessed from the [WHO website](http://www.who.int/childgrowth/standards/) except that the data from birth to 2 weeks are omitted.  Acknowledgement statements using these data should specify the data source as: *“WHO Child Growth Standards”*[3](#references), [4](#references)The British 1990 section runs from 4 to 20 years by month, and includes height, weight, BMI and head circumference (to 18/17 years in boys/girls). Acknowledgement statements using these data should specify the data source as: *“British 1990 reference”*.

2. _USCDC2000.xls_: length/height, weight &  head circumference for 
ages 0 to 19.9 yr; BMI 2 to 19.9 yr.

3. _WHO2006.xls_: length/height, weight, BMI, head circumference for 
ages 0 to 5 yr; arm circumference, subscapular skinfold, triceps 
skinfold for 0.25 to 5 yr.

4. _Spiro.xls_: FEV1, FVC, FEV1FVC & FEF2575 for ages 4 to 80 yr.

5. _LMSdata_BP.xls_: systoloc & diastolic blood pressure for ages 4 to 24 yr.

### References
1. Cole TJ, Freeman JV, Preece MA. British 1990 growth reference centiles for weight, height, body mass index and head circumference fitted by maximum penalized likelihood. Stat Med 1998;17:407-29. 
2.    Cole TJ, Freeman JV, Preece MA. 1998. British 1990 growth reference centiles for weight, height, body mass index and head circumference fitted by maximum penalized likelihood. Stat Med 17(4):407-29 
3.    WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Length/Height-for-age, Weight-for-age, Weight-for-length, Weight-for-height and Body Mass Index-for age. Methods and Development. 2006. ISBN    92 4 154693 X.  
4.    WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Head circumference-for-age, arm circumference-for-age, triceps skinfold-for-age and subscapular skinfold-for age. Methods and Development. 2007. ISBN 978 92 4 154718 5.  

## Technical Aspects
### API
The algorithms are written in Python 3.8.
Mathematical and statistical calculations are made using the [SciPy](https://www.scipy.org/) and [NumPy](https://numpy.org/) libraries.
Server middleware used is [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) and [FlaskForms](https://github.com/wtforms/wtforms/)
Frontend is provided by [Semantic UI](https://semantic-ui.com/)

### Software Licensing
The project team agree that the growth references and the algorithms that generate reliable results should all exist in the public domain. They are published here under GNU Affero GPL3 licence.

### Usage
All responses will have the form

```json
{
    "data": "mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

### Calculate static SDS and Centile values for child anthropometric measurements

#### End-points
_this section needs completing_
`POST /calculate`

#### Arguments
Naming is based on PEP 8 standards
- `"birth_date": date` date as datetimestamp (mandatory). This is of format 'DD/MM/YY' (eg 01/05/2020), without timestamp or locale
- `"observation_date": date` date as datetimestamp (mandatory). This is of format 'DD/MM/YY' (eg 01/05/2020), without timestamp or locale
- `"sex": string` MALE or FEMALE (mandatory)
- `"gestation_weeks": int` length of pregnancy in weeks (optional)
- `"gestation_days": int` days additional to length of pregnancy in weeks (optional)
- `"gestation_total_days": int` length of pregnancy in days from conception (optional)
- `"observation_type": string` HEIGHT / WEIGHT / OFC / BMI (/ SKIN_FOLDS / PEFR) lower case (mandatory)
- `"observation_units": string` CM / M / G / KGM2 / CM3SEC (mandatory)
- `"observation: float"` observation to 2 dp (mandatory)


-`201 Created` on success
```json
{
    "dates": {
            "birth_date": "02/05/2009",
            "obs_date": "03/01/2011",
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

- `"decimal_age_in_years": float` age to 3 d.p. calculated as the difference in days between date of birth at 00:00 and date of observation at 00:00 divided by 365.25 (to account for leap years every 4 years)
- `"chronological_calendar_age": string` human readable representation of age in years, months, weeks, days or hours. 
- `"corrected_decimal_age"`

#### Functions

##### Date and age calculations

***Constants***
```python
TERM_PREGNANCY_LENGTH_DAYS = 40 * 7
TERM_LOWER_THRESHOLD_LENGTH_DAYS = 37 * 7
EXTREME_PREMATURITY_THRESHOLD_LENGTH_DAYS = 32 * 7
```
##### Functions

```python
chronological_decimal_age(birth_date: date, observation_date: date) -> float
```
- Calculates a decimal age from two dates supplied as raw dates without times.
- Returns value floating point

```python
corrected_decimal_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_supplementary_days: int, pregnancy_length_days = 0)->float:
```
- Corrects for gestational age. 
- Corrects for 1 year, if gestation at birth >= 32 weeks and < 37 weeks
- Corrects for 2 years, if gestation at birth <32 weeks
- Otherwise returns decimal age without correction

```python
chronological_calendar_age(birth_date: date, observation_date: date) -> str:
```
- Returns age in years, months, weeks and days: to return a corrected calendar age user passes estimated date of delivery (EDD) instead of birth date

```python
estimated_date_delivery(birth_date: date, gestation_weeks: int, gestation_supplementary_days: int, pregnancy_length_days = 0) -> date:
```
- Returns estimated date of delivery from gestational age and birthdate

```python
corrected_gestational_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_supplementary_days: int)->str:
```
- Returns a corrected gestational age for those babies not yet 42 weeks gestation

##### SDS and Centile Calculations

##### Functions
```python
sds(age: float, measurement: str, observation: float, sex: str)->float:
```
- **This function is specific to the UK-WHO data set as this is actually a blend of UK-90 and WHO 2006 references and necessarily has duplicate values.**
- Returns a standard deviation score. 
- Parameters are: 
- a decimal age (corrected or chronological), 
- a measurement (type of observation) ['height', 'weight', 'bmi', 'ofc']
- observation (the value is standard units) [height and ofc are in cm, weight in kg bmi in kg/m2]
- sex (a standard string) ['male' or 'female']

SDS is generated by passing the interpolated L, M and S values for age through an equation.
Cubic interpolation is used for most values, but where ages of children are at the extremes of the growth reference,
linear interpolation is used instead. These are:
- 23 weeks gestation
- 42 weeks gestation or 2 weeks post term delivery - the reference data here changes from UK90 to WHO 2006
- 2 years - children at this age stop being measured lying down and are instead measured standing, leading to a small decrease
- 4 years - the reference data here changes back to UK90 data
- 20 years - the threshold of the reference data

Other considerations
- Length data is not available until 25 weeks gestation, though weight date is available from 23 weeks
- There is only BMI reference data from 2 weeks of age to aged 20y
- Head circumference reference data is available from 23 weeks gestation to 17y in girls and 18y in boys

```python
centile(z_score: float):
```
- Converts a Z Score to a p value (2-tailed) using the SciPy library, which it returns as a percentage

#### BMI functions

```python
percentage_median_bmi( age: float, actual_bmi: float, sex: str)->float:
```
- This returns a child's BMI expressed as a percentage of the median value for age and sex. It is used widely in the assessment of malnutrition particularly in children and young people with eating disorders.

```python
bmi_from_height_weight( height: float,  weight: float) -> float:
```
- Returns a BMI in kg/m2 from a height in cm and a weight in kg
- Does not depend on the age or sex of the child.

```python
weight_for_bmi_height( height: float,  bmi: float) -> float:
```
- Returns a weight from a height in cm and a BMI in kg/m2
- Does not depend on the age or sex of the child.

##### Scope
Currently the minimum viable product is to provide reliable calculations for all children in the UK under the age of 1 year for height, weight, body mass index (BMI) and head circumference ('occipitofrontal circumference' - OFC).

In addition to providing standard deviation scores (SDS) and centiles, it will also provide basic guidance for users on how to interpret the information received.

It is envisaged that once established and validated, older age groups can be included, and other growth references.

It is planned that the API will in future be able to receive longitudinal growth data of individual children as an array, with a view to making some interpretations on their growth pattern and trajectory.

It separately aimed that this project in future standardise the data format for all growth references.

An additional future objective is to create a respository of all available growth references.