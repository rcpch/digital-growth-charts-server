# Clinical Advice regarding Centile results

# DEPRECATED
THIS HAS BEEN INCLUDED IN THE DOCS BUT IS NOLONGER ACTIVELY MAINTAINED AND IS LEFT FOR LEGACY REASONS. THE PROJECT BOARD DECIDED THAT SUPPLYING ADVICE ON INDIVIDUAL GROWTH POINTS WAS UNHELPFUL AND ASKED THAT THIS FUNCTION BE DEPRECATED. IT IS ANTICIPATED THAT ONCE THE API IS ABLE TO RECEIVE AN ARRAY OF DATAPOINTS, THEN INDIVIDUALISED ADVICE CAN BE CONSIDERED BUT THERE IS LARGE PIECE OF WORK STILL TO BE DONE TO VALIDATE IT.

## Background
As part of commissioning for the RCPCH charts, a stipulation was made that the API not only provide accurate and reliable SDS and centiles for measurements of children, but some contextual advice be also reported, tailored to the user. This is contraversial, as interpretation of growth data can only be made understanding a child's context and their growth history. Advice therefore is reported as follows, as MVP (minimum viable product) currently does not consider multiple data points at the current time, though plans are in place in future for this to be possible.

#### 0.4th Centile
##### ___Height/Length___

###### _Parent/Carer of child aged < 2y:_ 
 ```
"Your child has a lower or the same length as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child has a lower or the same height as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

######  _Clinician_
```
"On or below the 0.4th centile for height. Medical review advised."
```
##### ___Weight___

###### _Parent/Carer_
```
"Your child has a lower or the same weight as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

######  _Clinician_
```
"On or below the 0.4th centile for weight. Medical review advised."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is below or the same weight as only 4 in every 1000 children. It is advisable to see your doctor."
```

######  _Clinician_
```
"On or below the 0.4th centile. Medical review advised."
```
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child 's head size is larger than or the same as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
```

######  _Clinician_
```
"On or below the 0.4th centile for head circumference. Medical review advised."
```
***
#### 2nd Centile
##### ___Height/Length___

###### _Parent/Care_of child aged < 2y:_
```
"Your child is in the lowest 2 percent for length, sex and age. Consider seeing your doctor."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child is in the lowest 2 percent for height, sex and age. Consider seeing your doctor."
```

######  _Clinician_
```
"On or below the 2nd centile. Consider reviewing trend."
```
##### __Weight__

###### _Parent/Carer_
```
"Your child is in the lowest 2 percent for weight compared with other children the same age and sex. Consider seeing your doctor."
```

######  _Clinician_
```
"On or below the 2nd centile. Consider reviewing trend."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is is in the lowest 2 percent of the population for their weight. Consider seeing your doctor."
```

######  _Clinician_
```
"On or below the 2nd centile. Consider reviewing trend."
```     
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child's head size is in the lowest 2 percent as other children the same sex and age. Consider seeing your doctor."
```

######  _Clinician_
```
"On or below the 2nd centile for head circumference. Consider reviewing trend."
```
***
#### 9th Centile
##### ___Height/Length___
###### __Parent/Carer_of child aged < 2y:_
```
"Your child is in the lowest 9 percent of the population for length, sex and age."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child is in the lowest 9 percent of the population for height, sex and age."
```

######  _Clinician_
```
"On or below the 9th centile. Consider reviewing trend."
```
##### ___Weight___

###### _Parent/Carer_
```
"Your child is in the lowest 9 percent of the population for weight compared with other children the same age and sex."
```

######  _Clinician_
```
"On or below the 9th centile. Consider reviewing trend."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the lowest 9 percent of the population for weight."
```

######  _Clinician_
```
"On or below the 9th centile. Consider reviewing trend."
```
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child's head size is in the lowest 9 percent of the population for children the same sex and age."
```

######  _Clinician_
```
"On or below the 9th centile for head circumference. Consider reviewing trend."
```
***
#### 25th Centile
##### ___Height/Length___

###### _Parent/Care_of child aged < 2y:_
```
"Your child is in the lowest 1/4 of the population for length, sex and age."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child is in the lowest 1/4 of the population for height, sex and age."
```

######  _Clinician_
```
"On or below the 25th centile. Consider reviewing trend."
```
##### ___Weight___

###### _Parent/Carer_

```
"Your child is in the lowest 1/4 of the population for weight, compared with other children the same age and sex."
```

######  _Clinician_
```
"On or below the 25th centile. Consider reviewing trend."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the lowest 1/4 of the population for their weight."
```

######  _Clinician_
```
"On or below the 25th centile. Consider reviewing trend."
```
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child's head size is in the lowest 1/4 of the population compared with other children the same sex and age."
```

######  _Clinician_
```
"On or below the 25th centile for head circumference. Consider reviewing trend."
```
***
#### 50th Centile
##### ___Height/Length___

###### _Parent/Care_of child aged < 2y:_
```
"Your child is on or just below the average length of the population for sex and age."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child is on or just below the average height of the population for sex and age."
```

######  _Clinician_
```
"On or below the 50th centile."
```
##### ___Weight___

###### _Parent/Carer_
```
"Your child is on or just below the average weight of the population, compared with other children the same age and sex."
```

