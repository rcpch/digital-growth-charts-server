# Data Protection Considerations

## #for the API Server

The dGC server API and the service we provide around it has been designed with privacy and information security in mind.

### Anonymous Requests

The data that is sent to our server does not contain any identifiers such as patient name, NHS number or other numeric identifier, address data. It does contain date of birth because this is required to calculate the age of the patient, but this is not saved to the server.

### What does 'Stateless API' mean?

'State' in computing terms is equal to 'persistent data'.

In practical terms, being 'Stateful' means an application retaining some information on the server between two requests to the server.

By contrast, the dGC API is 'Stateless' by design, meaning it does **not** persist information between the web requests that are made of it. Each request from the API-consuming application contains all the information required to calculate a set of centile data. The response we send back contains this data, and it is never saved on the server. Some information about requests is kept for a 72 hours in the logs of our server, to enable us to monitor performance and to debug problems, however this information is anonymous.

### Persistence of results in Medical Records

Any 'persistence' (data saving) must happen in **the application which is consuming the API**, which is the natural place to persist data anyway, since this is the DPCHR, the GP system, the hospital EPR - which already likely persists lots of data about the patient.

### Data Protection Impact Assessment & ICO

In view of the stateless nature of the server, we don't handle any Patient Identifiable Data. We have reviewed the privacy implications of our application and believe it does not require a Data Privacy Impact Assessment, according to our review of [current Information Commissioner's Office guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-impact-assessments/#dpia3).

* [DPCHR]: Digital Paediatric Child Health Record

## For the API Service Wrapper

The API 'service wrapper' collects the essential minimum details from Consumers/Integrators/Customers so that we can provide them a safe, reliable API service.

* Email Address
* Name of Developer or Organisation

See our [Privacy Policy](privacy.md) for further details
 