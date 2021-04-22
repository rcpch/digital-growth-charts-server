# Chart Specifications

## Chart plotting

* Provide facility to toggle between height chart and weight chart or display together
* Offer option of BMI and head circumference charts for health staff use
* Allow the chart to be scaleable, i.e. zooming in or out, while maintaining variable, visible axes or offer a variety of age ranges displayed to optimise data view 
* Provide option of Z (SD) score plots for health staff use  (see below)
* Provide help / information facility to access instructions drawn from the RCPCH educational materials (see separate documents: information for parents, information for health staff)

### When plotting centile charts

Certain key presentation principles should be included:

* Use nine centile format (see below)
* Scale different elements of the chart to best display information in each period
* Use fortnightly grid points to 6 months, monthly thereafter
* Either show exact age and centile band (see below) when hovering over a point or show in an embedded table
* Data points should not be joined by lines
* There should be a toggle button to allow the user to see the chronological and corrected ages separately or together.
* Omit grid lines, which are only useful for manual plotting, and the Y axis can be inconspicuous

### When Plotting Z (SD) score charts

* Z score centile charts can be created with age on the X axis and Z score on the Y axis – this converts the centile curves to horizontal straight lines
* All available measurements (weight, height, head, BMI) should be plotted as series on the same chart with consistent colour coding of the different series (e.g. weight could always be red and height blue etc)
* The data points could be joined by fine lines
* The Y axis should cross the X axis at Z = 0 and have horizontal centile lines at intervals of 0.67 Z between -2.67 and 2.67

### Adjusting for Gestation at birth

On the centile chart it should be made clear that allowance has been made for varying age of gestation at birth by offering the option of plotting at chronological age with a circle as well as gestational age (age – number of weeks premature) with a cross. If plotted together they should be joined by a line. An option should be offered to toggle between the plotted chronological, corrected ages and both.

The standard has changed that now gestational age is taken into account even when term, across the lifespan.

Definitions:
Gestation at birth
Weeks premature
Gestational age
Chronological age

Gestational adjustment option provided for all birth gestations and continues indefinitely. 
Note this is different from paper charts

On a Z score plot the gestationally adjusted Z score should be plotted against actual (chronological) age with a label on the plot specifying the number of weeks premature.

## The UK Nine centile chart format

The nine centile lines used in the British 1990 and UK-WHO charts are labelled in terms of rounded centiles (see table below) but they are precisely defined in terms of the underlying Z scores. The following Z score thresholds are used to define the centiles in the British charts.

| Approximate centile | Exact Z score | Line format |
| ------------------- | ------------- | ----------- |
| 0.4th               |     -2.67     |   Dashed    |
| 2nd                 |     -2.00     | Continuous  |
| 9th                 |     -1.33     |    Dashed   |
| 25th                |     -0.67     | Continuous  |
| 50th                | 	  0	      |   Dashed    |
| 75th                | 	0.67      | Continuous  |
| 91st                | 	1.33	  |   Dashed    |
| 98th 	              |     2.00	  | Continuous  |
| 99.6th              | 	2.67	  |   Dashed    |

## Definitions and terminology Centile Bands

Within the normal range A child is defined as being “on” a centile when within 0.17 SD (0.25 centile space) of the underlying exact Z score, otherwise they are “between”.

|              |   SDS                     |  Additional Message  |                  |
|--------------|---------------------------|----------------------|------------------|
| Centile band | Lower limit | Upper limit | Weight/Height/Head	  |  BMI             |
|              |  <-6        |             |   Probable error                        |
| Below 0.4th  |  -6.00      | 	-2.84      | Below normal range   | Very thin        |
|       0.4th  |  -2.84      | 	-2.50      |                      | Low BMI          |
|   0.4th-2nd  |  -2.50      | 	-2.17      |                      | Low BMI          |
|         2nd  |  -2.17      | 	-1.83      |                      |                  |
|  2nd-9th     |  -1.83      | 	-1.50      |                      |                  |
|      9th     |  -1.50      | 	-1.16      |                      |                  |
|   9th-25th   |  -1.16      | 	-0.84      |                      |                  |
|   25th       |  -0.84      | 	-0.5       |                      |                  |
|   25th-50th  |  -0.50      | 	-0.17      |                      |                  |
|   50th       |  -0.17      | 	0.17       |                      |                  |
|   50th-75th  |  0.17       | 	0.50       | Below normal range   | Very thin        |
|     75th     |  0.5        | 	0.84       |                      | Low BMI          |
|   75th-91st  |  0.84       | 	1.16       |                      | Low BMI          |
|      91st    |  1.16       | 	1.50       |                      |                  |
|  91st-98th   |  1.50       | 	1.83       | Overweight           |                  |
|      98th    |  1.83       | 	2.17       | Overweight           |                  |
| 98th-99.6th  |  2.17       | 	2.50       | overweight(obese)    |                  |
|   99.6th     |  2.50       | 	2.84       | overweight(obese)    |                  |
|    >99.6th   |  2.84       |  6          |  Above normal range  | severely obese   |
|              |             |  > 6        | probable error       |                  |
