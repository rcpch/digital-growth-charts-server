# Calculating Growth Parameters - WIP

This page is to document the gotchas and difficulties that arise when doing Centiles etc in code /
clinico-statistical centiles gotchas that we've had to work through.

- cubic interpolation
- term dates averaging
- age thresholds for different measurements begin and end at different ages

## Gold Standard

The current 'gold standard' for LMS calculation is [LMS Growth](https://www.healthforallchildren.com/shop-base/shop/software/lmsgrowth/), an Excel add-in written in Visual Basic by Huiqi Pan and Tim Cole (copyright Medical Research Council 2002–10).

Results from RCPCHGrowth agree with LMS Growth to 3 decimal places, though beyond this there are discrepancies. Part of the reason for this relates to the decimal age calculation - in LMS Growth months and weeks are handled differently to RCPCHGrowth which uses the python date-utils library to calculate differences between dates.

### Interpolation

The logic involves .. steps:

1. Calculate decimal age in years (age in days / 365.25, to account for leap years)
2. Look up nearest decimal ages in the reference data and read off associated L, M and S values.
3. Substitute L, M and S in the final equation to generate an SDS.

In most situations the decimal age of the index child falls between decimal ages in the reference data. If that is the case, an interpolation needs to be performed on the ages either side of the child's age, and the same applied in turn to the L, M and S values associated with each of the ages below and above.

#### Cubic Interpolation

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

#### Linear Interpolation

It is not always possible to perform cubic interpolation. Where a child's measurement falls close to a reference threshold, there may not be two ages below or above them, and in these situations linear interpolation is used. Linear interpolation requires only one decimal age below and above the child's age. Here, the interp1d function from the [Scipy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html) has been used to keep code less verbose.

### Reference Thresholds

It is documented in several places how there are age thresholds for different measurements.
This is either due to a lack of measurements, or an overlap in references. Because the different datasets overlap, there is a certain amount of logic throughout the functions to ensure that the correct reference is selected. The threshold are:

- length runs from 25 weeks to 2 years. There is overlap here where children are measured standing, not lying, and therefore 2 LMS values for the same age. The functions have a `default_to_youngest_reference` flag which by default is false. From 2 years, the data continues as height to 4 years where again there are 2 values. This is the join between the WHO 2006 and older UK90 data. Again here, default is to the older reference, but this can be overridded by the user if they wish. Length/Height appears as such on charts, and can be found simply as `'height'` as a parameter for simplicity.
- weight appears as `'weight'` as a parameter and is continuous from 23 weeks gestation through to 20 y for both sexes. There are overlaps as with height, between UK90 preterm, UK-WHO infant and child and again UK90 child datasets.
- BMI appears as `'bmi'` as a paramater and is a calculated value requiring height in metres and weight in kilograms, expressed as kg/m². Reference data for BMI are available from 2 weeks of age in the UK-WHO dataset, up to 20 years. Overlaps, as with height and weight, exist at 2 and 4 years.
- Head circumference is referred to as occipitofrontal circumference and appears as an `'ofc'` parameter. Reference data exist for both sexes from 23 weeks gestation to 17 years in girls, and 18 years in boys. There are overlaps as above where datasets meet.

#### Prematurity and Term

An infant is considered premature if born below 37 weeks gestation. The limits of viability may stretch occasionally below 23 weeks, the reference data stops here. It is important to note that at this very young age reference data on length do not exist until the infant is 25 weeks gestation, or 42 weeks gestation in the case of BMI. For babies born premature, a gestation is provided in weeks and supplemental days, which together with the birth and measurement dates, can be used to calculate a corrected decimal age. Correction continues from delivery in those born premature up until their first birthday (if 33 weeks and above) or their second birthday if more premature. The reference data for these are found in the `uk_who_0_20_preterm.json` file.

Term (37-42 weeks) is reported as a decimal age of 0 y and the Growth Chart Reference Group at the inception of the UK-WHO paper charts had previously stipulated that no growth data should be reported over the 2 week period after delivery in term infants. This same guidance has been followed here. The reason for this is that measurements of length are often inaccurate in newborn babies, the caput swelling and overriding sutures from delivery make head circumference (occipitofrontal circumference) similarly unreliable, and infants typically lose upto 10% of their birth weight physiologically in the first two weeks following delivery - their birthweight often representing fluid retained from pregnancy. For these reasons, babies born between 37 and 42 weeks all receive a decimal age of 0 at birth, for which there is only one L, M and S value, which represents a mean average of all the values for L, M and S between 37 and 42 weeks. These data are found in the `uk_who_0_20_term.json` file.

It should be noted that once a term infant is beyond 2 weeks of age, the reference data is picked up in the `uk_who_0_20_preterm.json` file which runs through to 20y. This is perhaps confusing, given the name, but breaking the data into a separately named file, purely for semantic clarity, added extra steps and so has been left in a single file for convenience.

## Other packages

Ours is not the only open source project to perform these calculations - there are others on [PyPi](https://pypi.org/), and other implementation in other programming languages. There are also standalone software packages such as [iGrow](https://www.igrow-software.com/) which exist as off the shelf solutions.

RCPCHGrowth has the benefit of being commissioned by NHS England, built by programmers and paediatric doctors/general practitioner with expertise in software development, and tested with the oversight of the team that set the original growth chart standards over the last 40 years. The project is available and open source here, overseen and maintained by the Royal College of Paediatrics and Child Health.

The clinical board and development team welcome support from users in maintaining the repositories, and actively encourage users to post issues they find on [Github](https://github.com/rcpch/digital-growth-charts-server/issues) or submit pull requests.

## Helpful reference documents for understanding what Centiles are, how they are calculated, and how they are used

- https://www.openhealthhub.org/t/centile-part-1-what-are-centiles/463
- https://www.cdc.gov/growthcharts/percentile_data_files.htm
- https://www.cdc.gov/nchs/data/nhsr/nhsr063.pdf
