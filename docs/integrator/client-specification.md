---
title: Client Specification
reviewers: Dr Marcus Baw, Dr Simon Chapman, Dr Anchit Chandran
---

In this document, we have collated the exact specification mandated by the Digital Growth Charts Project Board for Digital Growth Charts. Much of the specification is inherited from the preceding paper growth charts, so clinicians have immediate familiarity using the digital version.

## Background

!!! warning "A safe and familiar Client User Interface is a requirement of the Licensing Agreement"
    **A requirement of the API licence is that any charts rendered must meet these standards as agreed by the Digital Growth Charts Project Board. A large amount of documentation has been produced to guide the clinically-safe design and rendering of UK growth charts.**

!!! tip "Implementation support service"
    The RCPCH can assist in both the technical implementation and clinical assurance of any new charts implementations. This ensures adherence to the Project Board specification, a clinically-safe User Interface, and increased likelihood of clinical-user acceptance. Please contact us to discuss your needs on <mailto:commercial@rcpch.ac.uk>.

### Understanding the UK-WHO dataset

It is critically important to understand the dataset is **not** a simple 'lookup table' of height/weight against ages and centiles.

Such a table would rapidly become large and unusable because of the number of variables involved. More, since variables like weight, height, etc. are *continuous*, not discrete, a 'lookup table' approach would involve a loss of accuracy.

The UK growth charts are made up of four datasets taken from two different growth references (see [clinical documentation](../clinician/chart-information-health-staff.md) for more detail).

- The UK 1990 preterm dataset runs from 23 weeks gestation to 42 weeks post-menstrual age as length (from 25 weeks), weight and head circumference.

- The WHO 2006 dataset runs from 2 weeks of age to 2 years of age as length, weight, BMI and head circumference.

- The WHO 2006 dataset continues as **height** (now measured *standing*) from 2 years to 4 years of age

- The UK90 dataset picks up from 4 years until 20 years (head circumference to 17 years in girls and 18 years in boys)

There is established clinical guidance for how these different datasets should be combined to produce a correct chart. This results in slight visual anomalies, such as small steps in the chart at 2 and 4 years of age, however, these are **intentional** and **clinically valid**.

## Implications for digital charting

These datasets all overlap. Therefore, when plotting, they must be rendered as four individual series. They will appear discontinuous, with breaks in the lines where they meet / overlap.

A natural step exists at each of these time points which **must** be respected. In particular, this is clinically relevant at age 2 years, where infants are no longer measured lying flat, and instead measured standing up, leading to a natural small step. If all 4 datasets are presented 0-20 years as a continuous dataset, chart packages will interpolate the gaps and the intentional 'step' will be lost. There is no change in references at this transition from infancy to childhood, but at exactly 2 years, the reference data have values for both lying and standing, so **both** should be plotted.

The API endpoint returns the chart data in an array of arrays.

- The first level array represents the 9 centiles `[0.4, 2, 9 , 25, 50, 75, 91, 98, 99.6]`, with each centile sequentially having a nested array of 4 arrays of data, one for each dataset (see below).
- The individual data points are reported as float values for x and y coordinates. X corresponds to decimal age, y to the measurement value of the chart requested. If the optional `three-percent-centiles` is passed - instead of the default `cole-nine-centiles` - an older format of 9 centiles `[3, 5, 10, 25, 50, 75, 90, 95, 97]` is returned. The `nine-cole-centiles` is the international standard.

The chart data is only returned for the measurement method requested e.g. if only height is supplied, only height centile data will be returned. Multiple API calls are required to obtain a full set of measurement data.

Along with the centile data, the growth data (presented to the endpoint in the request) are returned as an array of x and y coordinate values for plotting on the chart.

## Specifications for implementing your own charting

!!! success "React component reference charting implementation"
    In terms of technical, statistical and clinical skill-sets, making growth charts adhere to the specification, which are clinically safe and usable is quite difficult. That's why we built a [reference implementation](../products/react-component.md) of the charts, as a permissively-licensed React component, so you can use it in your own application.

    We **strongly** recommend the use of this package if possible. If not possible, we recommend discussion with the RCPCH Digital Growth Charts team to help properly start your implementation.

### Chart plotting

- Provide the facility to toggle between height chart and weight chart or display together.

- Offer option of BMI and head circumference charts for health staff use.

- Allow the chart to be scalable, i.e. zooming in or out, whilst maintaining variable, visible axes, or offer a variety of age ranges displayed to optimise data view.

