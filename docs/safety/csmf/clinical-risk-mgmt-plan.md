---
title: Clinical Risk Management Plan
reviewers: Dr Marcus Baw
---

# Clinical Risk Management Plan

## Purpose

The aim of the Clinical Risk Management Plan is to ensure that all of the RCPCH dGC Team involved with the development, implementation and use of healthcare IT systems are aware of the activities that are required to be undertaken to ensure patient safety is improved rather than compromised from the introduction of healthcare IT systems.

The RCPCH dGC Team is required to adhere to National Information standards created and monitored via the Data Coordination Board (DCB) within NHS Information Standards frameworks.

The mechanisms used are approved process Clinical Risk Management System compliance documents.

This Clinical Risk Management System will be reviewed periodically to ensure that:

- changes in working practices are incorporated.
- issues identified through an established internal audit programme are addressed.
- the safety approach continues to adhere to the requirements of applicable international standards.
- the system continues to protect the safety of patients in a complex and changing environment.

## Audience

This document is for the RCPCH dGC Team staff that are involved in ensuring the safety of the RCPCH's healthcare IT systems, products or services, but is made publicly available as part of our commitment to transparency and open governance.

## Scope

This policy applies to the the RCPCH dGC Team's organisation and to all of the RCPCH dGC Team's IT systems. The policy also applies to any local customisations, upgrades or specific configurations made to a healthcare IT system by the RCPCH dGC Team.

If clarification is required of whether any system falls within scope of this CRMS this should be raised with the nominated Clinical Safety Officer (CSO) for clarification. This nominated person provides clinical and organisational leadership on healthcare IT Patient Safety on behalf of the Organisation.

!!! danger "IMPORTANT NOTICE FOR SELF-HOSTING"
    IMPORTANT: This Clinical Risk Management File applies ONLY to RCPCH open source software as deployed and managed by the RCPCH dGC Team under our direct control.
    
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

