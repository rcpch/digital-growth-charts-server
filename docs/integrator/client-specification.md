---
title: Client Specification
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# Client Specification

## Background

!!! warning
    **A requirement of the licence for the API is that any charts rendered must meet these standards as agreed by the Digital Growth Charts Project Board. A large amount of documentation has been produced to guide the clinically safe design and rendering of UK growth charts.**

!!! tip "Implementation support service"
    The RCPCH can assist in both the technical implementation and clinical assurance of any new charts implementations, to ensure adherence to the Project Board specification, a clinically safe user interface, and likely clinician user acceptance. Please contact us to discuss your needs on <mailto:commercial@rcpch.ac.uk>

### Understanding UK-WHO

The UK growth charts are made up of 4 datasets taken from 2 growth references (see [clinical documentation](../clinician/chart-information-health-staff.md) for more detail).

- The UK90 preterm dataset runs from 23 weeks gestation to 42 weeks postmenstrual age as length (from 25 weeks), weight and head circumference.

- The WHO 2006 dataset runs from 2 weeks of age to 2 years of age as length, weight, BMI and head circumference.

- The WHO 2006 dataset continues as **height** (now measured _standing_) from 2 years to 4 years of age

- The UK90 dataset picks up from 4y until 20y (head circumference to 17y in girls and 18y in boys)

## Implications for charting digitally

- These datasets all overlap, and therefore when plotting them, they must be passed to charting packages as 4 individual series. This means they will appear as discontinuous, with breaks in the lines where they meet/overlap.

- There is a natural step at each of these time points which **must** be respected. If all 4 datasets are presented 0-20y as a continuous dataset, chart packages will interpolate the gaps and the intentional 'step' will be lost. This is particularly clinically relevant at aged 2 y, where infant are measured standing, not lying as is standard before this age. This leads to a natural small step in the data which must be respected. There is no change in references at this transition from infancy to childhood, but the reference data have values for both lying and standing, so both should be plotted.

- The API endpoint returns the chart data in an array of arrays. The first level array represents the 9 centiles `[0.4, 2, 9 , 25, 50, 75, 91, 98, 99.6]`, with each centile in turn having a nested array of 4 arrays of data, one for each dataset (see below). The individual data points are reported as float values for x and y coordinates. X corresponds to decimal age, y to the measurement value of the chart requested. If the `three-percent-centiles` optionally is passed in (instead of the default `cole-nine-centiles`) an older format of 9 centiles `[3, 5, 10, 25, 50, 75, 90, 95, 97]` is returned. The `nine-cole-centiles` is default if no parameter is passed, and this is the international standard.

- The chart data is only returned for the measurement method requested - if only height is supplied, only height centile data will be returned.

- In addition to the centile data, the growth data presented to the endpoint in the request are returned as an array of x and y values.

## Specifications for implementing your own charting

!!! success "React component reference charting implementation"
    Making growth charts that adhere to the specifcation and are clinical safe and usable is not completely straightforward. That's why we have built a [reference implementation](/products/react-component.md) of the charts, as a permissively licensed React component so that you can use it in your own application.

### Chart plotting

- Provide the facility to toggle between height chart and weight chart or display together.

- Offer option of BMI and head circumference charts for health staff use.

- Allow the chart to be scaleable, i.e. zooming in or out, while maintaining variable, visible axes or offer a variety of age ranges displayed to optimise data view.

- Provide option of Z-score (SD) plots for health staff use (see below).

- The 50th Centile should be de-emphasised: this middle line must not be made darker or wider than others, as it might give the impression to families that being on it is desirable or normal. Standard notation is for the 0.4th, 9th, 50th, 91st and 99.6th centiles to be dashed, the 2nd, 25th, 75th and 98th centiles to be solid.

- Chart colours are not prescribed. The lines and data points need to be meet accessibilty guidelines, be clearly visible and avoid colour combinations that reduce useabilty.

- Information for the user must not be crowded, and where possible, contextualised. For example, information on puberty for girls be shown only on girls' charts.

- Highlight the pitfalls of measuring weight in the first weeks after birth of a term infant. It is normal for babies to lose up to 10% of their birth weight - this should be made clear to users.

- Signpost reference transitions. The user should be made aware of why the lines are discontinuous between data sets or when going from being measured from lying to standing.

- Chart labelling: axes must be labelled appropriately with the correct intervals. Below 42 weeks gestation, the x axis should reflect gestation. Beyond 42 weeks to 2 years, weeks and months should be shown. Above 2 years, months and years should be shown. Above 4 y, yearly and 6mthly intervals are shown. On the y axis, measurement units should be used, with scope of the chart showing only the measurements, not the whole chart.

- Provide help / information facility to access instructions drawn from the RCPCH educational materials (see separate documents: information for parents, information for health staff).

### When plotting centile charts

Certain key presentation principles should be included:

