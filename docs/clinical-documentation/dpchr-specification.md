# Digital Personal Child Health Record (DPCHR)

# Minimum Viable Product Requirements

# Version 1. 3 July 2020

# V

### Document Management

Revision History

| Version | Status                                 | Date    | Contributors     | Summary of Changes                                                                                                                                                                                                                                                                           |
| ------- | -------------------------------------- | ------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0. 4    | Draft                                  | 16/1/20 | Neil Calland     | Distributed to ERG members                                                                                                                                                                                                                                                                   |
| 0. 5    | Draft                                  | 17/1/20 | Neil Calland     | Section 1 amended; annex removed, distributed to suppliers                                                                                                                                                                                                                                   |
| 0. 6    | Draft                                  | 24/2/   | Neil Calland     | Comments incorporated from ERG, RCPCH and DCH programme team members; distributed to ERG members for final review                                                                                                                                                                            |
| 0.7     | First draft for publication            | 27/2/   | Neil Calland     | Further comments from ERG members incorporated; sent up for final approval; distributed to suppliers                                                                                                                                                                                         |
| 1.0     | Second draft                           | 30/3/   | Alison Golightly | Upversioned following previous publication, re-formatting ofdocument for easy readability, inclusion of navigable table of contents, clarifications, deletion of data field ambiguity where this was a potential source of conflict for development work. and change control appendix added. |
| 1.1     | Second draft for review                | 22/4/20 | Alison Golightly | Addition of SCAL section                                                                                                                                                                                                                                                                     |
| 1. 2    | Final Draft                            | 4/5/    | Alison Golightly | Addition of clarifications suggested by NHSx, removal of publish requirement for Professional Contact in MVP, moved to future requirement.                                                                                                                                                   |
| 1.      | Final Draft for sharing with suppliers | 03/07/  | Alison Golightly | Clarity that GP address must not be displayed.                                                                                                                                                                                                                                               |

## Reviewers

This document must be reviewed by the following:
|Reviewer Name |Title / Responsibility |Date| Version|
|-|-|-|-|
|Leanne Summers| Digital Eco-System Lead, NHSx| 27/4/2020| V1.|
|Helen Harger| Product Owner, Digital Child Health Programme, NHSD| 22/4/2020| V1|
|Andy Payne| Technical Architect, NHSx| 27/4/2020| V1.|
|Donna-Marie Jarrett| Lancashire + London Healthier Lancashire + South Cumbria ICSDCH Programme Manager| , 27/4/2020| V1.|

## Approvals

This document requires the following approvals.
 - Leanne Summers Digital Eco-System Lead, NHSx 

 -----

- 1 Introduction Table of Contents
  - 1.1 Purpose
  - 1.2 Background
  - 1.3 Minimum Viable Product
  - 1.4 Format of document
- 2 Health information recorded by professionals
  - 2.1 Functional requirements for the MVP
  - 2.2 Relevant national services, standards and capabilities
  - 2.3 Direction of travel beyond the MVP
- 3 Health information recorded by parents
  - 3.1 Functional requirements for the MVP
  - 3.2 Relevant national services, standards and capabilities
  - 3.2 Direction of travel beyond the MVP
- 4 Advice and guidance for parents
  - 4.1 Functional requirements for the MVP
  - 4.2 Relevant national services, standards and capabilities
  - 4.3 Direction of travel beyond the MVP
- 5 Reminders, follow-ups and alerts
  - 5.1 Functional requirements for the MVP
  - 5.2 Relevant national services, standards and capabilities
  - 5.3 Direction of travel beyond the MVP
- 6 Account and record management
  - 6.1 Functional requirements for the MVP
  - 6.2 Relevant national services, standards and capabilities
  - 6.3 Direction of travel beyond the MVP

7 Onboarding to NHS Digital services and completing the SCAL ................................................ 28

8 Other Requirements....................................................................................................................... 29

```
8.1 Other Requirements for the MVP/ Supplier ............................................................................... 29
```

9 Change Control .............................................................................................................................. 30

## 1 Introduction

### 1.1 Purpose

This document is aimed at suppliers who are interested in supporting the NHS aspiration for
Digital Personal Child Health Records (DPCHRs), and in particular, those interested in
supporting the initial target – from the start of 2021, parents across the country should have
the option of a DPCHR minimum viable product (MVP) to supplement their paper 'red book’.

### 1.2 Background

Parents of newborns across the country are currently issued with a paper personal child
health record (PCHR, or ‘red book’). The specification for this can be downloaded from
Harlow Printing through this link - https://www.healthforallchildren.com/pchr-download/.

The PCHR is designed to support the Healthy Child Programme. Public Health England
(PHE) are currently leading on a review and modernisation of the programme.

The Government published a Tech Vision for healthcare in 2018, underpinned by four
guiding principles:

- User need
- Privacy and security
- Interoperability and openness
- Inclusion

The digital strategy Healthy Children: Transforming Child Health Information published in
2016 included an ambition for an electronic version of the PCHR for parents, which:

- Encourages partnership between health professionals and parents, families and
  children and young people
- Improves communication between health professionals and parents

- Improves communication between health professionals based in different
  organisations or care settings who do not share a common record of a child’s care
- Increases parents’ understanding of their child’s health and development

The NHS Long Term Plan was published in 2019, and states:
“A digital version of the 'red book' will help parents record and use information about
their child, including immunisation records and growth.”

A DPCHR should provide at least the equivalent parent-facing functionality as the paper
PCHR, while also exploiting the inherent capabilities of ‘digital’.

The Royal College of Paediatrics and Child Health (RCPCH) owns the copyright of the
Personal Child Health Record and any of its derivatives^1. Selected features in this document
specified for the MVP will be supported by clinical advice and content made available under
licence from RCPCH, who will be responsible for quality assurance on an ongoing basis.
The terms of the licence will be clarified by RCPCH and NHSX in due course. The license
will facilitate free access for the launch of the MVP and for a finite period afterwards.

NHS Digital has recently published a Personal Health Record (PHR) toolkit at
https://digital.nhs.uk/services/personal-health-records-adoption-service/personal-health-
records-adoption-toolkit. The toolkit states that a record is a PHR if:

- It's secure, usable and online
- It's managed by the person who the record is about and they can add information to
  their PHR
