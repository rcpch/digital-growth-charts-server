---
title: Command-line tools
reviewers: Dr Marcus Baw, Dr Simon Chapman
---

# Command-line growth tools

Partly for our own uses, we've wrapped the [Python package](python-library.md) in a command-line tool so that you can use the power of the growth functions in the `rcpchgrowth-python` package conveniently in the terminal.

![command-line-tool](../_assets/_images/command-line-tool.png)

:octicons-mark-github-16: [GitHub repository](https://github.com/rcpch/rcpchgrowth-python-cli)

:material-web: link

[![Upload Python Package](https://github.com/rcpch/rcpchgrowth-python-cli/actions/workflows/python-publish.yml/badge.svg)](https://github.com/rcpch/rcpchgrowth-python-cli/actions/workflows/python-publish.yml)

To use:

```console
foo@bar:~$ pip3 install rcpchgrowth-cli
foo@bar:~$ python3 -m rcpchgrowth-python-cli
foo@bar:~$ rcpchgrowth --help
```

There are 4 functions:

## age-calculation

This returns a decimal age from 2 dates. If the gestation is supplied with the adjustment flag, a correction is made.

### required arguments (argument order sensitive):

* birth_date: format YYYY-M-D
* observation_date: format YYYY-M-D
Note the command line will usually error if a leading 0 is supplied.

### non-essential arguments:

* gestation_weeks: this is an integer which defaults to 40 if not specified
* gestation-days: this is an integer which defaults to 0 if not specified

### option

```console
-a
--adjustment
```

This flag is added with the gestation if a corrected age is needed.

### example:

```console
foo@bar:~$ rcpchgrowth age-calculation 1759-10-10 1759-11-12 28 2 -a
 ____   ____ ____   ____ _   _  ____                   _   _     
|  _ \ / ___|  _ \ / ___| | | |/ ___|_ __ _____      _| |_| |__  
| |_) | |   | |_) | |   | |_| | |  _| '__/ _ \ \ /\ / / __| '_ \ 
|  _ <| |___|  __/| |___|  _  | |_| | | | (_) \ V  V /| |_| | | |
|_| \_\\____|_|    \____|_| |_|\____|_|  \___/ \_/\_/  \__|_| |_|
                                                                 

Calculates decimal age, either chronological or corrected for gestation if the adjustment flag is true. Params: birth_date, observation_date, gestation_weeks, gestation_days
Adjusted: -0.13415468856947296 y,
1 month and 2 days
```

## measurement-for-sds

This function returns a measurement for an SDS.
### required arguments (argument order sensitive)

* decimal_age: a float value
* measurement_method: one of 'height', 'weight', 'bmi' (body mass index) or 'ofc' (head circumference)
* sex: one of 'male' or 'female'
* SDS: a float value

### option

```console
-r
--reference
```

This defaults to uk-who if not provided. If provide, parameters are one of 'uk-who', 'trisomy-21' or 'turners-syndrome'

### example

```console
foo@bar:~$ rcpchgrowth measurement-for-sds 8.3 height female 0.72 --reference turners-syndrome
 ____   ____ ____   ____ _   _  ____                   _   _     
|  _ \ / ___|  _ \ / ___| | | |/ ___|_ __ _____      _| |_| |__  
| |_) | |   | |_) | |   | |_| | |  _| '__/ _ \ \ /\ / / __| '_ \ 
|  _ <| |___|  __/| |___|  _  | |_| | | | (_) \ V  V /| |_| | | |
|_| \_\\____|_|    \____|_| |_|\____|_|  \___/ \_/\_/  \__|_| |_|
                                                                 

Reference: Turner's Syndrome
SDS 0.72
Centile: 76.424 %
height: 115.79078818040003 cm
```

## sds-for-measurement

### required arguments (argument order sensitive)

* decimal_age: a float value
* measurement_method: one of 'height', 'weight', 'bmi' (body mass index) or 'ofc' (head circumference)
* sex: one of 'male' or 'female'
* observation_value: a float value

### option

```console
-r
--reference
```

This defaults to uk-who if not provided. If provide, paramaters are one of 'uk-who', 'trisomy-21' or 'turners-syndrome'
### example

```console
foo@bar:~$ rcpchgrowth sds-for-measurement 16.3 ofc female 55
 ____   ____ ____   ____ _   _  ____                   _   _     
|  _ \ / ___|  _ \ / ___| | | |/ ___|_ __ _____      _| |_| |__  
| |_) | |   | |_) | |   | |_| | |  _| '__/ _ \ \ /\ / / __| '_ \ 
|  _ <| |___|  __/| |___|  _  | |_| | | | (_) \ V  V /| |_| | | |
|_| \_\\____|_|    \____|_| |_|\____|_|  \___/ \_/\_/  \__|_| |_|
                                                                 

Reference: UK-WHO
SDS: -0.27811780457145885
Centile: 39.0 %
```

## measurement-for-centile

This function returns a measurement for an centile.
### required arguments (argument order sensitive)

* decimal_age: a float value
* measurement_method: one of 'height', 'weight', 'bmi' (body mass index) or 'ofc' (head circumference)
* sex: one of 'male' or 'female'
* centile: a float value

### option

```console
-r
--reference
```

This defaults to uk-who if not provided. If provide, paramaters are one of 'uk-who', 'trisomy-21' or 'turners-syndrome'

### example

```console
foo@bar:~$ rcpchgrowth measurement-for-centile 3.4 weight male 25.0 --reference trisomy-21
 ____   ____ ____   ____ _   _  ____                   _   _     
|  _ \ / ___|  _ \ / ___| | | |/ ___|_ __ _____      _| |_| |__  
| |_) | |   | |_) | |   | |_| | |  _| '__/ _ \ \ /\ / / __| '_ \ 
|  _ <| |___|  __/| |___|  _  | |_| | | | (_) \ V  V /| |_| | | |
|_| \_\\____|_|    \____|_| |_|\____|_|  \___/ \_/\_/  \__|_| |_|
                                                                 

Reference: Trisomy 21/Down's Syndrome
SDS -0.674
Centile: 25.0 %
weight: 12.367721906931306 kg
```