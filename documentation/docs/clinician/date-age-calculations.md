---
title: Date and Age Calculations
reviewers: Dr Marcus Baw, Dr Anchit Chandran
audience: clinicians, health-staff, statisticians
---

# Date and Age Calculations

## Decimal Age

Decimal age is expressed as a decimal fraction in units of years. It is calculated as the number of days / 365.25. The extra 0.25 is to account for the leap year which comes round every 4 years.

A pregnancy lasts 40 weeks (280 days). This is calculated from the date of the baby's mother's last menstrual period. In fact, from that date, ovulation occurs midway through the following cycle (on average 14 days into a 28-day cycle). This means that from conception, a pregnancy actually lasts only 266 days. Babies are considered to have been born 'term' if delivered anywhere from 37 to 42 weeks gestation (3 weeks before to 2 weeks after the due date).

The due date is referred to as the Estimated Date of Delivery (EDD).

## Gestational Age / Post-menstrual Age

Gestational age at birth is the gestation at which the infant was born, and represents the number of weeks (and extra days) since the last menstrual period. It is often shortened to gestational age, with "at birth" being assumed.

After delivery, the gestational age of preterm infants is often tracked by clinicians in addition to chronological age (and is sometimes referred to as post-menstrual age).

## Chronological Decimal Age

This is the time elapsed since birth, in years, irrespective of the gestational age at birth. For example the chronological age at EDD, i.e. at 40 weeks gestation, of a baby born at 24 weeks gestation would be 16 weeks or (16 x 7)/365.25 = 0.31 years.

## Corrected Decimal Age

Used for preterm children, the *corrected decimal age* is calculated from their *due date*, rather than their birth date (which will be earlier than their due date, owing to prematurity).

This correction adjusts for the immaturity of preterm babies born early. The process is referred to as *gestational age correction*. Prior to digital growth charts, it was a manual process.

The previous convention was to apply gestational age correction to all babies born before 37 weeks gestation. For those born at 32-36 weeks, the correction was applied until the baby was 1 year old (in _corrected_ years), and below 32 weeks until they were 2 years old (in _corrected_ years).

Now the correction is applied automatically by the API, the Project Board decided it made no sense to stop the correction at arbitrary ages, and it should be applied throughout childhood. Of course, the difference between corrected and uncorrected age becomes less apparent as the child gets older.

A further Project Board decision was to extend the gestational age correction to all children, including those born at term. This represents a departure from the previous practice of using a common reference for all term gestation babies, averaged across gestations 37-42 weeks. Now term babies, like preterm babies, are assessed using their gestational age. Equally, babies born post 40 weeks are corrected backwards. There is no upper limit to this.
