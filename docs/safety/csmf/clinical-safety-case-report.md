---
title: Clinical Safety Case Report
reviewers: Dr Marcus Baw
---

# Clinical Safety Case Report for the RCPCH Digital Growth Charts Platform

## Document Controls

| Version control                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The revisions of this document are managed in the Git version control system and are visible by reviewing the Git commit log, which is here <https://github.com/rcpch/digital-growth-charts-documentation/commits/live/docs/safety/csmf> |

| Reviewers        |                                                                   |
| ---------------- | ----------------------------------------------------------------- |
| Dr Marcus Baw    | Lead Developer, General Practitioner, Clinical Safety Officer     |
| Dr Simon Chapman | Lead Developer, Consultant Paediatrician, Clinical Safety Officer |

| Approvers     |                         |
| ------------- | ----------------------- |
| Dr Marcus Baw | Clinical Safety Officer |

## Introduction

The purpose of the DCB0129 Clinical Safety Case Report is to describe the clinical safety processes and assurances applied to the RCPCH Digital Growth Charts Platform in its manufacture. In deployment or implementation, a further DCB0160 clinical safety case will be required.

## System Definition / Overview

The RCPCH Digital Growth Charts Platform consists of a suite of software tools which together enable the calculation and display of important growth-related parameters for children ranging in age from severely premature up to the age of around 20.

For the purposes of this Safety Case, the principal components are:

1. a [The Digital Growth Charts API Server](../../products/api-server.md), which recieves measurements and returns the calculations
2. a [The React.js chart component](../../products/react-component.md), which takes the returned calculation information and shows it as a HTML-based visual growth chart which clinicians would recognise and be able to safely interpret and use for the clinical care of their patient.

## Intended Use

The RCPCH Digital Growth Charts Platform is intended to be deployed within other systems, principally Electronic Patient Records (EPRs), Electronic Health Records (EHRs), Personal Health Records (PHRs), and other software platforms. The commercial subscription API service provided by the RCPCH is warranted to have undergone the testing and assurance described in this document.

If using the API service in any other 'unofficial' way, such as self-hosting, reverse-engineering, or misusing internal dGC components outwith the RCPCH Platform - this is deemed to be usage **outwith** any provisions of this document. The RCPCH Clinical Safety Officer expressly disclaims any responsibility for usage of the RCPCH dGC Platform outwith of its intended commercial use.

## Clinical Risk Management System

A full description of the Clinical Risk Management System in place at the RCPCH is detailed in the section on [Clinical Risk Management System](clinical-risk-mgmt-system.md).

Clinical safety and risk management are well-embedded within the culture of the RCPCH Incubator

The Clinical Risk Management File is currently maintained by the Clinical Safety Officer, and contains all the relevant documentation related to the clinical safety of the RCPCH Digital Growth Charts Platform.

The Clinical Safety Officer (CSO) is responsible for clinical safety of RCPCH Digital Growth Charts Platform, through the application of clinical risk management procedure. The CSO is a suitably qualified and experienced clinician who holds current registration with their relevant professional body and has had appropriate training for this role. In the RCPCH the CSO role is held by one of the lead developers.

## Clinical Risk Analysis

Hazard Identification Workshops were held, involving the entire RCPCH dGC Project Board, the Clinical Safety Officer, the Development team, and the supporting RCPCH staff team, at which hazards affecting the Digital Growth Charts were discussed and the risk levels identified.

## Hazard Log

A [Hazard Log](hazard-log.md) was established using GitHub Issues as a mechanism for logging the Hazard, quantifying risk severity and likelihood and overall risk level. Steps were then taken to reduce and mitigate risks down to acceptable levels, using the DCB0129 definitions for acceptability.

More detail of the individual risks and descriptions of the pre- and post-mitigation risk levels are within the text of each of the Hazards in the Hazard Logs.

![risk-matrix](../../_assets/_images/risk-matrix.png)

---

### Hazard: Unavailability of the dGC API calculation and charting functions

<https://github.com/rcpch/digital-growth-charts-documentation/issues/51>

#### Description of initial Risk and mitigation steps

The API server runs on high-availability Microsoft Azure public cloud infrastructure and is hardened to above industry standard.

The Project Board felt the unavailability of the API would be unlikely to cause any form of harm to a patient because there are immediately available fallback methods such as manual calculation on printed paper charts.

#### Severity

Minor

#### Likelihood

Medium

#### Residual Risk Level

#### Outcome

                                    |                      | Level 1 - Acceptable  |

| | RCPCH endeavours to ensure that implementer organisations have appropriate support in order to reduce the risk of errors in passing data to the API | Level 1 - Transferred |
| Misuse of the API code by external organisations

---

### Hazard: Wrong data is _entered into_ the Digital Growth Chart API

#### Description of initial Risk and mitigation steps

In both the above scenarios, our Project Board of clinical paediatrics and growth experts agreed that the absolute risk of directly attributable harm to a child is rather low, because of the multiple clinical practice safeguards that exist whether the growth chart is paper, PDF or digital.

#### Severity

#### Likelihood

#### Residual Risk Level

#### Outcome

RCPCH endeavours to ensure that implementer organisations have appropriate support in order to reduce the risk of errors in passing data to the API, however much of the implementation risk must necessarily be passed on to the DCB0160 clinical safety assessment.

---

### Hazard: Incorrect centile data is _returned by_ the API



#### Description of initial Risk and mitigation steps

Prior to deployment of the Digital Growth Charts, significant 'static' software testing was performed, to ensure that the complex statistical calculations returned by the API had been confirmed to have a very high degree of conformity to previous statistical Centile calculation engines, across a synthetic 'test harness' of approximately 4000 children's data. It is worth noting that the agreement between the systems was to 4 decimal places, the small variation between these is accounted for by the fact that statistics uses complex modelling of curves and interpolation, so it is impossible to get perfect alignment between two systems written in different languages (in this case, R and Python).

This testing process was supervised directly by Prof Tim Cole, a distinguished UK Child Health statistician and the originator of using the LMS Method for centile charts. The degree of error in calculation was deemed to be clinically insignificant, representing around _one-ten-thousandth_ of a Centile percentage point, in a clinical measurement context in which significant variations are found simply in the measurement technique itself (for example weighing and measuring a moving baby).

End-to-end testing of the platform was also manually performed to 'spot check' that the data entered for a generated synthetic child was corroborated against analogue calculations of centile values.

#### Severity

Major

#### Likelihood

Very Low

#### Residual Risk Level

#### Outcome

---

### Hazard: Misuse of the API code by external organisations

#### Description of initial Risk and mitigation steps

#### Severity

#### Likelihood

#### Residual Risk Level

#### Outcome

---

## Test Issues

There are no outstanding test issues from a DCB0129 standpoint. Implementers will be expected to conduct their own User Acceptance Testing as part of development and roll-out of their solution, and their feedback may inform future development of the RCPCH Digital Growth Charts Platform.

## Summary Safety Statement

This document recommends that the RCPCH Digital Growth Charts platform is suitable for clinical deployment and use, subject to further DCB0160 clinical risk management within the deploying organisation, and with support from the RCPCH in correct and safe deployment.

## Quality Assurance and Document Approval

This document is currently written by the CSO with support from the RCPCH Incubator and Development Team who have undergone the necessary training on clinical safety in Healthcare IT systems. The other activities which support the creation of this document include the hazard identification workshops which are supported by the RCPCH Project Board and other clinical and administrative staff.

This report is then reviewed by the Deputy Clinical Safety Officer, Lead Developers, dGC Product Owner, dGC Project Manager, and Chief Digital Officer before a recommendation is made.
