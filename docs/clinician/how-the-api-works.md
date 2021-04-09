# How the API Works

Details for interested clinicians and statisticians

## Growth Charting Introduction

The UK-WHO 0-4 year old charts were officially launched on May 11th 2009. Any child born after that date should be plotted on a UK-WHO growth chart. Children born before May 11th 2009 are plotted on British 1990 (UK90) charts and subsequent measurements must be plotted using those charts. After age 4 the two charts are the same.

## The LMS Method

It is now common practice to express child growth status in the form of SD scores - the number of standard deviations away from the mean (also known as a z-score). The SD score can be converted to a centile.

The LMS method provides a way of obtaining normalized growth centiles from a relatively small original dataset, applying smoothing and extrapolation such that the resulting L, M and S curves contain the information to draw **any** centile curve, and to convert measurements (even extreme values) into exact SD scores. The growth reference is summarised by a table of LMS values at a series of ages.

### How the LMS method is used

- Look up in the LMS table for the relevant measurement (e.g. height) the age and sex-specific values of L, M and S for the child. If the child's age falls between the tabulated ages, use cubic interpolation to obtain values for the child's exact age.

- To obtain the z-score, plug the LMS values with the child's measurement into the formula:
  ![formula](https://latex.codecogs.com/svg.latex?\=z={[(Measurement / M)-1] \over L S})

## Growth References

This is a growing list of growth references for children. These cover a number of specific medical conditions as well as a range of different physiological parameters. It will continue to be added to as the data become available. As a side-project of this work we are interested in collating an international library of growth references in computable format, which is at https://github.com/rcpch/growth-references and further details are available in that repository.

If you have a reference which you would like us to add, please contact us on growth.digital@rcpch.ac.uk


## Gold Standard

The preceding 'gold standard' for LMS calculation was [LMS Growth](https://www.healthforallchildren.com/shop-base/shop/software/lmsgrowth/), an Excel add-in written in Visual Basic by Huiqi Pan and Tim Cole (copyright Medical Research Council 2002–10).

Results from RCPCHGrowth agree with LMS Growth to 3 decimal places, though beyond this there are discrepancies. Part of the reason for this relates to the decimal age calculation - in LMS Growth months and weeks are handled differently to RCPCHGrowth which uses the python date-utils library to calculate differences between dates.

## Interpolation

The process involves the following steps:

1. Calculate decimal age in years (age in days / 365.25, to account for leap years)
2. Look up nearest decimal ages in the reference data and read off associated L, M and S values.
3. Substitute L, M and S in the final equation to generate an SDS.

In most situations, the decimal age of the child falls *between* the available decimal ages in the reference data. If that is the case, an *interpolation* needs to be performed on the ages either side of the child's age, and the same applied in turn to the L, M and S values associated with each of the ages below and above.

### Cubic Interpolation

In most circumstances _cubic_ interpolation is used - this involves identifying 2 ages below and 2 ages above the child's age and substitution the following equation:

If _t₀_, _t₁_, _t₂_, _t₃_, _y₀_, _y₁_, _y₂_, _y₃_, are given, and _t₀_<_t₁_<_t₂_<_t₃_, _t_ is in the range of [*t₁*, *t₂*], the cubic interpolation of _y_ for _t_ is:

<img src="https://latex.codecogs.com/svg.latex?\inline&space;\bg_white&space;\large&space;y=\frac{y_{0}(t-t_{1})(t-t_{2})(t-t_{3})}{(t_{0}-t_{1})(t_{0}-t_{2})(t_{0}-t_{3})}&space;&plus;&space;\frac{y_{1}(t-t_{0})(t-t_{2})(t-t_{3})}{(t_{1}-t_{0})(t_{1}-t_{2})(t_{1}-t_{3})}&space;&plus;&space;\frac{y_{2}(t-t_{0})(t-t_{1})(t-t_{3})}{(t_{2}-t_{0})(t_{2}-t_{1})(t_{2}-t_{3})}&plus;\frac{y_{3}(t-t_{0})(t-t_{1})(t-t_{2})}{(t_{3}-t_{0})(t_{3}-t_{1})(t_{3}-t_{2})}" title="\large y=\frac{y_{0}(t-t_{1})(t-t_{2})(t-t_{3})}{(t_{0}-t_{1})(t_{0}-t_{2})(t_{0}-t_{3})} + \frac{y_{1}(t-t_{0})(t-t_{2})(t-t_{3})}{(t_{1}-t_{0})(t_{1}-t_{2})(t_{1}-t_{3})} + \frac{y_{2}(t-t_{0})(t-t_{1})(t-t_{3})}{(t_{2}-t_{0})(t_{2}-t_{1})(t_{2}-t_{3})}+\frac{y_{3}(t-t_{0})(t-t_{1})(t-t_{2})}{(t_{3}-t_{0})(t_{3}-t_{1})(t_{3}-t_{2})}" />

_dt_ = (*t-t*₁)/0.5
<img src="https://latex.codecogs.com/svg.latex?\inline&space;\large&space;a_{0}=-\frac{y_{0}}{6}&plus;\frac{y_{1}}{2}-\frac{y_{2}}{2}&plus;\frac{y_{3}}{6}" title="\large a_{0}=-\frac{y_{0}}{6}+\frac{y_{1}}{2}-\frac{y_{2}}{2}+\frac{y_{3}}{6}" />
<img src="https://latex.codecogs.com/svg.latex?\inline&space;\large&space;a_{1}=\frac{y_{0}}{2}-y_{1}&plus;\frac{y_{2}}{2}" title="\large a_{1}=\frac{y_{0}}{2}-y_{1}+\frac{y_{2}}{2}" />
<img src="https://latex.codecogs.com/svg.latex?\inline&space;\large&space;a_{2}=-\frac{y_{0}}{3}-\frac{y_{1}}{2}&plus;&space;y_{2}-\frac{y_{3}}{6}" title="\large a_{2}=-\frac{y_{0}}{3}-\frac{y_{1}}{2}+ y_{2}-\frac{y_{3}}{6}" />
_a₃_ = _y₁_
y=a*{0}dt^{3}+a*{1}dt^{2}+a\_{2}dt+a^{3}

**Note: this derived formula is equivalent to the above cubic interpolation only when the age interval is 0.5.**

Alternatively, it is possible to use the CubicSpline function from the SciPy interpolate package, or the interpolate.splev function - details can be found in the comments in the sds_calculations.py module. In testing our findings were that the original Cole method above ran faster than the Scipy interpolate functions with the same level of accuracy.

### Linear Interpolation

It is not always possible to perform cubic interpolation. Where a child's measurement falls close to a reference threshold, there may not be two ages below or above them, and in these situations linear interpolation is used. Linear interpolation requires only one decimal age below and above the child's age. Here, the interp1d function from the [Scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html) has been used to keep code less verbose.

## Reference Thresholds

It is documented in several places how there are age thresholds for different measurements.

This is either due to a lack of measurements, or an overlap in references. Because the different datasets overlap, there is a certain amount of logic throughout the functions to ensure that the correct reference is selected. The threshold are:

- length runs from 25 weeks to 2 years. There is overlap here where children are measured standing, not lying, and therefore 2 LMS values for the same age. The functions have a `default_to_youngest_reference` flag which by default is false. From 2 years, the data continues as height to 4 years where again there are 2 values. This is the join between the WHO 2006 and older UK90 data. Again here, default is to the older reference, but this can be overridded by the user if they wish. Length/Height appears as such on charts, and can be found simply as `'height'` as a parameter for simplicity.
- weight appears as `'weight'` as a parameter and is continuous from 23 weeks gestation through to 20 y for both sexes. There are overlaps as with height, between UK90 preterm, UK-WHO infant and child and again UK90 child datasets.
- BMI appears as `'bmi'` as a paramater and is a calculated value requiring height in metres and weight in kilograms, expressed as kg/m². Reference data for BMI are available from 2 weeks of age in the UK-WHO dataset, up to 20 years. Overlaps, as with height and weight, exist at 2 and 4 years.
- Head circumference is referred to as occipitofrontal circumference and appears as an `'ofc'` parameter. Reference data exist for both sexes from 23 weeks gestation to 17 years in girls, and 18 years in boys. There are overlaps as above where datasets meet.

## Prematurity and Term

An infant is considered premature if born below 37 weeks gestation. The limits of viability may stretch occasionally below 23 weeks, the reference data stops here. It is important to note that at this very young age reference data on length do not exist until the infant is 25 weeks gestation, or 42 weeks gestation in the case of BMI. For babies born premature, a gestation is provided in weeks and supplemental days, which together with the birth and measurement dates, can be used to calculate a corrected decimal age. Correction continues from delivery in those born premature up until their first birthday (if 33 weeks and above) or their second birthday if more premature. The reference data for these are found in the `uk_who_0_20_preterm.json` file.

### Removal of Term Dates Averaging

The entire Term period (from 37-42 weeks gestation) used to be defined as a decimal age of exactly 0 years, and the Growth Chart Reference Group at the inception of the UK-WHO paper charts had previously stipulated that no growth data should be reported over the 2 week period after delivery in term infants.

The growth chart reference data covering this Term period used to be averaged across the period, so that regardless of actual gestational age, all Term-born children were considered to be the same, for paper and PDF growth charts.

However, during the development of the Digital Growth Charts, the [dGC Project Board]() determined that since there is now evidence that there *is* a difference between the outcomes of children born at different extremes of the Term period, and also since the dGC makes it easy to correct for all gestational ages, that we should abolish the 'averaging' effect of the concept of Term, and simply correct all children for gestational age.


### Helpful reference documents for understanding what Centiles are, how they are calculated, and how they are used

- https://www.openhealthhub.org/t/centile-part-1-what-are-centiles/463
- https://www.cdc.gov/growthcharts/percentile_data_files.htm
- https://www.cdc.gov/nchs/data/nhsr/nhsr063.pdf
- [The development of growth references and growth charts - T J Cole](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3920659/)
