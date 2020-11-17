# Clinical Documentation

<!-- TOC -->

- [Clinical Documentation](#clinical-documentation)
  - [Privacy](#privacy)
    - [Stateless API](#stateless-api)
  - [Definitions](#definitions)
    - [Growth velocity](#growth-velocity)
    - [Growth acceleration](#growth-acceleration)
    - [Thrive Lines](#thrive-lines)
    - [Interpreting the individual child](#interpreting-the-individual-child)
    - [Further reading about Growth Charts](#further-reading-about-growth-charts)
  - [Acknowledgements](#acknowledgements)
    - [Project Board](#project-board)
    - [RCPCH Staff](#rcpch-staff)
    - [Development Team](#development-team)
  - [References](#references)

<!-- /TOC -->

- [References](references.md)
- [Acknowledgements](acknowledgements.md)
- [DPCHR Specification (auto converted to Markdown for referenceability)](docs/clinical-documentation/dpchr-specification.md)

## Privacy

### Stateless API

The server has been designed with privacy and information security in mind.

The API is 'stateless', meaning it does **not** persist information between the web requests that are made of it. Each request from the API-consuming application contains all the information required to calculate a set of centile data. The response we send back contains this data, and it is never saved on the server.

Any 'persistence' (data saving) must happen in the application which is consuming the API, which is the natural place to persist data anyway, since this is the DPCHR, the GP system, the hospital EPR - which already persists lots of data about the patient.

In view of the stateless nature of the server, we don't handle any Patient Identifiable Data. We have reviewed the privacy implications of our application and we don't believe it currently requires a Data Privacy Impact Assessment, according to our review of [current Information Commissioner's Office guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/accountability-and-governance/data-protection-impact-assessments/#dpia3).

## Definitions

### Growth velocity

definition here

### Growth acceleration

definition here

### Thrive Lines

description of what they are and how they work

### Interpreting the individual child

clinical guidance

### Further reading about Growth Charts

[The development of growth references and growth charts - T J Cole](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3920659/)

## Acknowledgements

### Project Board

- Prof Helen Bedford, Professor of Children's Health, University College London, Great Ormond Street Institute of Child Health, London
- Dr Simon Chapman, Consultant in Paediatric Endocrinology, King's College Hospital, London
- Prof Tim Cole, Professor of Medical Statistics, Faculty of Population Health Sciences, UCL GOS Institute of Child Health, London.
- Prof Mary Fewtrell, Professor of Paediatric Nutrition. Population, Policy & Practice Dept. UCL GOS Institute of Child Health, London
- Victoria Jackson, Project Coordinator, Institute of Health Visiting
- Liz Marder, Consultant Paediatrician in Community Child Health and Neurodisability, Nottingham Children's Hospital
- Charlotte Weldon,
- Prof Charlotte Wright, Professor of Community Child Health (Medicine), University of Glasgow

### RCPCH Staff

- Rachel McKeown, Policy Lead & Project Manager, Royal College of Paediatrics and Child Health (RCPCH)
- Jonathan Miall, Director of Membership and Development, Royal College of Paediatrics and Child Health (RCPCH)
- Magdalena Umerska. Digital Platform Commercial Manager, Royal College of Paediatrics and Child Health (RCPCH)

### Development Team

- Dr Marcus Baw, General Hacktitioner, Developer and Informatician, Yorkshire and The Internet.
- Dr Simon Chapman, Consultant in Paediatric Endocrinology, King's College Hospital, London
- Prof. Tim Cole, Professor of Medical Statistics, Faculty of Population Health Sciences, UCL GOS Institute of Child Health, London.
- Joanne Hatton, Enterprise Systems Manager, Royal College of Paediatrics and Child Health, London
- Andrew Palmer, Head of Information Systems, Royal College of Paediatrics and Child Health, London

## References

1. Cole TJ, Freeman JV, Preece MA. British 1990 growth reference centiles for weight, height, body mass index and head circumference fitted by maximum penalized likelihood. Stat Med 1998;17:407-29.

2. Cole TJ, Freeman JV, Preece MA. 1998. British 1990 growth reference centiles for weight, height, body mass index and head circumference fitted by maximum penalized likelihood. Stat Med 17(4):407-29

3. WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Length/Height-for-age, Weight-for-age, Weight-for-length, Weight-for-height and Body Mass Index-for age. Methods and Development. 2006. ISBN 92 4 154693 X.

4. WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Head circumference-for-age, arm circumference-for-age, triceps skinfold-for-age and subscapular skinfold-for age. Methods and Development. 2007. ISBN 978 92 4 154718 5.

5. 3-in-1 weight monitoring chart. T Cole, Lancet. 1997 Jan 11;349(9045):102-3.

6. A chart to predict adult height from a child’s current height. T Cole, C Wright, Annals of Human Biology, November–December 2011; 38(6): 662–668

7. Designing the New UK-WHO Growth Charts to Enhance Assessment of Growth Around Birth. Tim J Cole 1, Charlotte M Wright, Anthony F Williams, RCPCH Growth Chart Expert Group, Arch Dis Child Fetal Neonatal Ed. 2012 May;97(3):F219-22.