- Use Cole nine-centile format (see below).

- Scale different elements of the chart to best display information in each period.

- Either show exact age and centile band (see below) when hovering over a point or show in an embedded table.

- Different data points should not be joined by lines.

- Data points should follow standard notation: a child's growth point plotted at their chronological age is a round dot. If plotted at their age adjusted for gestation, it is plotted as a cross. If plotted together, they are joined by a line, often with an 'arrow back', denoting the relationship.

- Bone ages can additionally be plotted on the chart. These are skeletal ages calculated using standard scores from x-rays of the left hand. They are associated with a height value measured on the same day. They are plotted as a cross, with the bone age on the x-axis, the measurement on the y-axis. The measurement is plotted against age (corrected and chronological) as standard. The two plots are connected by a dotted/dashed line to denote they are linked.

- Events can be plotted on the chart also - these are contextual information, such as starting a treatment or the time a diagnosis is made. They are a vertical arrow above or below the measurement in question, outside the centiles for clarity.

- There should be a toggle button to allow the user to see the chronological and corrected ages separately or together.

- Omit grid lines, which are only useful for manual plotting, and the Y axis can be inconspicuous.

### When Plotting Z-score (SD) charts

- Z-score centile charts may be created with age on the X axis and Z-score on the Y axis – this converts the centile curves to horizontal straight lines.

- All available measurements (weight, height, head, BMI) should be plotted as series on the same chart with consistent colour coding of the different series (e.g. weight could always be red and height blue etc).

- The data points may be joined by fine lines.

- The Y axis should cross the X axis at Z = 0 and have horizontal centile lines at intervals of 0.67 Z between -2.67 and 2.67.

### Adjusting for Gestation at birth

On the centile chart it should be made clear that allowance has been made for varying age of gestation at birth by offering the option of plotting at chronological age with a **circle** as well as gestational age (age – number of weeks premature) with a **cross**. If plotted together, they should be joined by a line. An option should be offered to toggle between the plotted chronological, corrected ages and both.

!!! note "Gestation Age Correction through the life course"
    **The standard has recently changed** such that now gestational age is taken into account, even when born at gestational ages regarded as term,  and across the whole lifespan. This change was adopted because digital charting makes gestational age correction much easier to do, in fact it is now a completely automated process because of the the dGC API. (Note that this is different from paper charts, where gestational age correction was manual and therefore was only done up to 1 or 2 years depending on the degree of prematurity).

#### Examples

| Example Gestation | Old policy                                                       | New policy                                                                                                                           |
| ----------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 39 weeks 4 days   | Plot on 'Term' reference                                         | 'Term' reference has been abandoned in favour of plotting on UK90 preterm chart up till corrected gestational age of 42 weeks 0 days |
| 26 weeks 0 days   | Gestational age correction applied until 2 (corrected) years old | Correct for the whole life span                                                                                                      |
| 35 weeks 6 days   | Gestational age correction applied until 1 (corrected) year old  | Correct for the whole life span                                                                                                      |


Definitions:
Gestation at birth
Weeks premature
Gestational age
Chronological age

Gestational adjustment option provided for all birth gestations and continues indefinitely.

On a Z-score plot the gestationally adjusted Z-score should be plotted against actual (chronological) age with a label on the plot specifying the number of weeks premature.

## Essential standards for rendering

Whilst it is not essential to show the whole life course when plotting measurements against centile lines, the rendering of the centile lines and the plots must meet the following design standards.

- Centiles should be clearly labelled.

- Overlap between datasets for each centile should be clearly visible and no interpolation function should be used to attempt to link them.

- The 0.4th, 9th, 50th, 91st and, 99.6th centiles should all be dashed lines (**not** dotted, **not** continuous).

- The 2nd, 25th, 75th and 98th centiles should be continuous lines (thin).

- Axes should be clearly labelled (Height/Length in cm, Weight in kg, body mass index in kg/m2, head circumference in cm, age in years).

- X axis (age in years) increments should be monthly under the age of 2 y, 3 monthly over the age of 2 years.

- Measurements (height, weight, etc) should be to one decimal place.

- Centiles should be reported as integers, except if >99 or <1. If outside threshold, they should be reported as >99.6 or <0.4.

## The UK Nine centile chart format

The nine centile lines used in the British 1990 and UK-WHO charts are labelled in terms of rounded centiles (see table below) but they are precisely defined in terms of the underlying Zscores. The following Z score thresholds are used to define the centiles in the British charts.

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

## Definitions and terminology Centile Bands

A "centile space" is the distance between two centile lines. <br/>
A child is defined as being “on” a centile when within 0.17 SD (0.25 centile space) of the underlying exact Z-score, otherwise they are “between”.

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
| >99.6th      | 2.84            | 6               | Above normal range                      | severely obese           |
|              |                 | > 6             | Probable error                          | Probable error           |

*[BMI]: Body Mass Index
