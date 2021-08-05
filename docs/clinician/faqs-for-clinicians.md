---
title: FAQs for Clinicians
reviewers: Dr Marcus Baw
---

# Frequently Asked Questions for Clinicians

## Q: What are the main differences between the old paper or PDF Growth Charts and the dGC Project?

**A**: Paper or PDF charts required a human to plot the measurement and then read off the Centile. Digital Growth Charts automatically calculate Centiles and SDS (Standard Deviation Score) from the measurements, and plot these on a digital chart for you.

Digital Growth Charts include recommended SNOMED-CT clinical terminology to guide persistence of the returned values

## Q: How do I get the RCPCH Digital Growth Charts in my EPR?

**A**: As a first step, we would suggest to discuss with the CIO (Chief Information Officer) and CCIO (Chief Clinical Information Officer) at your trust, or their equivalents in your place of work.

Hopefully this can lead on to further discussion with the IT team at your place of work, which should hopefully establish lines of communication with the supplier of the Electronic Patient Record (EPR).

Many EPR suppliers will have already started the process of integrating the RCPCH dGC API into their product, and we are happy to assist vendors with integration once they purchase a subscription.

## Q: How much do the RCPCH dGC APIs cost?

**A**: The APIs themselves are run on a sustainable non-profit basis by the RCPCH, which is a charitable organisation. The aim is for modest revenues from the API to be fed back into development of future APIs and new features.

Pricing tiers for the API are shortly to be published, and usually the EPR vendor or integration service would pay for this directly, however the costs are likely to be passed on to you, the customer.

Pricing depends on the volume of requests that the vendor requires and the amount of support they need.

The process of integrating the API into an existing EPR product is technically straightforward and the amount of work is modest. EPR suppliers may of course levy a fee for this additional integration work, however once this has been done once for a product, there should be minimal or zero additional work to roll out to other sites, so you should check whether the vendor has already deployed the dGC elsewhere.

## Q: Can I try out the dGC APIs?

**A**: Yes, you can use the demo site at <https://growth.rcpch.ac.uk/> to evaluate the service.

## Q: If we have a calculated centile from the API then why do we need the traditional 'curved-lines' growth charts at all?  

**A**: Good question. Maybe, in time, this style of chart will no longer be needed. Maybe in time they will be replaced by SDS charts, which would allow us to view height, weight, head circumference, and BMI all on one chart too!

The traditional growth charts were actually a form of 'paper calculator' for the centile values. The clinician plotted the age and the height/weight data and then looked for which centile lines it was between, and this was the data that the clinician read off and recorded. We would also keep the charts for future plotting.

The Growth Charts API obviates the need for this step since **we** calculate the centiles for you. However, another important function of the chart was to visualise **trends** in the growth. Our API does not do this, so there will be a need for some form of chart to visualise the trend.

Initially we expect that clinical users will want to see the traditional growth chart, out of simple familiarity. But in time we think that researchers may develop better visualisations of the trend in centiles/SDS that don't have to come on such confusing curvy charts. The future of displaying growth trends is entirely open to new ideas and innovation.

## Q: Where can I see your clinical safety documentation?

**A**: Our clinical safety documentation is completely open and public, and is all under the [Safety](../safety/overview.md) tab within this documentation site. Feedback is welcome - contact [growth.digital@rcpch.ac.uk](mailto:growth.digital@rcpch.ac.uk) including 'Clinical Safety:' in the subject for ease of routing to the Clinical Safety Officer. Alternatively you can [create an Issue in the documentation site source code on GitHub](https://github.com/rcpch/digital-growth-charts-documentation/issues), or talk to us on our [Forum](https://openhealthhub.org/c/rcpch-digital-growth-charts).