- Provide option of Z-score (SD) plots for health staff use (see below).

- The 50th centile should be de-emphasised: this middle line must not be made darker or wider than others, as it might give the impression to families that being on it is desirable or normal. Standard notation is for the 0.4th, 9th, 50th, 91st and 99.6th centiles to be dashed, the 2nd, 25th, 75th and 98th centiles to be solid.

- Chart colour choices are not mandated by this document. The lines and data points need to meet accessibility guidelines, be clearly visible and avoid colour combinations that reduce usability. Also, we try to avoid gender stereotypical colours (pink and pale blue), as these seem dated in 2022.

- Information for the user must not be crowded, and where possible, contextualised. For example, information on puberty for girls should be shown only on girls' charts.

- Highlight the pitfalls of measuring weight in the first weeks after birth of a term infant. It is normal for babies to lose up to 10% of their birth weight; this should be made clear to users.

- Signpost reference transitions. The user should be made aware of why the lines are discontinuous between data sets, or when going from lying measurements to standing.

- Chart labelling: axes must be labelled appropriately with the correct intervals. Below 42 weeks gestation, the x-axis should reflect gestation. Beyond 42 weeks to 2 years, weeks and months should be shown. Above 2 years, months and years should be shown. Above 4 years, yearly and 6-monthly intervals are shown. On the y-axis, measurement units should be used, with scope of the chart showing only the measurements, not the whole chart.

- Provide help and information facility to access instructions drawn from the RCPCH educational materials (see separate documents: [information for parents](../clinician/chart-information-families.md), [information for health staff](../clinician/chart-information-health-staff.md)).

### When plotting centile charts

Certain key presentation principles should be included:

- Use Cole nine-centile format (see below).

- Scale different elements of the chart to best display information in each period.

- When hovering over a point, either show exact age and centile band (see below), or show in an embedded table.

- Different data points should not be joined by lines.

- Data points should follow standard notation: a child's growth point plotted at their chronological age is a round dot. If plotted at their age adjusted for gestation, it is plotted as a cross. If plotted together, they are joined by a line, often with an 'arrow back', denoting the relationship.

- Bone ages can additionally be plotted on the chart. These are skeletal ages calculated using standard scores from x-rays of the left hand. They are associated with a height value measured on the same day. They are plotted as a cross, with the bone age on the x-axis and the measurement on the y-axis. The measurement is plotted against age (corrected and chronological) as standard. The two plots are connected by a dotted/dashed line to denote they are linked.

- Events can be plotted on the chart also - these are contextual information, such as starting a treatment or the time a diagnosis is made. They are a vertical arrow above or below the measurement in question, outside the centiles for clarity.

- There should be a toggle button to allow the user to see the chronological and corrected ages separately or together.

- Omit grid lines, which are only useful for manual plotting, and the y-axis can be inconspicuous.

### When plotting Z-score (SD) charts

- Z-score centile charts may be created with age on the x-axis and Z-score on the y-axis. This converts the centile curves to horizontal straight lines.

- All available measurements (weight, height, head, BMI) should be plotted as series on the same chart, with consistent colour coding of the different series (e.g. weight is always be red and height is always blue etc.).

- The data points may be joined by fine lines.

- The y-axis should cross the x-axis at Z = 0, and have horizontal centile lines at intervals of 0.67 Z between -2.67 and 2.67.

### Adjusting for Gestation at birth

On the centile chart, it should be clear that allowance has been made for varying age of gestation at birth, by offering the option of plotting at chronological age with a **circle**, as well as gestational age (age – number of weeks premature) with a **cross**. If plotted together, they should be joined by a line. An option should be offered to toggle between the plotted chronological, corrected ages and both.

!!! note "Gestation Age Correction through the life course"
    **The standard has recently changed**: gestational age is now taken into account, even when born at 'term gestational ages', and across the whole lifespan. This change was adopted because digital charting makes gestational age correction much easier to do. In fact, it is now a completely automated process because of the Digital Growth Charts API.

    *Note: this is different from paper charts, where gestational age correction was manual, and therefore only done up to 1 or 2 years depending on the degree of prematurity.*

#### Examples

| Example Gestation | Old policy                                                       | New policy                                                                                                                           |
| ----------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 39 weeks + 4 days   | Plot on 'Term' reference                                         | 'Term' reference has been abandoned in favour of plotting on UK90 preterm chart, up till corrected gestational age of 42 weeks + 0 days |
| 26 weeks + 0 days   | Gestational age correction applied until 2 years old (corrected) | Correct for the whole life span                                                                                                      |
| 35 weeks + 6 days   | Gestational age correction applied until 1 years old (corrected)  | Correct for the whole life span                                                                                                      |

