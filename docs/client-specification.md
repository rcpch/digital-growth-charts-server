# Client Specification

## Background

**A requirement of the licence for the API is that any charts rendered must meet these standards as agreed by the digital growth chart project board. A large amount of documentation has been produced to guide the design and rendering of UK growth charts.**

The UK growth charts are made up of 4 datasets taken from 2 growth references (see clinical documentation for more detail).

- The UK90 preterm dataset runs from 23 weeks gestation to 42 weeks postmenstrual age as length (from 25 weeks), weight and head circumference.
- The WHO 2006 dataset runs from 2 weeks of age to 2 years of age as length, weight, BMI and head circumference.
- The WHO 2006 dataset continues as height (now measured standing) to 4 years of age
- The UK90 dataset picks up until 20y (head circumference to 17 in girls and 18 y in boys)

## Implications for charting digitally

These datasets all overlap, and therefore when plotting them, they must be passed to charting packages as individual series. This means they will appear as discontinuous, with breaks in the lines where they meet/overlap.

- There is a natural step at each of these time points which must be respected. If all 4 datasets are presented 0-20y as a continuous dataset, chart packages will interpolate the gaps and the intentional 'step' will be lost.

- The api endpoint returns the chart data in an array of arrays. The first level array represents the 9 centiles [0.4, 2, 9 , 25, 50, 75, 91, 98, 99.6], with each centile in turn having a nested array of 4 arrays of data, one for each dataset (see below). The individual data points are reported as float values for x and y coordinates. X corresponds to decimal age, y to the measurement value of the chart requested.

- The chart data is only returned for the measurement method requested - if only height is supplied, only height centile data will be returned.

- In addition to the centile data, the growth data presented to the endpoint in the request are returned as an array of x and y values.

## Essential standards for rendering

Whilst it is not essential to show the whole life course when plotting measurements against centile lines, the rendering of the centile lines and the plots must meet the following design standards.

- Centiles should be clearly labelled
- Overlap between datasets for each centile should be clearly visibile and no interpolation function should be used to attempt to link them
- The 0.4th, 9th, 50th, 91st and, 99.6th centiles should all be dashed lines (not dotted, not continuous)
- The 2nd, 25th, 75th and 98th centiles should be continuous lines (thin)
- Axes should be clearly labelled (Height/Length in cm, Weight in kg, body mass index in kg/m2, head circumference in cm, age in years)
- X axis (age in years) increments should be monthly under the age of 2 y, 3 monthly over the age of 2 years.
- Measurements should be to one decimal place.
- Centiles should be reported as integers, except if >99 or <1. If outside threshold, they should be reported as >99.6 or <0.4.
