# Frequently Asked Questions


-----

## The Gestational Age Parameters and Gestational Age Correction

1. **Q**: Is entering a gestation age mandatory? from a DPCHR implementer perspective, if a birth notification has not flowed into the DPCHR, suppliers will need to require parents to enter it.  
**A**: Gestational age is **not** mandatory. If it is not supplied then the child will be assumed to be born at term (ie between 37 and 42 weeks) and for the UK-WHO charts, the standard term references will be used for calculations and charts.


1. **Q**: Is corrected age passed back by the API, or do implementers have to calculate it?  
**A**: Yes, corrected age is passed back by the API, if a gestational age is included in the request. The API can only correct for gestational age if a gestational age has been supplied. This correction is applied up to the corrected age of 1 year for preterm children born above 32 weeks, and to the corrected age of 2 years for preterm children born below 32 weeks.

-----

## Input Validation

1. **Q**: Does my application need to validate inputs?  
**A**: The API has validation and error handling for out-of-range requests, but it is good practice for the front-end software to also reject input values that are out of range since this feedback can be shown to the user, by the application.

1. **Q**: Is there a source from where we can get a list of extreme input values to use for our validation?  
**A**: Yes, we have included one in our source code: [Validation Constants ](https://github.com/rcpch/digital-growth-charts-server/blob/alpha/rcpchgrowth/rcpchgrowth/constants/validation_constants.py). This is what is used internally to validate API inputs and also used by the internal `rcpchgrowth` Python module to validate inputs to the `Measurement` class.

-----

## Growth Chart Questions

1. **Q**: If we have a calculated centile or SDS from the API then why do we need the traditional 'curved-lines' growth charts at all?  
**A**: The traditional growth charts were actually a form of paper calculator for the centile values. You plotted the age and the height/weight data and you then looked for which centile lines it was between, and this was the read-off data.  
The Growth Charts API obviates the need for this step since we calculate the cnetiles for you. However, another important function of the chart was to visualise trends in the growth. Our API does not do this, so there will be a need for some form of chart to visualise the trend.  
Initially we expect people will want to use the traditional growth chart, out of simple familiarity. But in time we think that researchers may develop better visualisations of the trend in centiles/SDS that don't have to come on such confusing curvy charts.

-----

## Plotting and displaying charts

1. **Q**: Would it be good enough to plot the returned centile values on a pre-prepared **image** of a growth chart?  
**A**: Maybe. Images of charts are definitely **not** good enough for calculating a centile from, although many GP software packages do it this way, it's poor practice and it's why the API needed to exist in the first place. BUT, since we are  calculating the centiles for you, then the chart is only for displaying the trend. An image **could** be used, but we would advise against it generally.  
The problem with images is that it is very easy to accidentally have an offset or scaling error that means that *some* plotted points are in the right place, and some are not. Best practice is always to use the **same** vector graphic tooling to both construct the lines *and* plot the points, to avoid offsets/scaling inaccuracy. If you are using an image (please don't) then you must ensure you're selecting the correct one for the data you're presenting, and that the scaling and offset is not just programmed to be correct, but clinically tested to be correct!