Dr Marcus Baw [@pacharanero](https://github.com/pacharanero)

#### Senior Clinical Adviser

Dr Simon Chapman [@eatyourpeas](https://github.com/eatyourpeas)

#### Chief Technology Officer

Andrew Palmer

#### Chief Executive Officer

Overall governance for the RCPCH Digital Growth Charts project is provided not by a single individual, but by the RCPCH Digital Growth Charts Project Board, which is composed of senior leadership within the RCPCH and the most eminent clinicians in the field of Growth charts.

## Governance

Governance for patient safety within the Organisation is provided through the following forums:

### Clinical Risk Meetings

- Clinical Safety is discussed as a fixed item on the two-weekly Sprint Planning Meeting at which the project is planned and priorities set for the next sprint of development.

- In the event of an **urgent** clinical safety issue or incident, a supplementary Clinical Risk meeting is held at the earliest possible time.

### Open, transparent public Issue tracking

- Open, public issue tracking ensures the widest possible reporting base, and unparalleled access to report issues compared to the majority of Health IT systems. These Issues, tracked in GitHub, directly form part of the development workflow used by the clinical and technical teams.

## Healthcare IT Clinical Risk Management Deliverables

### Clinical Risk Management File (this repository)

The RCPCH dGC Team will establish a Clinical Risk Management File (CRMF) for each safety related healthcare IT system. The purpose of the CRMF is toprovide a central repository where all safety related information pertaining to the healthcare IT system is stored and controlled. This GitHub repository contains out Clinical Risk Management File.

### Clinical Risk Management Plan (this document)

The RCPCH dGC Team will establish a Clinical Risk Management Plan (CRMP) for each safety related healthcare IT system. The purpose of the CRMP is to identify the clinical risk management activities that are to be undertaken and the phasing of these activities in the project lifecycle.

The CRMP will also identify the resources required to discharge these clinical risk management activities.

### Hazard Log

The RCPCH dGC Team will establish and maintain a Hazard Log (HL) for each safety related healthcare IT system. The HL will be controlled and configured in accordance with the Organisation document control /quality management policy \[provide a reference\].

### Clinical Safety Case

The RCPCH dGC Team will establish and develop a Clinical Safety Case (CSC) for each safety related HIT system:

- RCPCH dGC Application Programming Interface
- RCPCH Demo React Client (not for direct clinical use)
- RCPCH React Component

### Clinical Safety Case Report

The RCPCH dGC Team will issue a Clinical Safety Case Report (CSCR) for each safety related healthcare IT system. The CSCR will be issued to support initial deployment and will be updated during the lifecycle of the healthcare IT system should the safety characteristics change. The CSCR will be controlled and configured in accordance with the Organisation’s document control policy \[provide a reference\]. The HL will be made available within the CRMF.

## Healthcare IT Clinical Risk Management Activities

### Hazard Identification

The RCPCH dGC Team will conduct hazard identification workshops to identify potential hazards associated with the deployment and use of our healthcare IT system. The[<span class="underline">CSO</span>](#clinical-safety-officer)will be responsible for facilitating such workshops and ensuring attendance from the RCPCH dGC Team. Typically, representatives from the following domains will be required:

- Technical testing team

- User research and User Experience team

- Clinical testing team

- Statistical support

- Project Board

The workshops will have minutes taken and a copy stored in the[<span class="underline">CRMF</span>](#clinical-risk-management-file).

If a healthcare IT solution is deemed not to be safety related then this decision will be formally recorded.

The technical team will advise on the best mechanism for addition of new issues to the the RCPCH dGC Team's project management workflow.

Where any third-party components are used to support the healthcare IT system then they will be considered in the scope of the hazard identification activities and subsequent risk assessment. Where none areused a positive declaration to this effect will be recorded in the minutes.

All identified hazards will be recorded in the Hazard Log.

### Risk Assessment

the RCPCH dGC Team's Health will conduct healthcare IT system risk assessment inaccordance with the Risk Management Strategy. The Hazard Log will be updated to capture the risk assessment.

### Risk Evaluation

The RCPCH dGC Team will conduct healthcare IT system risk evaluation inaccordance with the Risk Management Strategy The Hazard Log will be updated to capture the risk evaluation.

### Risk Control

Where the initial risk evaluation is deemed unacceptable, further risk controls will be required. the RCPCH dGC Team will manage healthcare IT system risk in accordance with the Risk Management Strategy.

Details of the risk control measure and evidence of effective implementation will be captured in the Hazard Log.

### Deployment and Ongoing Maintenance

To support clinical safety activities undertaken during any deployment phases of a project or programme of work the following documentation will be required to form a part of the overall approval process.

Deployment of changes to any of the RCPCH dGC health IT systems follows an industry-standard pattern of 'code promotion' using a Git Branch-based strategy. New features are developed in branches specific to that feature. Following successful testing, user acceptance, and automated tests, a successful feature can be merged into the next branch 'up' which may be an 'alpha' or other nomenclature. The process of merging requires code review by nominated individuals and is a further opportunity for clinical safety review.

Code in the 'live' branch is changed relatively infrequently (except for urgent security or safety updates) but the code which is promoted into 'live' wuld have by then undergone several rounds of review as it progressed through our branch promotion strategy.

### Incident Management

Clinical Risk Management activities within the Organisation and thehealthcare IT programmes and services offered are completed within the corporate risk management strategy. As such, clinical safety related incidents are dealt with in a similar manner as other incidents within the organisational such as financial,reputational, technical and other service impacting categories.

### Safety Incident Management Process

### Security Incident Management Process

Security issues may be responsibly disclosed to growth.digital@rcpch.ac.uk for immediate action. We recognise and respect the work of security researchers and will treat your contribution with gratitude and appropriate action. We do not engage in vexatious CMA litigation.

Internally we treat security issues with the highest priority. Once the 'acute phase' of any security threat is handled, we will then follow the Safety Incident Management Process, usually converting to a public GitHub Issue.

## Clinical Safety Competence and Training

### Overview

The clinical safety activities described in this Clinical Risk Management System shall be undertaken by competent staff. Suitable training shall be undertaken by staff to maintain and expand their level of competence.

### Competency

All of the staff identified in the organisation chart, shall be sufficiently competent for the roles and tasks which they are asked to undertake. Where an individual does not yet have sufficient experience or knowledge, then that person shall be monitored, and his/her work reviewed, by someone who has the necessary competence. Such supervision shall prevail until it is judged that the individual has amassed the necessary experience to undertake such tasks unsupervised.

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

Audits shall be undertaken to ensure that projects are adhering to thedefined safety requirements. Such audits will focus on the **ClinicalSafety Team** and **third-party** suppliers.

### Internal Safety Audits

- the RCPCH dGC Team shall undertake regular internal safety audits to ensure that projects undertaken within the organisation are compliant with this Clinical Risk Management System. These audits shall be conducted and recorded in accordance with the internal quality management procedure.

- The scope of an internal safety audit will be the formal Clinical Risk Management System and the Organisation’s documentation supporting this document.

### Supplier Audits

The RCPCH dGC Team shall undertake regular third-party supplier audits, as a minimum annually, to ensure compliance with their Clinical Risk Management System. The audit shall focus on the Clinical Risk Management System, the evidence which demonstrates its effective operation and any issues arising from the deployment of the healthcare IT products and services. The basis for the audit shall be DCB0129.

Supplier audits shall be conducted in accordance with the External Safety Audit Procedure.
