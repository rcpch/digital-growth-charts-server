---
title: Technical Documentation
reviewers: Dr Marcus Baw
---

# Technical Documentation for EU Medical Device Regulation

## Digital Growth Charts Project

1. ### Your name and address, or those of any authorised representatives

The Royal College Of Paediatrics and Child Health (RCPCH), 5-11 Theobalds Road, London, WC1X 8SH (telephone: +44 (0)20 7092 6000).

1. ### A brief description of the product

A web-based software program which allows communication between user and/or back-end applications/databases (API - application programming interface) intended to assist a clinician by calculating variation in children's growth parameters [e.g., height, weight, head circumference, body mass index (BMI)] based on input data (e.g., birth height and weight, gender, gestation). The information may be used to detect children developing underweight or overweight, with height abnormalities or other related disorders.

1. ### Identification of the product, for example, the product's serial number

RCPCH Digital Growth Charts Platform, comprising of:

--8<--
docs/_assets/_snippets/dgc-platform-comprises.md
--8<--

This documentation pertains to **all versions** of the product. Current latest versions can be viewed by consulting the relevant repository at the RCPCH GitHub organisation <https://github.com/rcpch>

1. ### The name(s) and address(es) of the facilities involved in the design and manufacture of the product

The product was designed and developed entirely remotely by a geographically dispersed team, and online using collaboration software such as Git, GitHub, Google Meet, Microsoft Teams, and Signal instant messaging.

The 'place of manufacture' of the product could be most accurately said to be the code collaboration platform [GitHub](https://github.com/), and the primary tooling used in the manufacture was Microsoft Visual Studio Code.

1. ### The name and address of any notified body involved in assessing the conformity of the product

**Not Applicable** due to the Class I designation of the Device

1. ### A statement of the conformity assessment procedure that has been followed

**Not Applicable** due to the Class I designation of the Device

1. ### The EU declaration of conformity

See [Declaration of Confomity](doc-api.md)

1. ### Label and instructions of use

All instructions for use are contained within [this documentation website](/).

1. ### A statement of relevant regulations to which the product complies

* Regulation (EU) 2017/745 - Medical Devices

1. ### Identification of technical standards with which compliance is claimed

There are no technical standards pertaining directly to the manufacture of this kind of medical device.

1. ### A list of parts

1. #### Compliant parts

   * Digital Growth Charts Application Programming Interface **Server**, **Version 1**

   * Digital Growth Charts Application Programming Interface **React Charting Component**, **Version 1**

   * Digital Growth Charts Application Programming Interface **Demo React Client**, **Version 1**

   * Digital Growth Charts Application Programming Interface **Demo React Native Client**, **Version 1**

1. #### Supplementary parts (for which compliance is not claimed)

1. ### Test results

    Automated tests on the programs are run on every code change. If the tests fail then the new code cannot be incorporated into the program, and the previous version will remain in place.

    Tests can be viewed in the `test/` directory within each repository.

    All repositories are listed at <https://github.com/rcpch>
