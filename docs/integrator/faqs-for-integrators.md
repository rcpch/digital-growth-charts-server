---
title: FAQs for Integrators
reviewers: Dr Marcus Baw, Dr Anchit Chandran
audience: integrators, implementers, technical-architects
---

# FAQs for Integrators

In our documentation, we use the term **Integrator** to refer to a person or team who is integrating the API into a product or service. We also recognise the term 'customer'. This distinguishes 'Integrators' from 'clients' (by which *we* mean software which consumes the API), and 'developers' (by whom *we* mean those who are developing the Digital Growth Charts project)

> [Information about the dGC client products](../products/products-overview.md)
>
> [Information for dGC Developers](../developer/start-here.md)

## Q: Can we self-host the API?

**A**: Technically yes. However, there are several important considerations, of which the downsides outweigh any benefits.

We have open-sourced the API to align with our policy on transparency and clinical safety. However, we advise you do not self-host it. Only the version deployed and managed by the RCPCH team is warranted to be correct.

--8<--
docs/_assets/_snippets/self-host-warning.md
--8<--

!!! tip "RCPCH On-Premise Hosting Service"
    The RCPCH offers an 'on-premise' managed service which may suit some customers requiring the service to be hosted within their own data centre, or on their own cloud infrastructure. Find out more about [pricing](https://www.rcpch.ac.uk/resources/growth-charts/digital/about#subscriptions-and-pricing).

By using the RCPCH-provided API, you avoid all that requirement and use our commodity server.

## Q: Is entering a gestational age mandatory?

**A**: Gestational age is **not** mandatory for the API to return a value. If not supplied, the child will be assumed to be born at 40 weeks. For the UK-WHO charts, the standard term references will be used for calculations and charts.

From a DPCHR implementer perspective, if a birth notification has not flowed into the DPCHR, suppliers will need to require parents to enter it.

* [DPCHR]: Digital Paediatric Child Health Record
* [DCB0129]: (Data Coordination Board) Standard 0129
* [DCB0160]: (Data Coordination Board) Standard 0160

## Q: What development effort is required to integrate this API into an app or Electronic Patient Record?

**A**: Minimal development is required. The tricky stuff (calculating centiles from complex statistical tables, selecting the correct UK90 or WHO references for age, and gestational age correction) is all done for you. The data returned will be the correct centiles, which can be displayed to the user.

Producing a visual ‘growth chart’ with this data is a little more involved, however, we have simplified the process by building API endpoints which return coordinate data from which to build the chart lines. We’ve also made an open-source library which takes that source data and makes a chart for you. This is built in React and is MIT licensed, but if you are using another technology, you can inspect the source to build your own client.

We are keen to build a ‘catalogue’ of chart clients, so other open-source clients are very welcome. We will also help you build and test them!

## Q: Is corrected gestational age passed back by the API, or do implementers have to calculate it?

**A**: Yes, corrected age is passed back by the API, if a gestational age is included in the request.

**NOTE: The API can only correct for gestational age if a gestational age has been supplied!**

This correction is applied up to the corrected age of 1 year for preterm children born above 32 weeks, and to the corrected age of 2 years for preterm children born below 32 weeks, which is accepted standard practice among paediatricians.

## Q: Does my application need to validate inputs?

**A**: The API has validation and error handling for out-of-range requests, but it is good practice for the front-end software to also reject input values outside the valid range since the user will receive immediate feedback from your application.

## Q: Is there a source from where we can get a list of extreme input values to use for our validation?

**A**: Yes, we have included one in our source code: [Validation Constants](https://github.com/rcpch/rcpchgrowth-python/blob/live/rcpchgrowth/constants/validation_constants.py). This is used internally to validate API inputs, as well as by the internal `rcpchgrowth` Python module to validate inputs to the `Measurement` class.

## Q: Would it be good enough to plot the returned centile values on a pre-prepared **image** of a growth chart?

**A**: Maybe. It would depend on the implementation.

Images of charts are definitely **not** good enough for calculating a centile from, although many GP software packages do it this way. It is poor practice, and it's why the API needed to exist in the first place. However, since we are calculating the centiles for you, the chart is only for displaying the trend. An image **could** be used, but we generally advise against it.

It is very easy to accidentally offset or incorrectly scale images, leading to *some* correctly plotted points, but others not. The best practice is to always use the *same* vector graphic tooling to both construct lines **and** plot the points, avoiding offsets/scaling inaccuracy. If you use an image (against our advice), you must ensure the correct one is selected for the presented data. More, you must ensure scaling and offset are not just programmed to be correct, but also clinically tested to be correct!
