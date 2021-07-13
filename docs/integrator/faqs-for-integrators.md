---
title: FAQs for Integrators
reviewers: Dr Marcus Baw
---

# FAQs for Integrators

In our documentation we have used the term **Integrator** to refer to a person or team who is integrating the API into a product or service. We also recognise the term 'customer'. This is to distinguish Integrators from 'clients' (by which *we* mean software which consumes the API), and 'developers' (by whom *we* mean those who are developing the Digital Growth Charts project)

> [Information about the dGC client products](../products/products-overview.md)

> [Information for dGC Developers](../developer/start-here.md)

## Q: Can we self-host the API?

**A**: Technically yes. However there are several important considerations which we believe would more than negate any saving made.

We have open sourced the API in order to align with our policy on transparency and clinical safety, however we advise that you do not self host it. Only the version deployed and managed by the RCPCH team is warranted to be correct.

--8<--
docs/_assets/_snippets/self-host-warning.md
--8<--


!!! tip "RCPCH On-Premise Hosting Service"
    The RCPCH offers an 'on-premise' managed service which may suit some customers requiring the service to be hosted within their own data centre, or on their own cloud infrastructure. **LINK TO PRICING**



By using the RCPCH-provided API you avoid all that requirement and use our commodity server.

## Q: Is entering a gestational age mandatory?

**A**: Gestational age is **not** mandatory for the API to return a value. If it is not supplied then the child will be assumed to be born at 40 weeks and therefore for the UK-WHO charts, the standard term references will be used for calculations and charts.

From a DPCHR implementer perspective, if a birth notification has not flowed into the DPCHR, suppliers will need to require parents to enter it.

* [DPCHR]: Digital Paediatric Child Health Record
* [DCB0129]: (Data Coordination Board) Standard 0129
* [DCB0160]: (Data Coordination Board) Standard 0160

## Q: What development effort is required to integrate this API into an app or Electronic Patient Record?

**A**: Minimal development is required. The tricky stuff (calculating centiles from complex statistical tables, selecting the correct UK90 or WHO references for age, and gestational age correction) is all done for you. The data returned will be the correct centiles, which can be displayed to the user.

Producing a visual ‘growth chart’ with this data on is a little more involved, however we have tried to make the process as easy as possible by building API endpoints which return the coordinate data from which to build the chart lines, and also we’ve made an open source library which takes that source data and makes a chart for you. It’s built in React and is MIT licensed, but if you are using another technology then you can inspect the source and use that to build your own client.

We are keen to build a ‘catalogue’ of chart clients so other open source clients are very welcome and we will help you build and test them!

## Q: Is corrected gestational age passed back by the API, or do implementers have to calculate it?  

**A**: Yes, corrected age is passed back by the API, if a gestational age is included in the request.

!!! warning
    The API can only correct for gestational age if a gestational age has been supplied!

This correction is applied up to the corrected age of 1 year for preterm children born above 32 weeks, and to the corrected age of 2 years for preterm children born below 32 weeks, which is accepted standard practice among paediatricians.

## Q: Does my application need to validate inputs?

**A**: The API has validation and error handling for out-of-range requests, but it is good practice for the front-end software to also reject input values that are out of range since this feedback can be shown to the user, by the application.

## Q: Is there a source from where we can get a list of extreme input values to use for our validation?

**A**: Yes, we have included one in our source code: [Validation Constants](https://github.com/rcpch/digital-growth-charts-server/blob/alpha/rcpchgrowth/rcpchgrowth/constants/validation_constants.py). This is what is used internally to validate API inputs and also used by the internal `rcpchgrowth` Python module to validate inputs to the `Measurement` class.

## Q: Would it be good enough to plot the returned centile values on a pre-prepared **image** of a growth chart?  

**A**: Maybe. It would depend on the implementation.

Images of charts are definitely **not** good enough for calculating a centile from, although many GP software packages do it this way, it's poor practice and it's why the API needed to exist in the first place. BUT, since we are  calculating the centiles for you, then the chart is only for displaying the trend. An image **could** be used, but we would advise against it generally.

The problem with images is that it is very easy to accidentally have an offset or scaling error that means that *some* plotted points are in the right place, and some are not. Best practice is always to use the **same** vector graphic tooling to both construct the lines *and* plot the points, to avoid offsets/scaling inaccuracy. If you are using an image (please don't) then you must ensure you're selecting the correct one for the data you're presenting, and that the scaling and offset is not just programmed to be correct, but clinically tested to be correct!