- It stores information about that person’s health, care and wellbeing
- Health and care sources can add information to the PHR

DPCHRs are seen as a category of PHR and should meet this definition, although for babies
and young children, a proxy will manage the record on their behalf.

NHS Digital, NHSx, PHE and local organisations are collaborating in the Digital Child Health
Programme (https://digital.nhs.uk/services/digital-child-health) to create an interoperability
layer to support the exchange of Healthy Child Programme information, providing a
foundation for DPCHRs.

#### 1

```
This excludes the clinical datasets which the DPCHR will utilise.
```

A new record standard has been created in partnership with the Professional Records
Standards Body (https://theprsb.org/standards/healthychildrecordstandard/) and the
standard is supported by an Information Standards Notice requiring IT system suppliers to
make their systems compliant with the standard by June 2020. This, along with the NHS
Login service being able to support identity verification, provides key building blocks for
DPCHRs.

### 1.3 Minimum Viable Product

The target date for MVP availability across the country is January 2021. The MVP has been
scoped to provide value above and beyond the paper ‘red book’ (which parents will continue
to have for an interim period), while not setting up the programme to fail through being over-
ambitious, nor for barriers to entry to be too high for suppliers in an interim context where
there is unlikely to be any national / nationally-brokered revenue streams. The scope of the
MVP is also dependent upon the status of interoperability across clinical systems across the
country.

From a parent’s perspective, the key use cases that the DPCHR MVP will serve (and that
will provide value beyond the paper ‘red book’, will be:

- As a parent, I want access to health, wellbeing and parenting advice, guidance and
  reminders so that I can play my part in giving my child the best start
- As a parent, I want to start a lifetime digital vaccinations record for my child so that in
  the future, a comprehensive record of their vaccinations is easily accessible
- As a parent, I want timely access to my child’s screening results and vaccinations so
  that I have an accurate record of my child’s history which I share with others.

The MVP defines a national baseline ambition. Some localities may have the resources and
momentum to service a higher level of ambition and may move ‘further faster’.

It is anticipated that later in 2021, a revised set of requirements will be published that will
define a ‘richer’ baseline product to be available from 22/23.

### 1.4 Format of document

The document is structured around the following ‘feature sets’, each of which will be
represented to some degree in the MVP:

2. Health information recorded by professionals
3. Health information recorded by parents
4. Advice and guidance for parents
5. Reminders, follow-ups and alerts
6. Account and record management

Beyond these feature sets, other feature sets can be envisaged in a future product beyond
the MVP, including appointment management and digitally-enabled interactions (e.g. video
or instant messaging between professionals and parents).

It is envisaged that the document will be developed further in the future to set out a core
specification and set of requirements for DPCHR products beyond the MVP.

For each feature set represented in the MVP, the following standard format is followed:

- Functional requirements for the MVP: this section details the functional
  requirements that should be available to parents across the country from the start of
  2021; most of these are articulated as a ‘MUST’, but some as a ‘COULD’ –
  development of the latter could provide local revenue opportunities in the interim
  period where digital is being offered as a supplement to paper, but such opportunities
  are likely to also require local deployment of resources
- Relevant national services, standards and capabilities: this section sets out what
  is available now or will be soon, and where appropriate, references the relevant
  functional requirements in brackets; it also includes some non-functional
  requirements
- Direction of travel beyond the MVP: this section sets out what may, in due course,
  be specified nationally for development beyond the MVP, through an enhanced
  product to be available from 22/23, when the deployment model is anticipated to
  switch to ‘digital as an alternative’ (from ‘digital as a supplement’). This information
  may inform some initial design / architecture decisions by suppliers; should suppliers
  intend to pursue development in these areas in advance of it being specified
  nationally, they should consult with the national team first

## 2 Health information recorded by professionals

### 2.1 Functional requirements for the MVP

ID Requirement Xref to 2.
2.1.1 The DPCHR MUST process demographic information for the child as
per the PDS Birth Notification data fields, available here
https://developer.nhs.uk/apis/ems-beta/pds_birth_notification.html.
However DPCHR suppliers will not display the child’s address at
anytime to comply with safeguarding concerns about
accidental/coerced disclosure of a child’s address.
(Note – this information will be available if the mother has confirmed her
identity through NHS Login ante-natally; if not, then some of these fields
may be blank – see 6.1.3)

#### 2.2.2,

#### 2.2.

2.1.2 The DPCHR MUST present birth details for the child as per the PDS
Birth Notification data fields, available here
https://developer.nhs.uk/apis/ems-beta/pds_birth_notification.html
(Note – this information will be available if the mother has confirmed
her identity through NHS Login ante-natally; if not, then some of these
fields may be blank – see 6.1.3)

#### 2.2.2,

#### 2.2.

2.1.3 The DPCHR MUST present information on outcomes of newborn
screening for the child as per the relevant message specifications:
Blood Spot Test Outcome https://developer.nhs.uk/apis/ems-
beta/blood_spot_test_outcome_1.html
Newborn Hearing https://developer.nhs.uk/apis/ems-
beta/newborn_hearing_1.html
NIPE Outcome https://developer.nhs.uk/apis/ems-
beta/nipe_outcome_1.html
]; the DPCHR MUST wait until the child reaches a defined age (to be
configurable) before newborn blood spot results are displayed to
parents
(Note – this information will only be available from the point at which a

#### 2.2.

#### 2.2.

#### 2.2.

parent enters ‘connected mode’ – see section 6)
2.1.4 The DPCHR MUST present detailed information on vaccinations
received by the child as per the Vaccination data fields, available here
https://developer.nhs.uk/apis/ems-beta/vaccinations_1.html
(Note – this information will only be available from the point at which a
parent enters ‘connected mode’ – see section 6)
(Note – such data may include the recording of historical vaccinations
received overseas)

#### 2.2.

#### 2.2.

2.1.5 The DPCHR MUST present an overview of vaccinations received by
the child, providing access to the detail as set out above.Vaccinations
MUST be capable of being ordered on any of the data fields, for
example, date or vaccine code.
2.1.6 Where a parent has recorded one or more vaccinations (see 3.1.1), the
overview MUST also incorporate such vaccinations, which should be
clearly differentiated from professional-recorded vaccinations
2.1.7 The DPCHR MUST set parents’ expectations regarding which
screening outcomes and vaccinations may or may not appear, when
they would appear, and what to expect in the DPCHR v the paper ‘red
book’

#### 2.2.

2.1.8 The DPCHR MUST present the name of the organisation currently
responsible for providing a Health Visiting service to the child and the
name of the GP practice with which the child is currently registered
(where the data is received after the parent has entered a ‘connected’
mode - see section 6)
[Note that these relationships may not be in place for the child]
[Note the GP address must not be displayed]

#### 2.2.

#### 2.2.

#### 2.2.

2.1.9 The DPCHR MUST be able to support the portability (both ways, i.e. as
a potential ‘sender’ and as a potential ‘receiver’) of the professionally-
recorded information set out above, where a parent moves from one
DPCHR product to another; in a DPCHR that has imported data, the
DPCHR MUST clearly indicate the imported data and explain the
potential implications (i.e. that it could in theory have been changed)

#### 2.2.

#### 2.2.

2.1.10 The DPCHR MUST display the provenance of health information
recorded by professionals

#### 2.2.

### 2.2 Relevant national services, standards and capabilities

ID Requirement
2.2.1 This functionality is underpinned by interoperability via the National Events
Management Service (NEMS). A DPCHR MUST be a subscriber to the NEMS for
children who have been authenticated for that DPCHR, MUST auto-ingest the
relevant events, and MUST store the relevant elements in a child record indexed
by NHS number. Further detail on the NEMS capability can be found here –
https://developer.nhs.uk/apis/ems-beta/index.html.
2.2. 2 The PDS Birth Notification will be available from NEMS (2.1.1, 2.1.2). The
DPCHR MUST subscribe to the PDS Birth Notification, and auto-ingest and store
in the child record the elements to be displayed to parents (as a minimum). The
baby’s address should also be ingested and stored, even though it won’t be
displayed in a DPCHR (see 6.1.7, 6.1.11), but it will support functional
requirements in other sections. Seehttps://developer.nhs.uk/apis/ems-
beta/pds_birth_notification.html.
2.2.3 The PDS Change of GP will be available from NEMS (2.1.8). The DPCHR MUST
subscribe to the PDS Change of GP, and auto-ingest and store in the child record
the elements to be displayed to parents (as a minimum).
Seehttps://developer.nhs.uk/apis/ems-beta/pds_change_of_gp.html.
[Note the GP address must not be displayed]
2.2.4 The PDS Change of Address will be available from NEMS. The DPCHR MUST
subscribe to the PDS Change of Address, and the relevant elements should be
auto-ingested and stored in the child record, even though they won’t be displayed
in a DPCHR (see 6.1.7, 6.1.11), but will support functional requirements in other
sections. Seehttps://developer.nhs.uk/apis/ems-
beta/pds_change_of_address.html.
2.2.5 Note that the PDS Death Notification will also be available from NEMS and will
support functional requirements detailed in section 6 (see 6.2.5).
2.2.6 Beyond the PDS messages, the following events will also be available from
NEMS (2.1.3, 2.1.4, 2.1.8). The DPCHR MUST subscribe to these messages,
and auto-ingest and store in the child record the elements to be displayed to
parents (as a minimum). See the relevant tabs in the Healthy Child Event
Specification at https://theprsb.org/wp-content/uploads/2019/05/Healthy-Child-
Event-Specification-v2.2-ISN-COPY-NO-CHANGES.xlsx and also FHIR profiles
at https://developer.nhs.uk/apis/ems-beta/overview_supported_events.html

- CH015 – Vaccination
- CH021 – Newborn Hearing
- CH024 – NIPE Outcome
- CH027 – Professional Contacts
- CH035 – Blood Spot Test Outcome

  2.2.7 Field labels and ordering (2.1.1, 2.1.2, 2.1.3, 2.1.4) are listed in the associated
  tabs in the Healthy Child Record Specification at https://theprsb.org/wp-
  content/uploads/2019/05/Healthy-Child-Record-Specification-v2.0-13.12.18.xls.
  2.2.8 Further guidance will be provided on how to identify the Professional Contacts
  messages that relate specifically to Health Visiting, and how to decode the ODS
  code that will be in the message (2.1.8).
  2.2.9 A standard JSON / XML format will be defined to support portability (2.1.9).
  2.2.10 Wording will be provided to support the management of parents’ expectations
  (2.1.7) and the potential implications of imported data (2.1.9).
  2.2.11 Further guidance will be provided on how information provenance should be
  presented.
  2.2.12 Further guidance will be provided on the age at which blood spot results can be
  shared with parents.

### 2.3 Direction of travel beyond the MVP

Over time, the scope of professional-recorded information available will increase, until it
matches the scope of the paper ‘red book’ / Healthy Child Record standards. Within this, the
scope of birth details will increase beyond what is available in the PDS Birth Notification.

The wording to manage parents’ expectations will be updated as the scope of information
increases.

As LHCRs develop, it is anticipated they will offer local events management services
(LEMS). This would mean that in due course, in selected geographies, DPCHRs would
subscribe to a LEMS, rather than / in addition to the NEMS. This may also provide more
sophisticated solutions to a DPCHR being able to access historical information.

```
For parents who only move to a ‘connected’ mode (section 6) after the data flowed to NEMS,
there may be further solutions available to ensure information that is recorded between birth
and entering ‘connected’ mode is not lost to the DPCHR. Similarly, there may be scope for a
more sophisticated solution to support portability, potentially API-based.
```

```
In due course, the FHIR messages will move from R3 to R4.
```

```
Changes to the Healthy Child Programme will continue to happen from time-to-time. In such
cases, the Healthy Child Standards will be updated accordingly. Appropriate timescales to
comply with any changes will be given.
```

```
The potential to display data in the DPCHR from the child’s GP record will be assessed,
which may lead to future requirements for the DPCHR.
```

```
A future mechanism may need to be specified for parents to flag data that they believe is
incorrect.
```

## 3 Health information recorded by parents

### 3.1 Functional requirements for the MVP

ID Requirement Xref to 3.
3.1.1 The DPCHR MUST allow the structured recording of a vaccination
received by the child using field formats to align with those for
professionally recorded information, https://theprsb.org/wp-
content/uploads/2019/05/Healthy-Child-Event-Specification-v2.2-ISN-COPY-NO-
CHANGES.xlsx However, we do not expect parents to have to manage
SNOMED coding except through human readable pick list functionality.
In addition, the DPCHR MUST allow the recording of free text related to a
vaccination
[Note – this will not flow to clinical systems]

#### 3.2.1,

#### 3.2.

3.1.2 The DPCHR MUST present information on vaccinations received, as
potentially recorded by a parent, and clearly indicate that the information
is parent-recorded

#### 3.2.1,

#### 3.2.

[Note – see 2.1.6]
3.1.3 The DPCHR MUST allow a parent to amend or delete details of a
vaccination that they have recorded
[Note – does not apply to professional-recorded vaccinations]
3.1.4 The DPCHR MUST allow the structured recording of a child’s weight,
length / height and head circumference [, field formats to align with those
for CH018 Observations available in https://theprsb.org/wp-
content/uploads/2019/05/Healthy-Child-Event-Specification-v2.2-ISN-
COPY-NO-CHANGES.xlsx ; in addition, the DPCHR MUST allow the
recording of free text related to a measurement
[Note – this will not flow to clinical systems]
[Note – professionally recorded measurements are not part of the MVP
scope]

#### 3.2.3,

#### 3.2.

3.1.5 The DPCHR MUST allow a parent to amend or delete details of a
measurement they have recorded (while maintaining a full audit trail)
3.1.6 [Intentionally left blank]
3.1.7 The DPCHR MUST automatically plot a weight on a chart based on UK-
WHO data; the particular chart MUST be based on the child’s gender and
age – one of boys preterm, boys 0-1, boys 1-4, girls preterm, girls 0-1,
girls 1-4; for preterm babies, the 0-1 charts MUST incorporate automatic
gestational correction / line back

#### 3.2.

3.1.8 The DPCHR MUST automatically plot a length / height on a chart based
on UK-WHO data; the particular chart MUST be based on the child’s
gender and age – one of boys 0-1, boys 1-4, girls 0-1, girls 1-4; for
preterm babies, the 0-1 charts MUST incorporate automatic gestational
correction / line back

#### 3.2.

3.1.9 The DPCHR MUST automatically plot a head circumference on a chart
based on UK-WHO data; the particular chart MUST be based on the
child’s gender and age – one of boys preterm, boys 0-1, boys 1-4, girls
preterm, girls 0-1, girls 1-4; for preterm babies, the 0-1 charts MUST
incorporate automatic gestational correction / line back

#### 3.2.

3.1.10 The DPCHR MUST display series of measurements on relevant charts;
professional measured / parent recorded and parent measured / parent
recorded plot points MUST be easily distinguished, and the DPCHR
MUST allow these two different types to be filterable; the DPCHR must
support ‘hover over’ of the plot points, displaying the underlying data

#### 3.2.3,

#### 3.2.

[measurement, date of measurement, calculated centile, whether the
measurement was taken by a professional or not, who recorded, date of
recording, and any free text recorded by the parent]
3.1.11 The DPCHR MUST provide access to guidance on how to measure and
how to interpret growth charts

#### 3.2.

3.1.12 Beyond the structured recording of vaccinations and measurements, the
DPCHR MUST allow a parent to record text and upload images and to
tag / categorise each entry
[Note – in essence, this will form a ‘general’ parental log]
[Note – this will not flow to clinical systems]

#### 3.2.

3.1.13 The DPCHR MUST present information logged by a parent (3.1.12)
capable of being ordered on any of the data fields present, for example,
date.

#### 3.2.

3.1.14 The DPCHR MUST be able to support the portability (both ways, i.e. as a
potential ‘sender’ and as a potential ‘receiver’) of the parent-recorded
information set out above, where a parent moves from one DPCHR
product to another; in a DPCHR that has imported data, the DPCHR
MUST clearly indicate the imported data

#### 3.2.

### 3.2 Relevant national services, standards and capabilities

ID Requirement
3.2.1 The data elements and standards for a Vaccinations event are defined in the
Healthy Child Event Specification at https://theprsb.org/wp-
content/uploads/2019/05/Healthy-Child-Event-Specification-v2.2-ISN-COPY-NO-
CHANGES.xlsx.
3.2.2 Beyond the elements in the Event Specification for Vaccinations, the validation
and coding rules, the format for ‘who recorded’ the vaccination and the format for
the free text are to be defined (3.1.1, 3.1.2).
3.2.3 The data elements and standards for a Measurement (Observation) event are
defined in the Healthy Child Event Specification at https://theprsb.org/wp-
content/uploads/2019/05/Healthy-Child-Event-Specification-v2.2-ISN-COPY-NO-
CHANGES.xlsx. The subset of elements for parents to record (and the validation
rules around entry of these elements) or for the system to capture are to be
defined (3.1.4).

3.2.4 Beyond the elements in the Event Specification for Observations, the formats for
the marker that distinguishes professionally measured and parent measured and
for ‘who recorded’ the measurement are to be defined (3.1.4, 3.1.10).
3.2.5 3.2.5 [Intentionally left blank].

3.2.6 Digital and clinically robust versions of the growth charts together with advice and
guidance will be provided by the Royal College of Paediatrics and Child Health
(RCPCH) for suppliers to use. Suppliers should not develop their own charts or
guidance. Further details will be provided in due course (3.1.7, 3.1.8, 3.1.9).
3.2.7 The wording for the guidance on how to measure and how to interpret growth
charts will be provided, and on how to use paper and digital versions of growth
charts together (3.1.11).
3.2.8 The standards and validation rules for data elements for a log entry are to be
defined (3.1.12, 3.1.13).
3.2.9 A standard JSON / XML format will be defined to support portability (3.1.14).

### 3.2 Direction of travel beyond the MVP

```
The ability for professionally-recorded measurements will ultimately be in place across the
country. For plotting on growth charts, this will add a third category of plot point of
‘professional measured / professional recorded’ (to professional measured / parent recorded
and parent measured / parent recorded).
```

```
Over time, the scope of parent-recorded information will increase – it will incorporate
developmental firsts and checklists present in the paper ‘red book’, and may include further
features such as structured logs, diaries, feedback, and other self-assessment or interactive
tools, endorsed where appropriate by the National Screening Committee.
```

```
Further growth charts may be incorporated, such as age 2-9, Downs Syndrome, NICM.
Growth monitoring may encompass BMI. Growth charts will incorporate professionally
measured / professionally recorded data. Further research and analysis could lead to
alternative ways of articulating a child’s status, and personalised prompts / constraints (e.g.
advising against too-frequent measurement).
```

```
In due course, parent-recorded information may flow to clinical systems.
```

## 4 Advice and guidance for parents

### 4.1 Functional requirements for the MVP

ID Requirement Xref to 4.
4.1.1 The DPCHR MUST allow the searching of a nationally-curated set of
children’s (health, wellbeing and parenting) content to surface topics of
interest to the parent

#### 4.2.

4.1.2 The DPCHR MUST allow the drill-down through an information
architecture sitting above a nationally-curated set of children’s content to
surface topics of interest to the parent

#### 4.2.

4.1.3 The DPCHR MUST present the up-to-date UK standard vaccination
schedule appropriate to the date of birth of the child, with parents’
expectation set that this is a schedule based on standard rules, but may
not be accurate for children in certain circumstances - children may be
called for vaccination at dates different to the ones indicated here

#### 4.2.

4.1.4 The DPCHR MUST link directly to relevant advice and guidance (from
the curated content) from different parts of the DPCHR - for example,
individual vaccination-specific advice and guidance signposted from the
schedule (see above), reminders (see 5.1.1) and from the vaccination
record, feeding advice and guidance signposted from the growth charts
4.1.5 The DPCHR MUST ‘push’ topics appropriate to the age of the child from
a nationally-curated set of children’s content

#### 4.2.

4.1.6 The DPCHR MUST be able to provide a notification of newly-pushed
topics outside of the app, with parents able to personalise such
notifications (e.g. the ability to turn off such notifications)
4.1.7 The DPCHR MUST be able to allow a local healthcare service to amend
the frequency, timing and ‘batching’ of topics to push
(Note – this may be in response to national guidance, generated from
insights into early DPCHR experiences)

#### 4.2.

4.1.8 For information curated from the NHS Website or from Start4Life, the
DPCHR MUST present up-to-date information within the app, with the
provenance stated

#### 4.2.

#### 4.2.

#### 4.2.

4.1.9 For information curated from other sources, the DPCHR MUST signpost
to third-party sites through a valid link; such content MUST be clearly
marked and the provenance stated
(Note – this applies to content curated nationally, and potentially, curated
by local healthcare services (see 4.1.12) – the DPCHR MUST NOT
include or signpost to other content unless explicit agreement is obtained
from NHSX)

#### 4.2.

#### 4.2.

4.1.10 The DPCHR MUST present the up-to-date Healthy Child Programme
series of interventions to which all children are entitled

#### 4.2.

Optional
4.1.11 The DPCHR COULD support a more sophisticated model of pushing
information, applying some smoothing to the volumes of information
flowing to parents over a time period, and incorporating further factors
beyond age appropriateness
4.1.12 The DPCHR COULD allow local healthcare services to supplement the
nationally-curated children’s content with locally-relevant content, with
this information able to be searched, drilled-down into or pushed, as
above (and in a way that doesn’t require the parent to undertake
separate searches / drill-downs for national and local content); such
content MUST be clearly marked and the provenance stated

#### 4.2.

#### 4.2.

### 4.2 Relevant national services, standards and capabilities

ID Requirement
4.2.1 The national curation of a set of children’s content is to be completed. This will
include building an information architecture around the content, and also topic
summaries.
4.2.2 National guidance (high level) will be provided for local healthcare services
around amending how topics are pushed (4.1.7), should evidence emerge as to
the most effective way of doing this. Suppliers will be able to combine this with
more detailed ‘how to’ guidance and issue it appropriately. Similarly, should there
be significant demand for supplementary content (4.1.12) in the MVP period, then

further national guidance will be provided.
4.2.3 The potential for a curated children’s content service (C3S) is being investigated
currently. DPCHR products would embed it within their apps, and it would support
a number of the functional requirements detailed above, meaning that suppliers
wouldn’t need to develop these themselves. Further details will be provided in
due course, including how any tagging for age-relevance would be done
nationally.
4.2.4 NHS Website and Start4Life content will be pulled through via an API, either by
the DPCHR itself, or by the C3S embedded within a DPCHR (4.1.8).
4.2.5 The UK standard childhood vaccination schedules can be found at
https://www.gov.uk/government/publications/routine-childhood-immunisation-
schedule. Wording will be provided to manage parents’ expectations (4.1.3).
4.2.6 Further guidance will be provided on how information provenance should be
presented.
4.2.7 The content for the Healthy Child Programme series of universal interventions to
display to parents will be provided (4.1.10)

### 4.3 Direction of travel beyond the MVP

```
The requirements at the bottom of the table (4.1.11-4.1.12) marked as ‘COULD’ may all end
up in a future version of the functional requirements as ‘MUSTs’. (The national programme
team will be keen in gathering insights from users wherever these requirements are
deployed early).
```

```
For local content, the potential for integration with Directories of Services will be
investigated.
```

```
In the future, DPCHRs could allow supplier administrators to supplement the nationally
curated children’s content with non-core content. The premise would be to offer engaging
content to ‘hook’ parents in to viewing the core content – e.g. ’10 reasons to not feel guilty
about having a night out without baby’. Additionally, tailored or additional advice and
guidance targeted at fathers or other carers could be appropriate.
```

```
Other features that may be specified in the future include the ability to bookmark content, the
ability to feed back on content, health professionals able to ‘prescribe’ advice and guidance..
```

```
With regards to the vaccination schedule, this could become more personalised, potentially
based on age of child, family context and previous vaccination history.
```

## 5 Reminders, follow-ups and alerts

```
Note - the requirements are written based on the following premise. In addition to advice and
guidance ‘topics’ described in the previous section, other types of information will be
presented to parents, including reminders, follow-ups and alerts.
```

### 5.1 Functional requirements for the MVP

ID Requirement Xref to 5.
5.1.1 The DPCHR MUST ‘push’ reminders appropriate to the age of the child
from a nationally-maintained set of ‘Healthy Child’ reminders (e.g. a
reminder to have a dental check at one)

#### 5 .2.

5.1.2 The DPCHR MUST ‘push’ a reminder to parents who are in the maternity
pathway (i.e. child’s date of birth is in the future) to sign-up via NHS Login (if
not already done so) (6.1.1)

#### 5.2.

5.1.3 The DPCHR MUST be able to provide a notification of newly-pushed
reminders, follow-ups and alerts outside of the app
5.1.4 For vaccination reminders, the DPCHR MUST set parents’ expectation that
this is a reminder based on standard rules, but may not be accurate for
children in certain circumstances - children may be called for vaccination at
dates different to the ones indicated here or may have a contraindication

#### 5.2.

Optional
5.1.5 The DPCHR COULD allow local healthcare services to ‘push’ alerts based
on local environmental factors (such as disease outbreaks or digital
developments

#### 5.2.

### 5.2 Relevant national services, standards and capabilities

ID Requirement
5.2.1 The national development of a set of ‘Healthy Child’ reminders is to be completed
(5.1.1). These will be tagged for age-relevance.
5.2.2 Wording will be provided for the reminder (5.1.2) and to manage parents’
expectations (5.1.4).
5.2.3 Should there be significant demand for local ‘alerting’ (5.1.5) in the MVP period,
then further national guidance will be provided.

### 5.3 Direction of travel beyond the MVP

```
In the future, DPCHRs will be expected to support ‘follow ups’ and subscribe to failsafe
messages – Failsafe Message and Failsafe Message Response – and present the relevant
information to parents. In practice, this covers scenarios such as the child not being
registered with a GP, or screening, vaccinations or health visitor reviews not having taken
place within defined timescales.
```

```
There may be potential in the future to link reminders to developmental milestones, such as
a first tooth appearing.
```

```
The requirement at the bottom of the table (5.1.5) marked as ‘COULD’ may end up in a
future version of the functional requirements as a ‘MUST’.
```

## 6 Account and record management

```
Accounts and Records: The nature of a DPCHR – being a child’s record from birth - means
that the child’s record is administered by another person on behalf of the child for a
considerable period of time, this is referred to as ‘proxy access’. Such access is usually held
by a person who has parental responsibility for the child. We therefore make a distinction
between an account holder – the person holding parental responsibility and administering
the record and the record which is about the child. A child would eventually become an
account holder for the record themselves. As parental responsibility can change or be
```

shared during the course of a child’s life, a general principle is that one or more account
holders can have access to a child record either sequentially or jointly

```
In summary:
```

- 0 - 5 year olds are not of an age to manage their record themselves, so proxy
  access is required
- Parents, carers or guardians of a child can have a DPCHR account to access a
  DPCHR– as such, they would be account holders
- Multiple (related) account holders can have access to a single child record

Modes of Connection: a DPCHR can function in either an unconnected or a connected
mode.

Unconnected Service

- This is an information and guidance app in support of early years health and
  prompting parents to take their children to Healthy Child Programme services such
  as immunisations and health checks. It can also provide guidance on local services
  or local health promotion material.
- To use this service, parents can simply sign up with an email address and start using
  the app. No formal identification of the parent takes place and there is no verification
  of parental responsibility. There is consequently no connection to NHS data sources
  for the child.

Connected Service

- This is the same app as above, but the parent and child have been formally
  identified, meaning the NHS can send copies of the information it holds – screening
  test results, immunisations etc – to the child’s DPCHR, enabling rapid, convenient
  communication with health services
- This service will use the new NHS login standard^2 for identifying citizens or can use
  other suitable offline modes of identification.

Only a connected service requires proxy access, In an unconnected service there is no
formal identification of the account holder or verification that the child exists.

Professional Service

- This is a form of system administration which is required to effect connection and
  disconnection of account holders to the record.
- Connection of account holder to record is needed where this cannot be done
  automatically, that is, all scenarios where NHS Login and the PDS birth notification
  are not used.

#### 2

```
Or equivalent offline process, see 4.2 below and Appendix A on Identification
```

- There is no automated disconnection of record for changes of parental responsibility,
  so professiona mode is used to effect this.
  per The table below, references the relevant functional requirements for each mode.
  Connected mode Unconnected
  mode

```
Professional mode
```

```
Verification
requirement
```

#### 6.1.1 – 6.1.4 6.1.9 6.1.12

```
Privileges 6.1.5 – 6.1.6 6.1.10 6.1.13 – 6.1.14
Safeguarding
requirement
```

#### 6.1.7 – 6.1.8 6.1.11 6.1.15

```
Additional requirements are also set out that are not mode-specific – 6.1.16 - 6.1.25.
```

### 6.1 Functional requirements for the MVP

ID Requirement Xref to
6.2
Connected mode
6.1.1 The DPCHR MUST signpost to the NHS Login Service to enable an
account holder to be able to verify their identity and register for the
DPCHR using this service.

#### 6.2.2

6.1.2 The DPCHR MUST allow parental responsibility of an account holder to
be confirmed through a PDS Birth Notification for birth mothers who
have used NHS Login ante-natally to verify their identity; the DPCHR
MUST create a record for the child, indexed by NHS number

#### 6.2.3

6.1.3 The DPCHR MUST allow parental responsibility of an account holder to
be confirmed by a professional (operating in professional mode – see
6.1.13) where the new account holder has used NHS Login to verify
their identity; the DPCHR MUST require the professional to record the
child’s NHS number, name and date of birth; where a child record does
not already exist, the DPCHR MUST create a record for the child,
indexed by NHS number, and also populated with their name and date
of birth, plus their gender and length of gestation
[Note – this route supports scenarios including: the birth mother only

#### 6.2.8

verifying their identity through NHS Login post-natally; non-biological
parents; adoption; an estranged father; multiple account holders
operating in connected mode]
6.1.4 The DPCHR MUST allow parental responsibility of an account holder to
be confirmed by another account holder with parental responsibility
(confirmed through one of the two routes above) where the new
account holder has used NHS Login to verify their identity
[Note – this route supports scenarios including: one parent giving the
same level of access to another parent; multiple account holders
operating in connected mode
6.1.5 The DPCHR MUST allow an account holder operating in connected
mode access to all the parent-facing requirements in this specification
(including 6.1.4 and 6.1.6)

#### 6.2.7

6.1.6 For account holders that transition into connected mode from an
unconnected mode, the DPCHR MUST maintain their access to any
information recorded in unconnected mode
6.1.7 The DPCHR MUST not display the address of the child (or of a person
with parental responsibility)
6.1.8 The DPCHR MUST, upon receipt of a valid request from a professional
(operating in professional mode – see 6.1.14), disconnect / freeze a
connected account, meaning that no new data is presented or updated
(section 2), no new advice and guidance is pushed (section 4), no new
reminders, follow-ups and alerts are issued (section 5), and no
additional access can be granted (section 6)
[Note – this would typically be done should there be a change in
parental responsibility for the child]

#### 6.2.1

Unconnected mode
6.1.9 The DPCHR MUST allow an account holder to be created through their
provision of an e-mail and password and a label for the child
6.1.10 The DPCHR MUST NOT allow the account holder access to:

- the functionality under ‘Health information recorded by
  professionals’ (section 2)
- The DPCHR MUST allow the account holder access to:
- limited functionality under ‘Health information recorded by
  parents’ (section 3) – 3.1.4-3.1.6
- all the functionality under ‘Advice and guidance’ (section 4)
- all the functionality under ‘Reminders, follow-ups and alerts’

#### 6.2.7

(section 5), with the exception of 5.1.5 (should that be pursued)
6.1.11 The DPCHR MUST not display the address of the child (or of a person
with parental responsibility)
Professional mode
6.1.12 The DPCHR MUST allow a valid professional to operate in professional
mode

#### 6.2.10

6.1.13 The DPCHR MUST allow the professional to support the confirmation
of parental responsibility (as per 6.1.3); the DPCHR MUST require the
parent’s and child’s valid NHS numbers to be entered
6.1.14 The DPCHR MUST allow the professional to initiate the disconnection /
freezing of a connected record (as per 6.1.8); the DPCHR MUST
require the parent’s and child’s valid NHS numbers to be entered
[Note that for any details entered, there may not actually be a
connected record in place]
6.1.15 [No specific safeguarding requirement]
General requirements for account holders
6.1.16 The DPCHR MUST support access to information on multiple children
from a single account
6.1.17 The DPCHR MUST allow parents to make an informed choice on
connected versus unconnected mode, and set expectations accordingly

#### 6.2.9

6.1.18 The DPCHR MUST store personalisation information against the
account holder (to support 4.1.6), rather than the child
6.1.19 Upon receipt of a PDS Death Notification for a child, the child record
MUST effectively be disconnected / frozen, meaning that no new data
is presented or updated (section 2), no new advice and guidance is
pushed (section 4), no new reminders, follow-ups and alerts are issued
(section 5), and no additional access can be granted (section 6)
[Note – clinical data that is still ‘in the system’ may be presented /
updated (section 2)]

#### 6.2.5

6.1.20 The DPCHR MUST allow an account holder to delete their account
(without affecting the persistence and integrity of professional recorded
information in the child record)
6.1.21 The DPCHR app MUST be downloadable 6.2.6
Other requirements
6.1.22 The DPCHR supplier MUST provide a set of analytics data to local
commissioners and the national team

#### 6.2.4

6.1.23 The DPCHR MUST make it a condition for a parent entering connected
mode that they give their consent to be messaged by the NHS (or an
agency commissioned by the NHS) to ask for their participation in
research

#### 6.2.9

6.1.24 The DPCHR MUST offer both a timeline view and a structured view;
information associated with sections 2 and 3 MUST be available
through both views; pushed advice and guidance, reminders, follow-
ups and alerts (sections 4 and 5) MUST be accessible through the
timeline view (in addition to any other notifications)

### 6.2 Relevant national services, standards and capabilities

ID Requirement
6.2.1 National guidance (high level) will be provided for local healthcare services
around when they may need to disconnect / freeze a record (6.1.8), and how to
initiate this with suppliers. Guidance will also be provided for suppliers,
incorporating the expected timeframe for responding.
6.2.2 Information on NHS Login and the onboarding process can be accessed at
https://digital.nhs.uk/blog/transformation-blog/2020/creating-an-integration-toolkit-
for-nhs-login (6.1.1)
6.2.3 The PDS Birth Notification will be available from NEMS.
Seehttps://developer.nhs.uk/apis/ems-beta/pds_birth_notification.html. The PDS
Birth Notification will flow when the child is born, meaning that connected mode
can be initiated ante-natally (6.1.2).
6.2.4 Further information will be provided on the analytics requirement (6.1.22).
6.2.5 The PDS Death Notification will be available from NEMS. The DPCHR MUST
subscribe to the PDS Death Notification. Seehttps://developer.nhs.uk/apis/ems-
beta/pds_death_notification.html. Additionally, further detail will be provided on
the required DPCHR response to a death notification (6.1.19).
6.2.6 The mechanism by which parents / carers / guardians access the ability to
register (with an appropriate DPCHR product) to become an account holder is still
to be specified (6.1.21). The solution may be based on the NHS Apps Library.
6.2.7 The DPCHR MUST securely store both professional- and parent-entered data, in

a way that supports the different modes of access, and that enables the portability
requirements set out in 2.1.9 and 3.1.6 (6.1.5, 6.1.10).
6.2.8 National guidance (high level) will be provided for local healthcare services
around when they may need to confirm parental responsibility and how to initiate
this with suppliers. (6.1.3)
6.2.9 Guidance will be provided on wording to allow parents to make an informed
choice of DPCHR mode of access and on consent to be contacted for research
(6.1.16, 6.1.23).
6.2.10 The detailed validation requirements for professionals will be provided (6.1.12).
6.2.11 This functionality is underpinned by interoperability via the National Events
Management Service (NEMS).
6.2.12 Details of the Professional Contact message can be found in the relevant tab of
the Healthy Child Event Specification at https://theprsb.org/wp-
content/uploads/2019/05/Healthy-Child-Event-Specification-v2.2-ISN-COPY-NO-
CHANGES.xlsx and also FHIR profiles at https://developer.nhs.uk/apis/ems-
beta/overview_supported_events.html. Further guidance on how to populate the
message will be provided (6.1.25).

### 6.3 Direction of travel beyond the MVP

```
Further analytics requirements will be specified in the future, which may include providing
live dashboards to commissioners, or de-identified data being exportable to Tableau.
```

```
For changes in parental responsibility (such as adoption or a care order being issued), future
requirements could go further and allow the new parent with responsibility to inherit
Connected mode, and to have sight of information that flowed into the record prior to them
taking up responsibility.
```

```
Similarly, a future requirement may support more effectively a scenario where parental
responsibility is not changed but health professionals believe there is a risk to the child if
their location is known – for example, special guardianship orders.
```

```
A future version of the product will need to cater for a child reaching the age of ‘digital
competency’ (likely to be at some point between 11 and 13).
```

NHSX and NHSD are currently looking at how NHS Login should support proxy access
moving forward. In due course, this may result in solutions for suppliers to integrate with to
support account and record management.

There is an expectation in future that a will be a publisher to the NEMS for children who
have been authenticated for that DPCHR. Further detail on the NEMS capability can be
found here – https://developer.nhs.uk/apis/ems-beta/index.html.

Integration with the NHS App may be required / available in the future.

A further future requirements may be to allow users to view who has accessed information
about their child.

## 7 Onboarding to NHS Digital services and

## completing the SCAL

As described at 2.2.1 and 6.1.1, DPCHR suppliers are required to use the NEMs
infrastructure to subscribe to messages and to use NHS Login as an identity service to
register DPCHR accounts.

These are both national services provided by NHS Digital for which there is a particular
onboarding and assurance process which suppliers must go through, this is the Supplier
Conformance Assessment List (SCAL). The SCAL contains the key non-functional
requirements for DPCHRs.

The overview of the assessment process is available here:
https://developer.nhs.uk/apis/uec-appointments/assurance_overview.html#on-line-end-user-
agreement

Below is a diagram of the process itself:

When the process is complete, the supplier receives a Technical Conformance Certificate.

The SCAL requires that a supplier self-assess and provide evidence of conformance in
Information Governance, Security, Clinical Safety and Standards across a number of key
areas, these are:

```
Supplier and Product Information
Architecture
NEMs Subscription API
NEMS Event Receiver
DCH NEMs
NHS Login
SMS-PDS
It is important for suppliers to look at the SCAL as early as possible to understand the time
and effort and evidence required to connect their product to the national infrastructure.
An example of the SCAL is available here https://digital.nhs.uk/services/operations. SCAL
documentation is iterative so when your Expression of Interest is acknowledged, NHSx will
issue you with the version you are to complete.
```

## 8 Other Requirements

### 8 .1 Other Requirements for the MVP/ Supplier

ID Requirement
7.1.1 Further guidance will be provided on branding.
7.1.3 The DPCHR MUST align with the NHS Service Design Standards at
https://digital.nhs.uk/about-nhs-digital/our-work/nhs-digital-data-and-technology-
standards/framework/beta---service-design-standards. These reference a suite of
guidance and standards, and incorporate requirements for digital accessibility.
7.1.4 The DPCHR MUST be available through modern web and mobile browsers.
7.1.5 The DPCHR supplier MUST be a signed-up member of INTEROpen.
7.1.6 The DPCHR MUST navigate a set of assurance processes, to be specified
separately but including the NHS Digital SCAL, see Section 7.

7.1.7 The DPCHR COULD support additional personalisation, such as the ability for a
user to choose ‘connect only via wi-fi’. Any such requirements should be stored
against the parental account. (The national programme team will be keen in
gathering insights from users wherever these requirements are deployed early).

## 9 Change Control

```
The following table shows the changes in requirements from the previous version of the
document (version 0.7). An entry in green shows a new requirement or addition. All other
changes are deletions or clarifying comments.
```

ID Requirement
2.1.1
2.1.2
2.1.3
2.1.4

```
The specific data fields enumerated in these sections previously have been
removed to ensure there is no conflict with the data fields in the message
specifications which are in the developer space.
```

2.1.1 Further clarification on non-presentation of address provided _‘However DPCHR
suppliers will not display the child’_ s address at anytime to comply with
_safeguarding concerns about accidental/coerced disclosure of a child’s address’._
2.1.5 The phrase ‘with vaccines listed in chronological order’ has been removed as
parents should be able to order on any field
2.1.6 The phrase ‘(in a single chronological list)’ has been removed as parents should
be able to order on any field
2.1.8 Note added that GP address must not be displayed for safeguarding reasons
2.2.1 The following is deleted ‘The DPCHR MUST poll MESH for new events at least
every 30 minutes, 24 hours a day, 7 days a week. The relevant data must be
auto-ingested within one minute of polling of MESH (apart from blood spot results

- see 2.1.3. The DPCHR MUST keep an audit log of all received events – further
  detail will be provided’ as these are conditions of NEMS use and are covered in
  the SCAL which suppliers have to complete.
  2.2.3 Note added that GP address must not be displayed for safeguarding reasons

  3.1.1 The specific data fields enumerated in this section previously has been removed
  to ensure there is no conflict with the data fields in the message specifications
  which are in the developer space. However we do not expect parents to have to
  manage SNOMED coding except through human readable pick list functionality.
  3.1.4 The specific data fields enumerated in this section previously has been removed
  to ensure there is no conflict with the data fields in the PRSB Events specification,
  no message specification yet being available in the developer space
  3.1.13 Reference to chronological order has been removed as parents should be able to
  order on any field they choose
  6 Addition: clarifying text added to provide context for account and record
  management and connection modes. Deletion of unclear text.
  6.1.1 Addition of ‘and register for the DPCHR using this service.’ for clarification
  6.1.19 Deletion of DPCHR for clarification: it is the child’s record which is frozen, not the
  DPCHR account.
  6.1.20 Expansion of meaning, it must not affect ‘the persistence and integrity of
  professional recorded information’ in the child record)
  6.1.25 Removal of requirement for DPCHR to publish a Professional Contact message.
  7 Addition: section providing guidance on the SCAL and onboarding process
  9 Addition: change control section for easy reference as to what has been changed
  between versions.