######  _Clinician_
```
"On or below the 50th centile."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is on or just below the average weight for the population ."
```

######  _Clinician_
```
"On or below the 50th centile."
```
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child's head circumference is on or just below the average for the population for sex and age."
```

######  _Clinician_
```
"On or below the 50th centile for head circumference."
```
***
#### 75th Centile
##### ___Height/Length___

###### _Parent/Care_of child aged < 2y:_
```
"Your child has the same or a shorter length than 75 percent of children the same age and sex."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child has the same or a shorter height than 75 percent of children the same age and sex."
```

######  _Clinician_
```
"On or below the 75th centile. Consider reviewing trend."
```
##### ___Weight___

###### _Parent/Carer_
```
"Your child is below or the same as 75 percent of children the same age and sex. This does not take account of their height."
```

######  _Clinician_
```
"On or below the 75th centile. Consider reviewing trend."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is below or the same as 75 percent of children for their weight."
```

######  _Clinician_
```
"On or below the 75th centile. Consider reviewing trend."
```

##### _Head Circumference_

###### _Parent/Carer_
```
"Your child's head circumference is in the top 25 percent of children the same age and sex."
```

######  _Clinician_
```
"On or below the 75th centile for head circumference. Consider reviewing trend."
```
***
#### 91st Centile
##### ___Height/Length___

###### _Parent/Care_of child aged < 2y:_
```
"Your child is in the top 9 percent of children the same age and sex for their length."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child is in the top 9 percent of children the same age and sex for their height."
```

######  _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
##### ___Weight___

###### _Parent/Carer_
```
"Your child is in the top 9 percent of children the same age and sex for their weight. This does not take account of their height."
```

######  _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the top 9 percent of children for their weight."
```

######  _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child's head circumference is in the top 9 percent of children the same age and sex."
```

######  _Clinician_
```
"On or below the 91st centile for head circumference. Consider reviewing trend."
```
***
#### 98th Centile
##### ___Height/Length___

###### _Parent/Care_of child aged < 2y:_
```
"Your child is in the top 2 percent of children the same age and sex for their length."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child is in the top 2 percent of children the same age and sex for their height."
```

######  _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
##### ___Weight___

###### _Parent/Carer_
```
"Your child is in the top 2 percent of children the same age and sex for their weight. This does not take account of their height. Consider seeking medical review ."
```

######  _Clinician_
```
"On or below the 91st centile. Consider reviewing trend."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child is in the top 2 percent of children for their weight. Consider seeing your doctor."
```

######  _Clinician_
```
"On or below the 98th centile. Meets definition for being overweight. Consider reviewing trend."
```
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child's head circumference is in the top 2 percent of children the same age and sex. Consider seeing your doctor."
```

######  _Clinician_
```
"On or below the 91st centile for head circumference. Consider reviewing trend."
```
***
#### 99.6th Centile
##### ___Height/Length___

###### _Parent/Care_of child aged < 2y:_
```
"Your child is longer than only 4 children in every 1000 the same age and sex. Consider seeking medical review."
```

###### _Parent/Carer of child aged >= 2y_
```
"Your child is taller than only 4 children in every 1000 the same age and sex. Consider seeking medical review."
```

######  _Clinician_
```
"On or below the 99.6th centile. Consider medical review."
```
##### ___Weight___

###### _Parent/Carer_
```
"Your child is heavier than only 4 children in every 1000 the same age and sex. This does not take account of their height. Medical review is advised."
```

######  _Clinician_
```
"On or below the 99.6th centile. Consider medical review."
```
##### ___BMI___

###### _Parent/Carer_
```
"Compared with other children the same height, age and sex, your child 's  weight is lower than only 4 children in every 1000 childre. Medical review is advised."
```

######  _Clinician_
```
"On or below the 99.6th centile. Above obesity threshold. Consider medical review."
```
##### ___Head Circumference___

###### _Parent/Carer_
```
"Your child's head circumference is larger than only 4 children in every 1000 children the same age and sex. Medical review is advised."
```

######  _Clinician_
```
"On or below the 99.6th centile for head circumference. Medical review is advised."
```
###
#### Errors
If requests are made for calculations which fall outside the thresholds of the reference data, responses are as follows:
##### ___Height/Length___
###### _Parent/Carer_
```
"Height centiles cannot be calculate below 25 weeks gestation."
```

######  _Clinician_
```
"Length SDS and Centiles cannot be calculated below 25 weeks as there is no reference data below this threshold."
```
##### ___BMI___
###### _Parent/Carer_
```
"BMI centiles cannot be calculated below 2 weeks of age or before your baby has reached term."
```

######  _Clinician_
```
"BMI SDS and Centiles cannot be calculated before 42 weeks as there is no reference data below this threshold."
```
##### ___Head Circumference___
###### _Parent/Carer_
```
"Head circumference centiles cannot be calculated above 17 years in girls."
or 
"Head circumference centiles cannot be calculated above 18 years in boys."
```

######  _Clinician_
```
"Head circumference SDS and Centiles cannot be calculated above 17 y as there is no reference data beyond this threshold in girls."
or
"Head circumference SDS and Centiles cannot be calculated above 18 y as there is no reference data below this threshold in boys."
```