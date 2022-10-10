---
title: Data Protection
reviewers: Dr Marcus Baw
---

# Data Protection Considerations

## For the Digital Growth Charts API Server

The dGC server API and the service we provide around it has been designed with privacy and information security in mind.

### Anonymous Requests

The data that is sent to our server does not contain any identifiers such as patient name, NHS number, any other numeric identifier, or address data. It does contain date of birth because this is required to calculate the age of the patient, but this is not saved to the server. 

### What does 'Stateless API' mean?

The term 'State' in computing is equal to 'saved data'. In computing terminology, if an application is 'State*ful*' it means it saves some information on the server between two requests to the server. Conversely, system that is 'state*less*' does not save any data on the server.

The Digital Growth Charts API is 'Stateless' by design, meaning it does **not** persist information between the web requests that are made of it. Each request from the API-consuming application to our API contains all the information required for our Growth Chart server to calculate a set of centile data. The response we send back contains this data, and it is never saved on the server. Some information about the requests made is kept for a maximum of 72 hours in the logs of our server, to enable us to monitor performance and to debug problems, however this information is anonymous.

### Persistence of results in Medical Records

Because our API is ststeless, any 'persistence' (data saving) must happen in **the application which is consuming the API**, which is the natural place to persist data anyway, since this client system is likely to be an existing GP system, hospital Electronic Patient Record, or Persnoal Health Record - which already likely persists lots of data about the patient.

### Legal basis for requester (client) persistence
The legal basis for persisting data on the client side is likely to be Direct Care **if** your organisation is providing medical care for patients. If your organisation doesn't provide direct individual care for the patients then you may need a different legal basis, for example if your project is purely for research or planning then you may need to have consent from patients to persist their data. **Either way**, your organisation should be registered as a Data controller with the Information Commissioner's Office (ICO)

### Data Protection Impact Assessment & ICO Guidance

In view of the stateless nature of the server, the RCPCH doesn't handle any Patient Identifiable Data for this platform. We have reviewed the privacy implications of the Digital Growth Charts platform and it does not require a Data Protection Impact Assessment, according to our review of [current Information Commissioner's Office guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-impact-assessments/#dpia3).

## For the Digital Growth Charts API Service provided by the RCPCH

The API developer portal at <dev.rcpch.ac.uk> collects the essential minimum details from Consumers/Integrators/Customers so that we can provide them a safe, reliable API service. Use of the service requires some data to be collected. This data is retained only for the duration of the customer's use of the API service, after which is it deleted.

| Data elements                                | Reason for collection                                    |
| -------------------------------------------- | -------------------------------------------------------- |
| Name                                         | As a point of contact with the organisation              |
| Email Address                                | As a point of contact with the organisation              |
| Name of Organisation                         | To understand the likely needs of the customer           |
| Customer's intended products for integration | To understand the likely needs of the customer           |
| Estimated API volume usage                   | To help us find the best API usage plan for the customer |

See our [Privacy Notice](privacy-notice.md) for further details.

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