#### Definitions

- **Gestation at birth**: 
- **Weeks premature**: 
- **Gestational age**: 
- **Chronological age**: 

Gestational adjustment option provided for all birth gestations and continues indefinitely.

On a Z-score plot, the adjusted Z-score for gestation should be plotted against actual (chronological) age, with a label on the plot specifying the number of weeks premature.

## Essential standards for rendering

Whilst not essential to show the whole life course when plotting measurements against centile lines, the rendering of the centile lines and the plots must meet the following design standards:

- Centiles should be clearly labelled.

- Overlap between datasets for each centile should be clearly visible, and no interpolation function should be used to link them.

- The 0.4th, 9th, 50th, 91st and, 99.6th centiles should all be dashed lines (**not** dotted, **not** continuous).

- The 2nd, 25th, 75th and 98th centiles should be continuous lines (thin).

- Axes should be clearly labelled: (Height/Length in cm, Weight in kg, Body Mass Index in kg/m<sup>2</sup>, head circumference in cm, age in years).

- X-axis (age in years) increments should be monthly under the age of 2 years, 3-monthly over the age of 2 years.

- Precision of measurements (height, weight, etc.) should be one decimal place.

- Centiles should be reported as integers, except if > 99 or < 1. If outside threshold, they should be reported as > 99.6 or < 0.4.

## The UK Nine centile chart format

The nine centile lines used in the British 1990 and UK-WHO charts are labelled in terms of rounded centiles (see table below), but they are precisely defined in terms of the underlying Z-scores. The following Z-score thresholds are used to define the centiles in the British charts:

| Approximate centile | Exact Z-score | Line format |
| ------------------- | ------------- | ----------- |
| 0.4th               | -2.67         | Dashed      |
| 2nd                 | -2.00         | Continuous  |
| 9th                 | -1.33         | Dashed      |
| 25th                | -0.67         | Continuous  |
| 50th                | 0             | Dashed      |
| 75th                | 0.67          | Continuous  |
| 91st                | 1.33          | Dashed      |
| 98th                | 2.00          | Continuous  |
| 99.6th              | 2.67          | Dashed      |

## Definitions and terminology of Centile Bands

A "centile space" is the distance between two centile lines.

A child is defined as being “on” a centile when within 0.17 SD (0.25 centile space) of the underlying exact Z-score, otherwise, they are “between”.

| Centile band | SDS Lower limit | SDS Upper limit | Additional Message - Weight/Height/Head | Additional Message - BMI |
| ------------ | --------------- | --------------- | --------------------------------------- | ------------------------ |
|              | < -6            |                 | Probable error                          | Probable error           |
| Below 0.4th  | -6.00           | -2.84           | Below normal range                      | Very thin                |
| 0.4th        | -2.84           | -2.50           |                                         | Low BMI                  |
| 0.4th-2nd    | -2.50           | -2.17           |                                         | Low BMI                  |
| 2nd          | -2.17           | -1.83           |                                         |                          |
| 2nd-9th      | -1.83           | -1.50           |                                         |                          |
| 9th          | -1.50           | -1.16           |                                         |                          |
| 9th-25th     | -1.16           | -0.84           |                                         |                          |
| 25th         | -0.84           | -0.5            |                                         |                          |
| 25th-50th    | -0.50           | -0.17           |                                         |                          |
| 50th         | -0.17           | 0.17            |                                         |                          |
| 50th-75th    | 0.17            | 0.50            |                                         |                          |
| 75th         | 0.5             | 0.84            |                                         |                          |
| 75th-91st    | 0.84            | 1.16            |                                         |                          |
| 91st         | 1.16            | 1.50            |                                         |                          |
| 91st-98th    | 1.50            | 1.83            |                                         | Overweight               |
| 98th         | 1.83            | 2.17            |                                         | Overweight               |
| 98th-99.6th  | 2.17            | 2.50            |                                         | Overweight (obese)       |
| 99.6th       | 2.50            | 2.84            |                                         | Overweight (obese)       |
| >99.6th      | 2.84            | 6               | Above normal range                      | Severely obese           |
|              |                 | > 6             | Probable error                          | Probable error           |

*[BMI]: Body Mass Index
