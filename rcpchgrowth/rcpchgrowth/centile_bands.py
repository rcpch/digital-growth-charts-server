# Recommendations from Project board for reporting Centiles

# Lower limit	Upper limit	Centile band	Weight,  Height, Head	BMI
# 	<-6 		Probable error	Probable error
# -6.00	-2.84	Below 0.4th	Below normal range	Very thin
# -2.84	-2.50	0.4th 		Low BMI
# -2.50	-2.17	0.4th-2nd		Low BMI
# -2.17	-1.83	2nd		
# -1.83	-1.50	2nd -9th		
# -1.50	-1.16	9th		
# -1.16	-0.84	9th-25th		
# -0.84	-0.50	25th		
# -0.50	-0.17	25-50th 		
# -0.17	0.17	50th 		
# 0.17	0.50	50-75th 		
# 0.50	0.84	75th 		
# 0.84	1.16	75-91st 		
# 1.16	1.50	91st 		
# 1.50	1.83	91-98th 		Overweight
# 1.83	2.17	98th 		Overweight
# 2.17	2.50	98-99.6th 		Very overweight (obese)
# 2.50	2.84	99.6th 		Very overweight (obese)
# 2.84	6.00	Above 99.6th	Above normal range	Severely obese
# 	>6.00		Probable error	Probable error

def centile_band_for_centile(sds: float, measurement_method: str)->str:
    ## this function returns a centile band into which the sds falls
    ## params: accepts a sds: float
    ## params: accepts a measurement_method as string

    centile_band=""

    if measurement_method=="bmi":
        measurement_method="body mass index"
    if measurement_method=="ofc":
        measurement_method="head circumference"

    if sds <=-6:
        centile_band = 'This ' + measurement_method + ' measurement is well below the normal range. Please review its accuracy.'
    elif sds <=-2.84:
        centile_band = "This " + measurement_method + " measurement is below the normal range."
    elif sds <=-2.5:
        centile_band = "This " + measurement_method + " measurement is on or near the 0.4th centile."
    elif sds <=-2.17: 
        centile_band = "This " + measurement_method + " measurement is between the 0.4th and 2nd centiles."
    elif sds <=-1.83:
        centile_band = "This " + measurement_method + " measurement is on or near the 2nd centile."
    elif sds <=-1.5:
        centile_band = "This " + measurement_method + " measurement is between the 2nd and 9th centiles."
    elif sds <=-1.16:
        centile_band = "This " + measurement_method + " measurement is on or near the 9th centile."
    elif sds <=-0.84:
        centile_band = "This " + measurement_method + " measurement is between the 9th and 25th centiles."
    elif sds <=-0.5:
        centile_band = "This " + measurement_method + " measurement is on or near the 25th centile."
    elif sds <=-0.17:
        centile_band = "This " + measurement_method + " measurement is between the 25th and 50th centiles."
    elif sds <=0.17:
        centile_band = "This " + measurement_method + " measurement is on or near the 50th centile."
    elif sds <=0.5:
        centile_band = "This " + measurement_method + " measurement is between the 50th and 75th centiles."
    elif sds <=0.84:
        centile_band = "This " + measurement_method + " measurement is on or near the 75th centile."
    elif sds <=1.16:
        centile_band = "This " + measurement_method + " measurement is between the 75th and 91st centiles."
    elif sds <=1.5:
        centile_band = "This " + measurement_method + " measurement is on or near the 91st centile."
    elif sds <=1.83:
        centile_band = "This " + measurement_method + " measurement is between the 91st and 98th centiles."
    elif sds <=2.17:
        centile_band = "This " + measurement_method + " measurement is on or near the 98th centile."
    elif sds <=2.5:
        centile_band = "This " + measurement_method + " measurement is between the 98th and 99.6th centiles."
    elif sds <=2.84:
        centile_band = "This " + measurement_method + " measurement is on or near the 99.6th centile."
    elif sds <=6:
        centile_band= "This " + measurement_method + " measurement is above the normal range."
    else:
        centile_band="This " + measurement_method + " measurement is well above the normal range. Please review its accuracy."

    return centile_band
