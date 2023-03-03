---
title: Reference Data
reviewers: Dr Marcus Baw, Dr Simon Chapman, Dr Anchit Chandran
---

# Growth Chart References

Growth Charts are built from reference data. A number of different datasets are available, and in the UK, we currently use a hybrid of two: the British 1990 or **UK 1990** dataset and the **World Health Organization (WHO)** dataset. The current UK charts are referred to as **UK-WHO**.

In general, datasets or growth references relate to the population of a geographical area (UK90, US Centers for Disease Control or CDC 2000), or are specific to a particular condition or disease state.

As part of this project, we have internationally catalogued the available datasets or growth references. The UK references are only usable under MRC licence. The WHO or CDC data are freely available open data.

Though not an exhaustive list, the aim is a repository for all LMS references - not only for growth, but for all other physiological parameters. This collection is incomplete at present. We welcome submissions to the repository to build the collection - please send [pull requests](https://github.com/rcpch/growth-references/pulls) or contact us on [growth.digital@rcpch.ac.uk](mailto:growth.digital@rcpch.ac.uk).

The codebase we have built is capable of utilising any reference or dataset, but there might need to be small configurations necessary to allow for the differences between them.

!!! info
    We are working on a 'standard format' of JSON, which contains reference metadata alongside the LMS tables themselves, in a 'key-value' format that makes programmatic lookups consistent across different references. Along with the data file, we request the following: file name, parameters described, acknowledgement text, authors, publication / reference.

## Reference Library

| identifier | Age Range           | Description                                                                    | Country          | Links                                                                   |
| ---------- | ------------------- | ------------------------------------------------------------------------------ | ---------------- | ----------------------------------------------------------------------- |
| cdc2000    |                     | length/height, weight & head circumference for ages 0 to 19.9y; BMI 2 to 19.9y | :us:             | [link](https://github.com/rcpch/growth-references/tree/main/cdc2000)     |
| spirometry | 4 - 80 years        | FEV1, FVC, FEV1FVC & FEF2575                                                   | :gb:             | [link](https://github.com/rcpch/growth-references/tree/main/spirometry) |
| trisomy21  |                     | Trisomy 21 Growth Standards 2002                                               | :gb: :ie:        | [link](https://github.com/rcpch/growth-references/tree/main/trisomy21)  |
| turner     |                     | Turner Syndrome, Heights 2002                                                  | :gb: :ie:        | [link](https://github.com/rcpch/growth-references/tree/main/turner)     |
| uk-who     | 23 weeks - 20y      | UK90 and WHO Child Growth Standards                                            | :gb:             | [link](https://github.com/rcpch/growth-references/tree/main/uk-who)     |
| uk90       | 23 weeks - 20 years | UK 1990 reference data, reanalysed 2009                                        | :gb:             | [link](https://github.com/rcpch/growth-references/tree/main/uk90)       |
| who2006    |                     | WHO Child Growth Standards                                                     | :united_nations: | [link](https://github.com/rcpch/growth-references/tree/main/who2006)    |

---

1. Average values at birth for weight, length and head circumference for all term births (gestations 37+0 to 42+6 weeks) computed from UK 1990 reference database.

2. Weight, and head circumference at birth (gestations 23 to 43 weeks) and length at birth (gestations 26 to 43 weeks), computed from UK 1990 reference database and shown by week.

3. This is the WHO standard for weight, BMI and head circumference from 2 weeks to 4 years, for length 2 weeks to 2 years and height 2-4 years. It is shown by week to 13 weeks and then by calendar month. It is exactly the same data as the LMS data included in the Z-score tables accessed from the WHO website [WHO](http://www.who.int/childgrowth/standards), except there is no birthweight.

### To be added

1. **LMSdata_BP** systolic & diastolic blood pressure for ages 4 to 24 yr.

### Citations

1. Freeman JV, Cole TJ, Chinn S, Jones PRM, White EM, Preece MA. Cross sectional stature and weight reference curves for the UK, 1990. Arch Dis Child 1995;73:17-24.

2. Cole TJ, Freeman JV, Preece MA. 1998. British 1990 growth reference centiles for weight, height, body mass index and head circumference fitted by maximum penalized likelihood. Stat Med 1998;17:407-29

3. WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Length/Height-for-age, Weight-for-age, Weight-for-length, Weight-for-height and Body Mass Index-for age. Methods and Development. 2006. ISBN 924 15 4 693X.

4. WHO Multicentre Growth Reference Study Group. WHO Child Growth Standards: Head circumference-for-age, arm circumference-for-age, triceps skinfold-for-age and subscapular skinfold-for age. Methods and Development. 2007. ISBN 978 92 4 1547185.

5. Down's syndrome centiles - Styles ME, Cole TJ, Dennis J, Preece MA. New cross sectional stature, weight and head circumference references for Down’s syndrome in the UK and Republic of Ireland. Arch Dis Child 2002;87:104-8. BMI centiles added 11/11/2013

6. Lyon AJ, Preece MA, Grant DB. Growth curve for girls with Turner syndrome. Arch Dis Child 1985;60:932-935.
