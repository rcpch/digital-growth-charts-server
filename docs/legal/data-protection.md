---
title: Data Protection
reviewers: Dr Marcus Baw
---

# Data Protection Considerations

## For the dGC API Server

The dGC server API and the service we provide around it has been designed with privacy and information security in mind.

### Anonymous Requests

The data that is sent to our server does not contain any identifiers such as patient name, NHS number or other numeric identifier, address data. It does contain date of birth because this is required to calculate the age of the patient, but this is not saved to the server.

### What does 'Stateless API' mean?

The term 'State' in computing is equal to 'saved data'. In computing terminology, if an application is 'State*ful*' it means it saves some information on the server between two requests to the server. A system that is 'state*less*' does not save any data.

The dGC API is 'Stateless' by design, meaning it does **not** persist information between the web requests that are made of it. Each request from the API-consuming application to our API contains all the information required to calculate a set of centile data. The response we send back contains this data, and it is never saved on the server. Some information about requests is kept for a 72 hours in the logs of our server, to enable us to monitor performance and to debug problems, however this information is anonymous.

### Persistence of results in Medical Records

Any 'persistence' (data saving) must happen in **the application which is consuming the API**, which is the natural place to persist data anyway, since this is the DPCHR, the GP system, the hospital EPR - which already likely persists lots of data about the patient.

### Data Protection Impact Assessment & ICO

In view of the stateless nature of the server, we don't handle any Patient Identifiable Data. We have reviewed the privacy implications of our application and believe it does not require a Data Privacy Impact Assessment, according to our review of [current Information Commissioner's Office guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-impact-assessments/#dpia3).

## For the dGC API Service provided by the RCPCH

The API 'service wrapper' collects the essential minimum details from Consumers/Integrators/Customers so that we can provide them a safe, reliable API service. Use of the service requires some data to be collected. This data is retained only for the duration of the customer's use of the API service, after which is it deleted.

| Data elements                                | Reason for collection                                    |
| -------------------------------------------- | -------------------------------------------------------- |
| Name                                         | As a point of contact with the organisation              |
| Email Address                                | As a point of contact with the organisation              |
| Name of Organisation                         | To understand the likely needs of the customer           |
| Customer's intended products for integration | To understand the likely needs of the customer           |
| Estimated API volume usage                   | To help us find the best API usage plan for the customer |

See our [Privacy Policy](privacy.md) for further details

## For other products

Most of our products do not collect or store **any** data whatsoever. These include:

* the dGC `rcpchgrowth-python` package
* the dGC React client demo
* the dGC React component library
* the React Native client
* the dGC command line tools
* the Google Sheets plugin (note that it's possible that Google or other services collect data about you during your use of this plugin)

*[DPCHR]: Digital Paediatric Child Health Record
*[EPR]: Electronic Patient Record
*[API]: Application Programming Interface