[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/6b1137d60067b8aedfea#?env%5Blocalhost%3A5000-testing%5D=W3sia2V5IjoiYmFzZVVybCIsInZhbHVlIjoibG9jYWxob3N0OjUwMDAiLCJlbmFibGVkIjp0cnVlfV0=)

![RCPCH Logo](https://www.rcpch.ac.uk/themes/rcpch/images/logo-desktop.svg)
# CALCULATIONS FOR GROWTH CHARTS USING UK-WHO GROWTH REFERENCES 
Marcus Baw, Helen Bedford, Simon Chapman, Tim Cole, Mary Fewtrell, Victoria Jackson, Liz Marder, Rachel McKeown, Jonathan Miall, Andy Palmer, Charlotte Weldon, Charlotte Wright, Magdalena Umerska.

## Clinical Aspects
### Introduction
#### The Charts
The UK-WHO 0-4 year old charts were officially launched on May 11th 2009. Any child born after that date should be plotted on a UK-WHO Growth chart.  Children born before May 11th 2009 are plotted on British 1990 (UK90) charts and subsequent measurements must be plotted using those charts. There should be no switch over of existing children to the new UK-WHO Charts.  After age 4 we revert to using UK90 charts. The source data for these charts (UK90 and WHO 2006) together define the UK-WHO growth charts, containing LMS values by age.  These data are freely available and can be used without charge as long as their source is acknowledged in any publications or products using them. Users may not claim any IP rights over them, derive financial gain from supplying the data to others, seek to restrict use of the data by others or use them for the purposes of advertising or promoting other products. Notwithstanding this limited grant of rights, the original copyright notices must continue to be reproduced in any copies of these materials.

#### The UK RCPCH Growth Chart Application Program Interface (API) Project (RCPCHGrowth)
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

5. _LMSdata_BP.xls_: systolic & diastolic blood pressure for ages 4 to 24 yr.

### Medical Recommendations
A particular stated requirement of RCPCHGrowth was not only to provide accurate and validated calculations against anthropometric data, but also to report alongside these clinical interpretations of the numbers generated. 

Advice provided is of two kinds:
- Advice for parents and carers
- Advice for clinicians

Advice reported is based on centile cut-offs:

The advice text is published elsewhere in the repository.

## Technical Aspects
### API
The API is written in Python 3.8.
Mathematical and statistical calculations are made using the [SciPy](https://www.scipy.org/) and [NumPy](https://numpy.org/) libraries. [Pandas](https://pandas.pydata.org/) and [Xlrd](https://pypi.org/project/xlrd/) are used for data analysis.

Server middleware used is [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/).

### Clients
See associate repositories. There are currently two clients offered as examples of implementation for users to follow. Please be aware that rendering of charts and reporting of results must adhere to strict guidance to comply with the licensing agreement for use. This advice is published elsewhere in the repository and forms consensus opinion of the UK Growth Chart Reference Group and the Clinical Board.

#### Flask
The Flask client is provided with [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) and [FlaskForms](https://github.com/wtforms/wtforms/). CSS Framework is provided by [Semantic UI](https://semantic-ui.com/) and [Jinja2](https://pypi.org/project/Jinja2/). Graphing is implemented with [ChartJS](https://www.chartjs.org/) and zoom plugin [chart-js-plugin-zoom](https://github.com/chartjs/chartjs-plugin-zoom).

#### React
The React client is provided by [React](https://reactjs.org/) (16.13.1) and [React Router](https://reactrouter.com/) (5.2.0). CSS Framework is provided by [Semantic UI React](https://react.semantic-ui.com/) (0.88.2). Graphing is implemented with [ChartJS](https://www.chartjs.org/) and zoom plugin [chart-js-plugin-zoom](https://github.com/chartjs/chartjs-plugin-zoom).

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
`/api/v1/json/calculations`: GET - Accepts parameters listed below. Returns Measurement class object as JSON (see below).
This function accepts up to 3 measurements made on the same day (height, weight and head circumference) and returns an array of up to 4 Measurement class objects as a response (BMI is also returned is height in cm and weight in kg are supplied).
__Query Params__
Naming is based on PEP 8 standards
- `"birth_date": date` date of birth of the infant/child in YYYY-MM-DD ISO8601 format (will be converted to Date)
- `"observation_date": date` date of birth of the infant/child in YYYY-MM-DD ISO8601 format (will be converted to Date)
- `"sex": string` 'male' or 'female' (lower case mandatory)
- `"gestation_weeks": int` length of pregnancy in weeks (optional)
- `"gestation_days": int` days additional to length of pregnancy in weeks (optional)
- `"height_in_cm": float` 
- `"weight_in_kg": float"` 
- `"head_circ_in_cm": float"`
Returns an array of Measurement class objects (see below)

`/api/v1/json/calculation`: GET - 
__Query Params__
Naming is based on PEP 8 standards
- `"birth_date": date` date of birth of the infant/child in YYYY-MM-DD ISO8601 format (will be converted to Date)
- `"observation_date": date` date of birth of the infant/child in YYYY-MM-DD ISO8601 format (will be converted to Date)
- `"sex": string` 'male' or 'female' (lower case mandatory)
- `"gestation_weeks": int` length of pregnancy in weeks (optional)
- `"gestation_days": int` days additional to length of pregnancy in weeks (optional)
- `"measurement_method": string` accepted parameters include: 'height', 'weight', 'ofc', 'bmi' (lower case mandatory)
- `"observation_value: float"` measurement value (mandatory). **NOTE:** Height must be provided in __cm__, weight must be provided in __kg__, BMI must be provided in __kg/m²__ and ofc (occipitofrontal circumference or head circumference) must be provided in __cm__.

Returns a Measurement class object (see below) as an array.

##### Response
-`200` on success
Each growth parameter generates a new json object in an array.
Therefore height, weight and head circumference performed on the same day report an array of 3 JSON objects.
```json
[
    {
        "birth_data": {
            "birth_date": "03/01/2020",
            "gestation_weeks": 31,
            "gestation_days": 3,
            "estimated_date_delivery": "03/03/2020",
            "estimated_date_delivery_string": "Tue 03 March, 2020",
        },
        "measurement_dates": {
            "obs_date": "15/05/2020",
            "decimal_age": 0.2,
            "chronological_decimal_age": 0.36,
            "chronological_calendar_age": "4 months, 1 week and 5 days",
            "corrected_decimal_age": 0.2,
            "corrected_calendar_age": "2 months, 1 week and 5 days",
            "corrected_gestational_age": {
                            "corrected_gestation_weeks": None,
                            "corrected_gestation_days": None
                        }, 
            "clinician_decimal_age_comment": "This is an age which has been corrected for prematurity.",
            "lay_decimal_age_comment": "This takes into account your child's prematurity"
        },
        "child_measurement_value": {  
            "observation_value": 60.7,
            "measurement_type": "height",
        },
        "measurement_calculated_values": {
            "height_sds": 1.20,
            "height_centile": 88,
            "clinician_height_commment": "This is in the top 15%. Serial data needed for comparison",
            "lay_height_comment": "Your child is tall for their age but in the normal range",
        }
    }
]

```

#### Functions

##### Date and age calculations

Ages are expressed as years. This is the number of days of life / 365.25. The extra 0.25 is to 
account for the leap year which comes round every 4 years.

A pregnancy lasts 40 weeks (280 days). This is calculated from the date of the baby's 
mother's last menstrual period.  In fact, from that date, ovulation will occur midway through 
the following cycle (on average 14 days into a 28 day cycle). This means that from conception,
a pregnancy actually lasts only 266 days. Babies are considered to have been born 'Term' if 
delivered anywhere from 37 to 42 weeks gestation (3 weeks before to 2 weeks after due date).

The due date is referred to as the Estimated Date of Delivery (EDD).

_Gestational age / post-menstrual age_
This is the gestation at which the infant was born and represents the number of weeks (and extra days) since last menstrual period. After delivery, the gestational age of preterm infants it is often tracked by clinicians in addition to chronological age (sometimes referred to at that point as 'corrected gestational age').

_Chronological decimal age_
This is the time elapsed since birth, in years, irrespective of gestation at birth. A baby born at 24 weeks would be 16 weeks old at 40 weeks gestation (16 x 7)/365.25 y

_Corrected decimal age_
This is the age of a child that was born preterm calculated from their due date, rather than from their birth date. This allows for some comparison between preterm and term babies.
Convention is that correction occurs for all babies born before 37 weeks (definition of term):
    babies born at or above 32 weeks have the additional weeks (calculated up to 40 weeks)
        subtracted from their chronological decimal age for the first year of life
    babies born below 32 weeks have the additional weeks (calculated up to 40 weeks) subtracted from their chronological decimal age until the age of 2 years

A few other things about correction:
- term is consider 37-42 weeks. No correction is made for any baby born between these gestations. Their decimal age, therefore is considered to be 0.0. This means a baby born at 42 weeks and 
now 2 weeks of age will calculate identically to a baby born at 37 weeks and now 2 weeks of age. The outcome of discussion amongst the project board members at length regarding babies born after 42 weeks gestation is that these infants should be treated as term and be considered to have an age of 0.0 y. It also follows that babies born premature who are not yet term will have a negative decimal age.


***Constants***
```python
TERM_PREGNANCY_LENGTH_DAYS = 40 * 7
TERM_LOWER_THRESHOLD_LENGTH_DAYS = 37 * 7
EXTREME_PREMATURITY_THRESHOLD_LENGTH_DAYS = 32 * 7
```
##### Functions
- `chronological_decimal_age(birth_date: date, observation_date: date) -> float` age reported to 1 d.p. calculated as the difference in days between date of birth at 00:00 and date of observation at 00:00 divided by 365.25 (to account for leap years every 4 years)
- `"chronological_calendar_age": string` human readable representation of age in years, months, weeks, days or hours. 
- `corrected_decimal_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_days: int)->float:` age reported to 1 d.p. accounting for prematurity. Returns a decimal age from 2 dates (birth_date and observation_date) and gestational age at delivery (gestation_weeks and gestation_days), based on 40 weeks as 0. Days/Weeks before 40 weeks are negative.
- Corrects for gestational age. 
- Corrects for 1 year, if gestation at birth >= 32 weeks and < 37 weeks
- Corrects for 2 years, if gestation at birth <32 weeks
- Otherwise returns decimal age without correction
- Returns a decimal age correct for gestation even over 37 weeks
- Depends on chronological_decimal_age function
- `"corrected_calendar_age": string` human readable representation of age in years, months, weeks, days or hours, accounting for prematurity, following principle of corrected decimal age
- `corrected_gestational_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_days: int)->str:` weeks of gestation (and supplementary days) in babies born premature who have not yet reached term. Reported as a string eg '24+3 weeks'
- `estimated_date_delivery(birth_date: date, gestation_weeks: int, gestation_days: int, pregnancy_length_days = 0) -> date:`
- Returns estimated date of delivery (as a python datetime) from gestational age and birthdate for those babies not yet 42 weeks gestation.
- Will still calculate an estimated date of delivery if already term (>37 weeks)


##### SDS and Centile Calculations

##### Functions
```python
def sds(age: float, measurement: str, measurement_value: float, sex: str, default_to_youngest_reference: bool = True)->float:
```
- **This function is specific to the UK-WHO data set as this is actually a blend of UK-90 and WHO 2006 references and necessarily has duplicate values.**
- Public function
- Returns a standard deviation score. 
- Parameters are: 
- a decimal age (corrected or chronological), 
- a measurement (type of observation) ['height', 'weight', 'bmi', 'ofc']
- observation (the value is standard units) [height and ofc are in cm, weight in kg bmi in kg/m²]
- sex (a standard string) ['male' or 'female']
- default_to_youngest_reference (boolean): defaults to False. For circumstances when the age exactly matches a join between two references (or moving from lying to standing at 2y) where there are 2 ages in the reference data to choose between.Defaults to the oldest reference unless the user selects True
- born_preterm (boolean): defaults to False. If a baby is 37-42 weeks, use the uk_who_0_20_term data by default. If a baby was born preterm, the UK90 gestation specific data is used up to 42 weeks.

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
- Converts a Z Score to a p value (2-tailed) using the SciPy library, which it returns as a percentage. Reported as an integer, or 1 d.p. if below 1 or above 99

```python
def measurement_from_sds(measurement: str,  requested_sds: float,  sex: str,  decimal_age: float, default_to_youngest_reference: bool = True) -> float:
    """
    Public method
    Returns the measurement from a given SDS.
    Parameters are: 
        measurement (type of observation) ['height', 'weight', 'bmi', 'ofc']
        decimal age (corrected or chronological),
        requested_sds
        sex (a standard string) ['male' or 'female']
        default_to_youngest_reference (boolean): in the event of an exact age match at the threshold of a chart,
            where it is possible to choose 2 references, default will pick the oldest reference (optional)

    Centile to SDS Conversion for Chart lines (these values are rounded to 2dp but are calculated to greater accuracy in the code - each centile equates to 2/3 of a SD)
    0.4th -2.67
    2nd -2.00
    9th -1.33
    25th -0.67
    50th 0
    75th 0.67
    91st 1.33
    98th 2.00
    99.6th 2.67
    """


#### BMI functions

```python
percentage_median_bmi( age: float, actual_bmi: float, sex: str)->float:
```
- This returns a child's BMI expressed as a percentage of the median value for age and sex. It is used widely in the assessment of malnutrition particularly in children and young people with eating disorders. Reported as an integer

```python
bmi_from_height_weight( height: float,  weight: float) -> float:
```
- Returns a BMI in kg/m<sup>2</sup> from a height in cm and a weight in kg. Reported to 1 d.p.
- Does not depend on the age or sex of the child.

```python
weight_for_bmi_height( height: float,  bmi: float) -> float:
```
- Returns a weight from a height in cm and a BMI in kg/m². Reported to 3 d.p.
- Does not depend on the age or sex of the child.

##### Scope
Currently the minimum viable product is to provide reliable calculations for all children in the UK under the age of 1 year for height, weight, body mass index (BMI) and head circumference ('occipitofrontal circumference' - OFC).

In addition to providing standard deviation scores (SDS) and centiles, it will also provide basic guidance for users on how to interpret the information received.

It is envisaged that once established and validated, older age groups can be included, and other growth references.

It is planned that the API will in future be able to receive longitudinal growth data of individual children as an array, with a view to making some interpretations on their growth pattern and trajectory, as well as *'thrive lines'*[5][6](#references)

It separately aimed that this project in future standardise the data format for all growth references.

An additional future objective is to create a respository of all available growth references.

* [References](docs/references.md)


## Copyright and License
This work is copyrighted ⓒ2020 The Royal College of Paediatrics and Child Health, and released under the GNU Affero Public License. Our [license file](./LICENSE.md) is included in this repository, with further details available here https://www.gnu.org/licenses/agpl-3.0.en.html


## Developing the RCPCH Growth Charts - WIP

* [Setting up your Python Development environment](docs/dev-documentation/python-development.md)
* [Running the Growth Chart API in development](docs/dev-documentation/running-in-development.md)
* Using different reference data files
* Adding new calculations
* Testing
* [Contributing](docs/dev-documentation/contributing.md)
* [Calculating Growth Parameters](docs/dev-documentation/about-calculating-growth-parameters.md)
