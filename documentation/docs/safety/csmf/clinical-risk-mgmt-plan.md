---
title: Clinical Risk Management Plan
reviewers: Dr Marcus Baw
---

# Clinical Risk Management Plan

## Document Controls

As part of our commitment to automation, transparency and open governance, this document's versioning is managed using the **Git** Distributed Version Control Software (DVCS), and the **GitHub** online code repository platform. These are currently regarded as the 'industry standard' for DVCS and online repositories, and are used by the majority of open and closed source developers worldwide. We also maintain our application and library code in Git and GitHub, meaning that our clinical safety case and documentation is managed close to our actual code.

Using the combination of Git and GitHub removes much of the manual work of maintaining document control processes, and so we have abandoned manual document controls entirely, in favour of GitHub's automatically updated controls.

To see the contributors to the documentation site you can view them here on GitHub.
Contributors: <https://github.com/rcpch/digital-growth-charts-documentation/graphs/contributors>

Most recent update: 

## Purpose

The aim of the Clinical Risk Management Plan is to ensure that all of the RCPCH Digital Growth Charts Team involved with the development, implementation and use of healthcare IT systems are aware of the activities that are required to be undertaken to ensure patient safety is improved rather than compromised from the introduction of healthcare IT systems.

The RCPCH Digital Growth Charts Team is required to adhere to National Information standards created and monitored via the Data Coordination Board (DCB) within NHS Information Standards frameworks.

The mechanisms used are approved Clinical Risk Management System compliance documents.

This Clinical Risk Management System will be reviewed periodically to ensure that:

- changes in working practices are incorporated.
- issues identified through an established internal audit programme are addressed.
- the safety approach continues to adhere to the requirements of applicable international standards.
- the system continues to protect the safety of patients in a complex and changing environment.

## Audience

This document is for the RCPCH Digital Growth Charts Team staff that are involved in ensuring the safety of the RCPCH's healthcare IT systems, products or services, but is made publicly available as part of our commitment to transparency and open governance.

## Scope

This policy applies to the the RCPCH Digital Growth Charts Team's organisation and to all of the RCPCH Digital Growth Charts Team's IT systems. The policy also applies to any local customisations, upgrades or specific configurations made to a healthcare IT system by the RCPCH Digital Growth Charts Team.

If clarification is required of whether any system falls within scope of this CRMS this should be raised with the nominated Clinical Safety Officer (CSO) for clarification. This nominated person provides clinical and organisational leadership on healthcare IT Patient Safety on behalf of the Organisation.

!!! danger "IMPORTANT NOTICE FOR SELF-HOSTING"
    IMPORTANT: This Clinical Risk Management File applies ONLY to RCPCH open source software as deployed and managed by the RCPCH Digital Growth Charts Team under our direct control.
    
--8<--
docs/_assets/_snippets/self-host-warning.md
--8<--

## Definitions

Note - Also see the RCPCH Risk Management Strategy

**CSO:** Clinical Safety Officer - the person responsible for ensuring that the healthcare IT Clinical Risk Management System is applied to all clinical systems. The Clinical Safety Officer (CSO) for the Organisation is responsible for ensuring the safety of a healthcare IT system through the application of clinical risk management. The Clinical Safety Officer must hold a current registration with an appropriate professional body relevant to their training and experience. They also need to be suitably trained and qualified in risk management or have an understanding in principles of risk and safety as applied to healthcare IT systems. The Clinical Safety Officer ensures that the processes defined by the clinical risk management system are followed.

**DCB**: Data Coordination Board

## Healthcare IT Clinical Risk Management (CRM) Governance Arrangements

The responsibility for healthcare IT CRM within the Organisation resides with the Clinical Safety Officer

Organisational management of healthcare IT related risks is as per the existing management arrangements as specified in the Organisation’s Risk Management Strategy.

### Clinical Risk Management Team Organisation Chart

The RCPCH's team is not yet of a size that it requires an org chart to explain. Left here as a placeholder in case an org chart is needed in the future.

### Personnel

#### Clinical Safety Officer

