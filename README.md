![RCPCH Logo](https://www.rcpch.ac.uk/themes/rcpch/images/logo-desktop.svg)
# CALCULATIONS FOR GROWTH CHARTS USING UK-WHO GROWTH REFERENCES 
Marcus Baw, Helen Bedford, Simon Chapman, Tim Cole, Mary Fewtrell, Victoria Jackson, Liz Marder, Rachel McKeown, Jonathan Miall, Andy Palmer, Charlotte Weldon, Charlotte Wright, Magdalena Umerska

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

##### 0.4th Centile
###### ___Height/Length___

 *-*_Parent/Carer of child aged < 2y:_
```
"Your child has a lower or the same length as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child has a lower or the same height as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

 *-* _Clinician_
```
"On or below the 0.4th centile for height. Medical review advised."
```
###### ___Weight___

 *-* _Parent/Carer_
```
"Your child has a lower or the same weight as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

 *-* _Clinician_
```
"On or below the 0.4th centile for weight. Medical review advised."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is below or the same weight as only 4 in every 1000 children. It is advisable to see your doctor."
```

 *-* _Clinician_
```
"On or below the 0.4th centile. Medical review advised."
```
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child 's head size is larger than or the same as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

 *-* _Clinician_
```
"On or below the 0.4th centile for head circumference. Medical review advised."
```
***
##### 2nd Centile
###### ___Height/Length___

 *-*_Parent/Care_of child aged < 2y:_
```
"Your child is in the lowest 2 percent for length, sex and age. Consider seeing your doctor."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child is in the lowest 2 percent for height, sex and age. Consider seeing your doctor."
```

 *-* _Clinician_
```
"On or below the 2nd centile. Consider reviewing trend."
```
###### __Weight__

 *-* _Parent/Carer_
```
"Your child is in the lowest 2 percent for weight compared with other children the same age and sex. Consider seeing your doctor."
```

 *-* _Clinician_
```
"On or below the 2nd centile. Consider reviewing trend."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is is in the lowest 2 percent of the population for their weight. Consider seeing your doctor."
```

 *-* _Clinician_
```
"On or below the 2nd centile. Consider reviewing trend."       
```     
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child's head size is in the lowest 2 percent as other children the same sex and age. Consider seeing your doctor."
```

 *-* _Clinician_
```
"On or below the 2nd centile for head circumference. Consider reviewing trend."
```
***
##### 9th Centile
###### ___Height/Length___
__Parent/Carer_of child aged < 2y:_
```
"Your child is in the lowest 9 percent of the population for length, sex and age."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child is in the lowest 9 percent of the population for height, sex and age."
```

 *-* _Clinician_
```
"On or below the 9th centile. Consider reviewing trend."
```
###### ___Weight___

 *-* _Parent/Carer_
```
"Your child is in the lowest 9 percent of the population for weight compared with other children the same age and sex."
```

 *-* _Clinician_
```
"On or below the 9th centile. Consider reviewing trend."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the lowest 9 percent of the population for weight."
```

 *-* _Clinician_
```
"On or below the 9th centile. Consider reviewing trend."
```
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child's head size is in the lowest 9 percent of the population for children the same sex and age."
```

 *-* _Clinician_
```
"On or below the 9th centile for head circumference. Consider reviewing trend."
```
***
##### 25th Centile
###### ___Height/Length___

 *-*_Parent/Care_of child aged < 2y:_
```
"Your child is in the lowest 1/4 of the population for length, sex and age."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child is in the lowest 1/4 of the population for height, sex and age."
```

 *-* _Clinician_
```
"On or below the 25th centile. Consider reviewing trend."
```

###### ___Weight___

 *-* _Parent/Carer_

```
"Your child is in the lowest 1/4 of the population for weight, compared with other children the same age and sex."
```

 *-* _Clinician_
```
"On or below the 25th centile. Consider reviewing trend."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the lowest 1/4 of the population for their weight."
```

 *-* _Clinician_
```
"On or below the 25th centile. Consider reviewing trend."
```
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child's head size is in the lowest 1/4 of the population compared with other children the same sex and age."
```

 *-* _Clinician_
```
"On or below the 25th centile for head circumference. Consider reviewing trend."
```
***
##### 50th Centile
###### ___Height/Length___

 *-*_Parent/Care_of child aged < 2y:_
```
"Your child is on or just below the average length of the population for sex and age."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child is on or just below the average height of the population for sex and age."
```

 *-* _Clinician_
```
"On or below the 50th centile."
```

###### ___Weight___

 *-* _Parent/Carer_
```
"Your child is on or just below the average weight of the population, compared with other children the same age and sex."
```

 *-* _Clinician_
```
"On or below the 50th centile."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is on or just below the average weight for the population ."
```

 *-* _Clinician_
```
"On or below the 50th centile."
```
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child is on or just below the average height of the population for sex and age."
```

 *-* _Clinician_
```
"On or below the 50th centile for head circumference."
```
***
##### 75th Centile
###### ___Height/Length___

 *-*_Parent/Care_of child aged < 2y:_
```
"Your child has the same or a shorter length than 75 percent of children the same age and sex."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child has the same or a shorter height than 75 percent of children the same age and sex."
```

 *-* _Clinician_
```
"On or below the 75th centile. Consider reviewing trend."
```
###### ___Weight___

 *-* _Parent/Carer_
```
"Your child is below or the same as 75 percent of children the same age and sex. This does not take account of their height."
```

 *-* _Clinician_
```
"On or below the 75th centile. Consider reviewing trend."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is below or the same as 75 percent of children for their weight."
```

 *-* _Clinician_
```
"On or below the 75th centile. Consider reviewing trend."
```

###### _Head Circumference_

 *-* _Parent/Carer_
```
"Your child's head circumference is in the top 25 percent of children the same age and sex."
```

 *-* _Clinician_
```
"On or below the 75th centile for head circumference. Consider reviewing trend."
```
***
##### 91st Centile
###### ___Height/Length___

 *-*_Parent/Care_of child aged < 2y:_
```
"Your child is in the top 9 percent of children the same age and sex for their length."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child is in the top 9 percent of children the same age and sex for their height."
```

 *-* _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
###### ___Weight___

 *-* _Parent/Carer_
```
"Your child is in the top 9 percent of children the same age and sex for their weight. This does not take account of their height."
```

 *-* _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the top 9 percent of children for their weight."
```

 *-* _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child's head circumference is in the top 9 percent of children the same age and sex."
```

 *-* _Clinician_
```
"On or below the 91st centile for head circumference. Consider reviewing trend."
```
***
##### 98th Centile
###### ___Height/Length___

 *-*_Parent/Care_of child aged < 2y:_
```
"Your child is in the top 2 percent of children the same age and sex for their length."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child is in the top 2 percent of children the same age and sex for their height."
```

 *-* _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
###### ___Weight___

 *-* _Parent/Carer_
```
"Your child is in the top 2 percent of children the same age and sex for their weight. This does not take account of their height. Consider seeking medical review ."
```

 *-* _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the top 2 percent of children for their weight. Consider seeing your doctor."
```

 *-* _Clinician_
```
"On or below the 98th centile. Meets definition for being overweight. Consider reviewing trend."
```
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child's head circumference is in the top 2 percent of children the same age and sex. Consider seeing your doctor."
```

 *-* _Clinician_
```
"On or below the 91st centile for head circumference. Consider reviewing trend."
```
***
#### 99.6th Centile
###### ___Height/Length___

 *-*_Parent/Care_of child aged < 2y:_
```
"Your child is longer than only 4 children in every 1000 the same age and sex. Consider seeking medical review."
```

 *-*_Parent/Carer of child aged >= 2y_
```
"Your child is taller than only 4 children in every 1000 the same age and sex. Consider seeking medical review."
```

 *-* _Clinician_
```
"On or below the 99.6th centile. Consider medical review."
```
###### ___Weight___

 *-* _Parent/Carer_
```
"Your child is taller than only 4 children in every 1000 the same age and sex. This does not take account of their height. Medical review is advised."
```

 *-* _Clinician_
```
"On or below the 99.6th centile. Consider medical review."
```
###### ___BMI___

 *-* _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child 's  weight is lower than only 4 children in every 1000 childre. Medical review is advised."
```

 *-* _Clinician_
```
"On or below the 99.6th centile. Above obesity threshold. Consider medical review."
```
###### ___Head Circumference___

 *-* _Parent/Carer_
```
"Your child's head circumference is larger than only 4 children in every 1000 children the same age and sex. Medical review is advised."
```

 *-* _Clinician_
```
"On or below the 99.6th centile for head circumference. Medical review is advised."
```

## Technical Aspects
### API
The API is written in Python 3.8.
Mathematical and statistical calculations are made using the [SciPy](https://www.scipy.org/) and [NumPy](https://numpy.org/) libraries.
Server middleware used is [Flask](https://flask.palletsprojects.com/en/1.1.x/quickstart/) and [FlaskForms](https://github.com/wtforms/wtforms/), [Pandas](https://pandas.pydata.org/) and [Xlrd](https://pypi.org/project/xlrd/) for data analysis.
Frontend is provided by [Semantic UI](https://semantic-ui.com/) and [Jinja2](https://pypi.org/project/Jinja2/). Graphing is implemented with [ChartJS](https://www.chartjs.org/) and zoom plugin [chart-js-plugin-zoom](https://github.com/chartjs/chartjs-plugin-zoom).

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

- `/` This endpoint renders a webform which accepts a POST request and returns age, centile and SDS calculations of children's growth data. A typical response is shown below in [Arguments](#Arguments). Note that growth reference data do not exist to calculate SDS or centiles for:
1. Height/Length below 25 weeks gestation
2. BMI below 2 weeks of age (post 40 weeks)
3. OFC (occipitofrontal circumference) above 17y in girls and >18y in boys.
In these circumstances, `NoneType` is returned.

- `/results/table` : Reports anthropometric data entered via the webform with calculated values (ages/SDS and centile values with clinical guidance) as a table.

- `/results/chart` : Plots data entered via the webform, or uploaded in .xlsx format, as growth charts. Charts have capability to zoom in and out.

- `/chart_data` : a JSON dump of the centile chart data

- `/import` : accepts a POST request to upload an excel spreadsheet of mixed patient data (for example for research purposes), or serial growth data over time for individual patients. The upload format for each is different and prescribed. Mandatory column names are: 'birth_date', 'observation_date', 'gestation_weeks','gestation_days', 'sex', 'measurement_type', 'measurement_value'. These are case sensitive. measurement_type must be lower case and one of 'height', 'weight', 'ofc', 'bmi'. This must be anonymised as is in the public domain. Any columns other than those prescribed will be stripped and discarded. No data is retained on the server.

- `/uploaded_data/example` : this is a sample spreadsheet of fictional data for users to try

- `/uploaded_data/excel_spreadsheet` : redirected here once an excel spreadsheet of data has been uploaded.

- `/references` : currently is a hardcoded list (stored as JSON) of national and international growth references (not the datasets themselves), with literature references and authorship, date of publication. The intention is for this to be stored in a database and available opensource (with some governance) for users to update and use. In future it is intended to be a national standard for growth reference publication and provide guidance on growth reference development.

- `/instructions` : currently renders this readme.md. In future is intended to be a resource to help users access the API, as well as details of the API licence, rules of use and disclaimers.

#### Arguments
Naming is based on PEP 8 standards
- `"birth_date": date` date as datetimestamp (mandatory). This is of format 'DD/MM/YY' (eg 01/05/2020), without timestamp or locale
- `"observation_date": date` date as datetimestamp (mandatory). This is of format 'DD/MM/YY' (eg 01/05/2020), without timestamp or locale
- `"sex": string` MALE or FEMALE (mandatory)
- `"gestation_weeks": int` length of pregnancy in weeks (optional)
- `"gestation_days": int` days additional to length of pregnancy in weeks (optional)
- `"gestation_total_days": int` length of pregnancy in days from conception (optional)
- `"measurement_type": string` HEIGHT / WEIGHT / OFC / BMI (/ SKIN_FOLDS / PEFR) lower case (mandatory)
- `"measurement_value: float"` observation to 2 dp (mandatory)


-`201 Created` on success
Each growth parameter generates a new json object in an array.
Therefore height, weight and head circumference performed on the same day report an array of 3 JSON objects.
```json
[
    {
        "birth_data": {
            "birth_date": "03/01/2020",
            "gestation_weeks": 31,
            "gestation_days": 3,
        },
        "measurement_dates": {
            "obs_date": "15/05/2020",
            "chronological_decimal_age": 0.36,
            "chronological_calendar_age": "4 months, 1 week and 5 days",
            "corrected_decimal_age": 0.2,
            "corrected_calendar_age": "2 months, 1 week and 5 days",
            "corrected_gestational_age": ""
            "clinician_decimal_age_comment": "This is an age which has been corrected for prematurity.",
            "lay_decimal_age_comment": "This takes into account your child's prematurity"
        },
        "child_measurement_value": {  
            "height": 60.7,
            "weight": None,
            "bmi": None,
            "ofc": None
        },
        "measurement_calculated_values": {
            "height_sds": 1.20,
            "height_centile": 88,
            "clinician_height_commment": "This is in the top 15%. Serial data needed for comparison",
            "lay_height_comment": "Your child is tall for their age but in the normal range",
            "weight_sds":  None,
            "weight_centile": None,
            "clinician_weight_commment": None,
            "lay_weight_comment": None,
            "ofc_sds":  None,
            "ofc_centile": None,
            "clinician_ofc_commment": None,
            "lay_ofc_comment": None,
        }
    }
]
```

- `"decimal_age_in_years": float` age reported to 1 d.p. calculated as the difference in days between date of birth at 00:00 and date of observation at 00:00 divided by 365.25 (to account for leap years every 4 years)
- `"chronological_calendar_age": string` human readable representation of age in years, months, weeks, days or hours. 
- `"corrected_decimal_age"` age reported to 1 d.p. accounting for prematurity. Correction only occurs in babies born below 32 weeks for the first 2 years of life, or if below 37 weeks, for the first year only.
- `"corrected_calendar_age": string` human readable representation of age in years, months, weeks, days or hours, accounting for prematurity, following principle of corrected decimal age
- `"corrected_gestational_age": string` weeks of gestation (and supplementary days) in babies born premature who have not yet reached term. Reported as a string eg '24+3 weeks'

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
corrected_decimal_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_days: int)->float:
```
- Corrects for gestational age. 
- Corrects for 1 year, if gestation at birth >= 32 weeks and < 37 weeks
- Corrects for 2 years, if gestation at birth <32 weeks
- Otherwise returns decimal age without correction

```python
chronological_calendar_age(birth_date: date, observation_date: date) -> str:
```
- Returns age in years, months, weeks and days as a string: to return a corrected calendar age user passes estimated date of delivery (EDD) instead of birth date

```python
estimated_date_delivery(birth_date: date, gestation_weeks: int, gestation_days: int, pregnancy_length_days = 0) -> date:
```
- Returns estimated date of delivery (as a python datetime) from gestational age and birthdate
- Will still calculate an estimated date of delivery if already term (>37 weeks)

```python
corrected_gestational_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_days: int)->str:
```
- Returns a corrected gestational age for those babies not yet 42 weeks gestation

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
- observation (the value is standard units) [height and ofc are in cm, weight in kg bmi in kg/m2]
- sex (a standard string) ['male' or 'female']
- default_to_youngest_reference (boolean): defaults to True. For circumstances when the age exactly matches a join between two references (or moving from lying to standing at 2y) where there are 2 ages in the reference data to choose between.Defaults to the youngest reference unless the user selects false

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
            where it is possible to choose 2 references, default will pick the youngest reference (optional)

    Centile to SDS Conversion for Chart lines
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
- Returns a weight from a height in cm and a BMI in kg/m2. Reported to 3 d.p.
- Does not depend on the age or sex of the child.

##### Scope
Currently the minimum viable product is to provide reliable calculations for all children in the UK under the age of 1 year for height, weight, body mass index (BMI) and head circumference ('occipitofrontal circumference' - OFC).

In addition to providing standard deviation scores (SDS) and centiles, it will also provide basic guidance for users on how to interpret the information received.

It is envisaged that once established and validated, older age groups can be included, and other growth references.

It is planned that the API will in future be able to receive longitudinal growth data of individual children as an array, with a view to making some interpretations on their growth pattern and trajectory, as well as *'thrive lines'*[5][6](#references)

It separately aimed that this project in future standardise the data format for all growth references.

An additional future objective is to create a respository of all available growth references.

### References
1. Cole TJ, Freeman JV, Preece MA. British 1990 growth reference centiles for weight, height, body mass index and head circumference fitted by maximum penalized likelihood. Stat Med 1998;17:407-29. 
2.    Cole TJ, Freeman JV, Preece MA. 1998. British 1990 growth reference centiles for weight, height, body mass index and head circumference fitted by maximum penalized likelihood. Stat Med 17(4):407-29 
3.  WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Length/Height-for-age, Weight-for-age, Weight-for-length, Weight-for-height and Body Mass Index-for age. Methods and Development. 2006. ISBN    92 4 154693 X.  
4.  WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Head circumference-for-age, arm circumference-for-age, triceps skinfold-for-age and subscapular skinfold-for age. Methods and Development. 2007. ISBN 978 92 4 154718 5. 
5.  3-in-1 weight monitoring chart. T Cole, Lancet. 1997 Jan 11;349(9045):102-3.
6. A chart to predict adult height from a child’s current height. T Cole, C Wright, Annals of Human Biology, November–December 2011; 38(6): 662–668
