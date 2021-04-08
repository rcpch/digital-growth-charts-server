Privacy Information

# Privacy

## Privacy Policy

Our RCPCH dGC API Privacy Policy can be viewed on our Developer Portal

[dev.rcpch.ac.uk/privacy](https://dev.rcpch.ac.uk/privacy)

## Stateless API

The server has been designed with privacy and information security in mind.

The API is 'stateless', meaning it does **not** persist information between the web requests that are made of it. Each request from the API-consuming application contains all the information required to calculate a set of centile data. The response we send back contains this data, and it is never saved on the server. Some information about requests is kept for a few days in the logs of our server, to enable us to monitor performance and to debug problems, however this information is anonymous.

Any 'persistence' (data saving) must happen in the application which is consuming the API, which is the natural place to persist data anyway, since this is the DPCHR, the GP system, the hospital EPR - which already likely persists lots of data about the patient.

In view of the stateless nature of the server, we don't handle any Patient Identifiable Data. We have reviewed the privacy implications of our application and believe it does not require a Data Privacy Impact Assessment, according to our review of [current Information Commissioner's Office guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-impact-assessments/#dpia3).