**Dr Marcus Baw**
NHS Digital-trained Clinical Safety Officer  
Registered General Medical Practitioner, GMC Number 4712729  
Software Developer  
Github [@pacharanero](https://github.com/pacharanero)  

#### Senior Clinical Adviser

**Dr Simon Chapman**
Consultant Paediatrician, King's College Hospital Trust  
Specialist in Diabetes and Endocrinology  
Software Developer  
Github [@eatyourpeas](https://github.com/eatyourpeas)  

#### Chief Digital Officer

Richard Burley
Chief Digital Officer, RCPCH

#### Chief Executive Officer

Overall governance for the RCPCH Digital Growth Charts project is provided not by a single individual, but by the R[CPCH Digital Growth Charts Project Board](../../about/team.md), which is composed of senior leadership within the RCPCH and the most eminent clinicians in the field of Growth charts.

## Governance

Governance for patient safety within the Organisation is provided through the following forums:

### Clinical Risk Meetings

- Clinical Safety is discussed as a fixed item on the two-weekly Sprint Planning Meeting at which the project is planned and priorities set for the next sprint of development.

- In the event of an **urgent** clinical safety issue or incident, a supplementary Clinical Risk meeting is held at the earliest possible time.

### Open, transparent public Issue tracking

- Open, public issue tracking ensures the widest possible reporting base, and unparalleled access to report issues compared to the majority of Health IT systems. These Issues, tracked in GitHub, directly form part of the development workflow used by the clinical and technical teams.

### Public forum

RCPCH maintains a presence on our [Discourse forum](https://forum.rcpch.tech/), where users, implementers, and clinicians can feed back on the system. This is a transparent and open mechanism for safety feedback and aftermarket surveillance of the platform. Using the same system or using our contact page it is also possible to send a private message or contact via email in the event of a private communication being necessary.

## Healthcare IT Clinical Risk Management Deliverables

### Clinical Risk Management File CRMF (this repository)

The RCPCH Digital Growth Charts Team will establish a Clinical Risk Management File (CRMF) for each safety related healthcare IT system. The purpose of the CRMF is to provide a central repository where all safety related information pertaining to the healthcare IT system is stored and controlled. This GitHub repository contains out Clinical Risk Management File.

### Clinical Risk Management Plan CRMP (this document)

The RCPCH Digital Growth Charts Team will establish a Clinical Risk Management Plan (CRMP) for each safety related healthcare IT system. The purpose of the CRMP is to identify the clinical risk management activities that are to be undertaken and the phasing of these activities in the project lifecycle.

The CRMP will also identify the resources required to discharge these clinical risk management activities.

### Hazard Log

The RCPCH Digital Growth Charts Team will establish and maintain a Hazard Log (HL) for each safety related healthcare IT system. The HL will be controlled and configured in accordance with the RCPCH Digital Growth Charts Team's document control policy.

The Hazard Log details can be viewed on the [Hazard Log page](hazard-log.md)

### Clinical Safety Case

The RCPCH Digital Growth Charts Team will establish and develop a Clinical Safety Case (CSC) for each safety related HIT system:

- [RCPCH dGC Application Programming Interface](clinical-safety-case-report.md)

### Clinical Safety Case Report

The RCPCH Digital Growth Charts Team will issue a Clinical Safety Case Report (CSCR) for each safety related healthcare IT system. The CSCR will be issued to support initial deployment and will be updated during the lifecycle of the Healthcare IT system should the safety characteristics change. The CSCR will be controlled and configured in accordance with the RCPCH Digital Growth Charts Team's document control policy. The Hazard Log will be made available within the CRMF.

- [RCPCH dGC Application Programming Interface](clinical-safety-case-report.md)

## Healthcare IT Clinical Risk Management Activities

### Hazard Identification

The RCPCH Digital Growth Charts Team will conduct hazard identification workshops to identify potential hazards associated with the deployment and use of our healthcare IT system. The[CSO](#clinical-safety-officer)will be responsible for facilitating such workshops and ensuring attendance from the RCPCH Digital Growth Charts Team. Typically, representatives from the following domains will be required:

- Technical testing team

- User research and User Experience team

- Clinical testing team

- Statistical support

- Project Board

If a healthcare IT solution is deemed not to be safety related then this decision will be formally recorded.

The technical team will advise on the best mechanism for addition of new issues to the the RCPCH Digital Growth Charts Team's project management workflow.

Where any third-party components are used to support the healthcare IT system then they will be considered in the scope of the hazard identification activities and subsequent risk assessment. Where none are used a positive declaration to this effect will be recorded in the minutes.

All identified hazards will be recorded in the [Hazard Log](hazard-log.md).

### Risk Assessment

The RCPCH Digital Growth Charts Team will conduct healthcare IT system risk assessment in accordance with the Risk Management Strategy. The Hazard Log will be updated to capture the risk assessment.

### Risk Evaluation

The RCPCH Digital Growth Charts Team will conduct healthcare IT system risk evaluation in accordance with the Risk Management Strategy The Hazard Log will be updated to capture the risk evaluation.

### Risk Control

Where the initial risk evaluation is deemed unacceptable, further risk controls will be required. the RCPCH Digital Growth Charts Team will manage healthcare IT system risk in accordance with the Risk Management Strategy.

Details of the risk control measures and evidence of effective implementation will be captured in the Hazard Log.

### Deployment and Ongoing Maintenance

To support clinical safety activities undertaken during any deployment phases of a project or programme of work the following documentation will be required to form a part of the overall approval process.

Deployment of changes to any of the RCPCH dGC Health IT systems follows an industry-standard pattern of 'code promotion' using a Git Branch-based strategy. New features are developed in branches specific to that feature. Following successful testing, user acceptance, and automated tests, a successful feature can be merged into the next branch 'up' which may be a `test` branch or other nomenclature. The process of merging requires code review by nominated individuals and is a further opportunity for clinical safety review.

Code in the `live` branch is changed relatively infrequently (except for urgent security or safety updates) but the code which is promoted into `live` would have by then undergone several rounds of review as it progressed through our branch promotion strategy.

### Incident Management

Clinical Risk Management activities within the Organisation and the healthcare IT programmes and services offered are completed within the corporate risk management strategy. As such, clinical safety related incidents are dealt with in a similar manner as other incidents within the organisation such as financial, reputational, technical and other service-impacting categories.

### Safety Incident Management Process

The first step in any possible Safety Incident is to inform the Clinical Safety Officer. The CSO will determine the most appropriate course of action and will record the incident, the hazards identified (if any) and the mitigations and other remediation taken in a GitHub Issue relevant to the software element in question. Senior management of RCPCH will be informed at the earliest opportunity.

### Security Incident Management Process

Security issues may be responsibly disclosed to <growth.digital@rcpch.ac.uk> for immediate action. We recognise and respect the work of security researchers and will treat your contribution with gratitude and appropriate action. We do not engage in vexatious CMA litigation.

Internally we treat security issues with the highest priority. Once the 'acute phase' of any security threat is handled, we will then follow the Safety Incident Management Process, usually converting to a public GitHub Issue.

## Clinical Safety Competence and Training

### Overview

The clinical safety activities described in this Clinical Risk Management System shall be undertaken by competent staff. Suitable training shall be undertaken by staff to maintain and expand their level of competence.

### Competency

All of the staff identified in the clinical safety documentation shall be sufficiently competent for the roles and tasks which they are asked to undertake. Where an individual does not yet have sufficient experience or knowledge, then that person shall be monitored, and his/her work reviewed, by someone who has the necessary competence. Such supervision shall prevail until it is judged that the individual has amassed the necessary experience to undertake such tasks unsupervised.

In assessing competency, the different functional roles required to fully discharge the obligations of the Clinical Risk Management System,and the necessary skills and knowledge needed for each, shall be considered. Primary functional roles may include: - Conducting discrete safety analyses (for example, a HAZOP or FFA) or defining the Hazard Risk Indicators for a particular project.

- Making a valid judgement on the safety tasks, activities and techniques required for a given Health Software Product in order to justify the comprehensiveness and completeness of the safety assessment and produce the safety argument with supporting evidence.

- Assurance of safety assessments and healthcare IT software products. Performance of safety techniques and development of the safety argument for a particular healthcare IT software product must be independent to any assurance activities for the same.

- Improving and refining the overall Clinical Risk Management System, for example, audit, process change, quality.

- Ownership and leadership, for example, ultimate safety accountability, culture change, influencing and strategic direction.

- The first test in establishing competency shall be at the interview stage where potential staff shall be assessed against the above representative roles and agreed job descriptions. Thereafter, competence shall be monitored through the organisation’s established appraisal scheme. Any perceived deficiencies identified during the course of the work or at the appraised stage, especially during probation, shall be addressed immediately, for example, through the assignment of a competent supervisor or the provision of suitable training.

- All registered clinicians involved in safety roles shall, as a minimum,have completed an accredited training course.

### Training

- As part of the employment process and thereafter through the appraisal scheme, clinical safety personnel will undergo suitable training to develop, maintain or enhance their competency level. Such training can comprise: - ‘on the job’ training conducted under supervision - Internal training courses - Approved external training courses.

- All registered clinicians involved in clinical safety roles shall, as a minimum, have completed an accredited training course.

- Completion of any safety training shall be recorded by the individual on the annual appraisal form.

## Audits

### Overview

Audits shall be undertaken to ensure that projects are adhering to the defined safety requirements. Such audits will focus on the **Clinical Safety Team** and **third-party** suppliers.

### Internal Safety Audits

- the RCPCH Digital Growth Charts Team shall undertake regular internal safety audits to ensure that projects undertaken within the organisation are compliant with this Clinical Risk Management System. These audits shall be conducted and recorded in accordance with the internal quality management procedure.

- The scope of an internal safety audit will be the formal Clinical Risk Management System and the organisation’s documentation supporting this document.

### Supplier Audits

The RCPCH Digital Growth Charts Team shall undertake regular third-party supplier audits, as a minimum annually, to ensure compliance with their Clinical Risk Management System. The audit shall focus on the Clinical Risk Management System, the evidence which demonstrates its effective operation and any issues arising from the deployment of the healthcare IT products and services. The basis for the audit shall be DCB0129.