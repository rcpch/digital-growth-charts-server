---
title: FAQs for Clinicians
reviewers: Dr Marcus Baw, Dr Anchit Chandran
audience: clinicians, health-staff
---

# Frequently Asked Questions for Clinicians

## Q: What are the main differences between the old paper or PDF Growth Charts and the dGC Project?

**A**: Paper or PDF charts required a human to plot the measurement and then read off the Centile. Digital Growth Charts automatically calculate Centiles and SDS (Standard Deviation Score) from the measurements, and plot these on a digital chart for you.

Digital Growth Charts include recommended SNOMED-CT clinical terminology to guide persistence of the returned values.

## Q: How do I get the RCPCH Digital Growth Charts in my EPR?

**A**: As a first step, we would suggest initial discussions with the CIO (Chief Information Officer) and CCIO (Chief Clinical Information Officer) at your trust, or their equivalents in your place of work.

Hopefully, this leads to further discussion with the IT team at your place of work, and establishing lines of communication with the supplier of the Electronic Patient Record (EPR).

Many EPR suppliers have already started the process of integrating the RCPCH Digital Growth Charts API into their product, and we are happy to assist vendors with integration once they purchase a subscription. The more clinicians who are asking for Digital Growth Charts, the more likely it is that suppliers will prioritise this essential part of digital transformation.

!!! info
    We now have a section on the RCPCH Forum for supporting clinicians wanting to get Digital Growth Charts implemented in their EPR. To get access to this area sign up to the forum site and request access to our [Digital Growth Charts Clinicians](https://forum.rcpch.tech/g/dgc-clinicians)

## Q: How much do the RCPCH Digital Growth Charts APIs cost?

**A**: The APIs themselves are run on a sustainable non-profit basis by the RCPCH, which is a charitable organisation. The aim is for modest revenues from the API to be fed back into development of future APIs and new features.

Pricing tiers for the API are [available on the RCPCH website](https://www.rcpch.ac.uk/resources/growth-charts/digital/about#subscriptions-and-pricing). Usually, the EPR vendor or integration service would pay directly, however the costs are likely to be passed on to you, the customer.

Pricing depends on the volume of requests the vendor requires and the amount of support they need.

The process of integrating the API into an existing EPR product is technically straightforward and the amount of work is modest. EPR suppliers may levy a fee for this additional integration work, however after being done once for a product, there should be zero to minimal additional work rolling out to other sites, so you should check whether the vendor has already deployed the dGC elsewhere.

## Q: Can I try out the Digital Growth Charts APIs?

**A**: Yes, you can use the demo site at <https://growth.rcpch.ac.uk/> to evaluate the service.

## Q: If we have a calculated centile from the API, then why do we need the traditional 'curved-lines' growth charts at all?

**A**: Good question. Maybe, this style of chart will no longer be needed in the future. Perhaps they will be replaced by SDS charts, which would allow us to view height, weight, head circumference, and BMI all on one chart too!

The traditional growth charts were actually a form of 'paper calculator' for the centile values. The clinician plotted the age, height/weight data, and then looked for which centile lines it was between: this was the data read off and recorded. We would also keep the charts for future plotting.

The Growth Charts API removes the need for this step, since **we** calculate the centiles for you. However, another important function of the chart was to visualise **trends** in the growth. Our API does not do this, so there will be a need for some form of chart to visualise the trend.

Initially, we expect that clinical users will want to see the traditional growth chart, out of simple familiarity. But in time, researchers may develop better visualisations of the trend in centiles/SDS, which don't necessitate such confusing curvy charts. The future of displaying growth trends is entirely open to new ideas and innovation.

## Q: Where can I see your clinical safety documentation?

**A**: Our clinical safety documentation is completely open and public, and is all in the [Clinical Safety](../safety/overview.md) section.

Feedback is welcome: contact [growth.digital@rcpch.ac.uk](mailto:growth.digital@rcpch.ac.uk), including "*Clinical Safety:*" in the subject for ease of routing to the Clinical Safety Officer. Alternatively, you can [create an Issue in the documentation site source code on GitHub](https://github.com/rcpch/digital-growth-charts-documentation/issues), or talk to us on our [Forum](https://forum.rcpch.tech/).
