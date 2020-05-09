import math
import data_tables
import statistics
import scipy.stats as stats
import numpy as np

"""
calculate interpolated LMS for growth parameters
"""

#exposed functions

"""
PARAMETERS
weight
height
BMI
OFC
"""

def bmiFromHeightandWeight( height: float,  weight: float) -> float:
    bmi = weight/math.pow(height/100, 2)
    return bmi

def weightForBMI( height: float,  bmi: float) -> float:
    returnWeight = 0.0
    returnWeight = bmi*math.pow(height/100, 2)
    return returnWeight

def percentageMedianBMI(actualBMI: float,  decimalAge: float, isMale: bool):
    percentMedianBMI=0.0
    mArray = getMeasurementParameter("BMI", isMale, "M")
    m = 0.0
    ageMatched = thereIsADecimalAgeMatch(decimalAge)
    if ageMatched:
        ageIndex = indexForMatchedDecimalAge(decimalAge)
        m = getMatchedLMorSParameter(mArray,ageIndex)
    else:
        oneBelow = findAgeIndexOneBelow(decimalAge)
        if canUseCubicInterpolation(oneBelow):
            m = cubicInterpolation(actualBMI, decimalAge, oneBelow, mArray, data_tables.uk_who.decimalAges)
        else:
            m = linearInterpolation(actualBMI, decimalAge, oneBelow, mArray, data_tables.uk_who.decimalAges)
    percentMedianBMI = (actualBMI/m)*100
    return percentMedianBMI

def measurementFromSDS(measurement: str,  requestedMeasureSDS: float,  actualMeasurement: float,  isMale: float,  decimalAge: float) -> float:

    lms = getLMS(measurement, isMale, actualMeasurement, decimalAge, data_tables.uk_who.decimalAges)

    measurementValue = 0.0

    l = lms[0]
    m = lms[1]
    s = lms[2]

    #note 9th centile is -1.341

    if l != 0.0:
        measurementValue = math.pow((1+l*s*requestedMeasureSDS),1/l)*m
    else:
        measurementValue = math.exp(s*requestedMeasureSDS)*m
    return measurementValue

def SDS(measurement: str,  decimalAge: float,  actualMeasurement: float, isMale: bool):
    z = 0.0

    lArray = getMeasurementParameter(measurement, isMale, "L")
    mArray = getMeasurementParameter(measurement, isMale, "M")
    sArray = getMeasurementParameter(measurement, isMale, "S")
    l, m, s = 0.0, 0.0, 0.0

    ageMatched = thereIsADecimalAgeMatch(decimalAge)

    if ageMatched:
        ageIndex = indexForMatchedDecimalAge(decimalAge)
        l = getMatchedLMorSParameter(lArray,ageIndex)
        m = getMatchedLMorSParameter(mArray,ageIndex)
        s = getMatchedLMorSParameter(sArray,ageIndex)
    else:
        oneBelow = findAgeIndexOneBelow(decimalAge)
        if canUseCubicInterpolation(oneBelow):
            l = cubicInterpolation(actualMeasurement, decimalAge, oneBelow, lArray, data_tables.uk_who.decimalAges)
            m = cubicInterpolation(actualMeasurement, decimalAge, oneBelow, mArray, data_tables.uk_who.decimalAges)
            s = cubicInterpolation(actualMeasurement, decimalAge, oneBelow, sArray, data_tables.uk_who.decimalAges)
        else:
            l = linearInterpolation(actualMeasurement, decimalAge, oneBelow, lArray, data_tables.uk_who.decimalAges)
            m = linearInterpolation(actualMeasurement, decimalAge, oneBelow, mArray, data_tables.uk_who.decimalAges)
            s = linearInterpolation(actualMeasurement, decimalAge, oneBelow, sArray, data_tables.uk_who.decimalAges)

    z = calculateSDS(l, m, s, actualMeasurement)

    return z

def centileFromSDS(z: float)->float:
    p = stats.norm.sf(abs(z))
    centile = statistics.NormalDist().cdf(p)
    return centile

#helper functions
"""these are all the private methods to remain unexposed"""

def getMeasurementParameter(measurement: str, male: bool, parameter: str):
    arrayToReturn = [0]
    if measurement=="weight":
        if male:
            if parameter=="L":
               arrayToReturn = data_tables.uk_who.boysWeightL
            if parameter=="M":
                arrayToReturn = data_tables.uk_who.boysWeightM
            if parameter=="S":
                arrayToReturn = data_tables.uk_who.boysWeightS
        else:
            if parameter=="L":
                arrayToReturn = data_tables.uk_who.girlsWeightL
            if parameter=="M":
                arrayToReturn = data_tables.uk_who.girlsWeightM
            if parameter=="S":
                arrayToReturn = data_tables.uk_who.girlsWeightS
    elif measurement=="height":
        if male:
            if parameter=="L":
               arrayToReturn = data_tables.uk_who.boysHeightL
            if parameter=="M":
                arrayToReturn = data_tables.uk_who.boysHeightM
            if parameter=="S":
               arrayToReturn = data_tables.uk_who.boysHeightS
        else:
            if parameter=="L":
               arrayToReturn = data_tables.uk_who.girlsHeightL
            if parameter=="M":
               arrayToReturn = data_tables.uk_who.girlsHeightM
            if parameter=="S":
               arrayToReturn = data_tables.uk_who.girlsHeightS
    elif measurement=="BMI":
        if male:
            if parameter=="L":
               arrayToReturn = data_tables.uk_who.boysBMIL
            if parameter=="M":
                arrayToReturn = data_tables.uk_who.boysBMIM
            if parameter=="S":
                arrayToReturn = data_tables.uk_who.boysBMIS
        else:
            if parameter=="L":
                arrayToReturn = data_tables.uk_who.girlsBMIL
            if parameter=="M":
                arrayToReturn = data_tables.uk_who.girlsBMIM
            if parameter=="S":
                arrayToReturn = data_tables.uk_who.girlsBMIS
    elif measurement=="OFC":
        if male:
            if parameter=="L":
               arrayToReturn = data_tables.uk_who.boysOFCL
            if parameter=="M":
                arrayToReturn = data_tables.uk_who.boysOFCM
            if parameter=="S":
                arrayToReturn = data_tables.uk_who.boysOFCS
        else:
            if parameter=="L":
                arrayToReturn = data_tables.uk_who.girlsOFCL
            if parameter=="M":
                arrayToReturn = data_tables.uk_who.girlsOFCM
            if parameter=="S":
                arrayToReturn = data_tables.uk_who.girlsOFCS
    return arrayToReturn

def getMatchedLMorSParameter( measurementArray: list, mDecimalAgeIndex: list) -> float:
    l = 0.0
    l = measurementArray[mDecimalAgeIndex]
    return l

def getInterpolatedLMorSParameter(measuredValue: float,  decimalAge: float, measurement: str, lowerAgeIndex: int,  canCubicInterpolate: bool, decimalAgeArrayToUse: list) -> float:
    interpolatedParameter = 0.0
    if canCubicInterpolate:
        interpolatedParameter = cubicInterpolation(measuredValue, decimalAge, lowerAgeIndex, measurement, decimalAgeArrayToUse)
    else:
        interpolatedParameter = linearInterpolation(measuredValue, decimalAge, lowerAgeIndex, measurement, decimalAgeArrayToUse)

    return interpolatedParameter


def indexForMatchedDecimalAge( mDecimalAge: float) -> int:
    mIndex = 0
    if mDecimalAge==0.0:
        mIndex = 17
    elif mDecimalAge==2.0:
        mIndex = 56
    elif mDecimalAge==4.0:
        mIndex = 81
    elif mDecimalAge==20:
        mIndex = 273
    else:
        mIndex = data_tables.uk_who.decimalAges.index(mDecimalAge)
    return mIndex



def thereIsADecimalAgeMatch(mDecimalAge: float) -> bool:
    matchFound = False
    if mDecimalAge in data_tables.uk_who.decimalAges: #note that a match may occur more than once if age = 2 or 4 yrs
        matchFound = True
    return matchFound

def findAgeIndexOneBelow(decimalAge: float) -> int:
    index = 0
    i = 0
    while i < len(data_tables.uk_who.decimalAges):
        lookUpAge = data_tables.uk_who.decimalAges[i]
        if lookUpAge < decimalAge:
           index = i
        i += 1
    return index


def canUseCubicInterpolation(ageIndexBelow: int) -> bool:
    canUseCubicInterpolation = True
    if ageIndexBelow == 17 or ageIndexBelow == 54 or ageIndexBelow == 55 or ageIndexBelow == 56 or ageIndexBelow == 80 or ageIndexBelow == 81 or ageIndexBelow == 272:
        #this is age 0 (17) or lower age just under 2 (54) or lower age 2 (55) or upper age 2 (56) or lower 4(80) or upper 4 (81) or 20 (273)
        canUseCubicInterpolation = False
        return canUseCubicInterpolation
    canUseCubicInterpolation = True
    return canUseCubicInterpolation

def linearInterpolation( measuredValue: float,  decimalAge: float, ageIndexBelow: int, measurementArrayToUse: list, decimalAgeArrayToUse: list) -> float:
    linearInterpolatedValue = 0.0
    valueBelow = measurementArrayToUse[ageIndexBelow]
    valueAbove = measurementArrayToUse[ageIndexBelow+1]
    ageBelow = decimalAgeArrayToUse[ageIndexBelow]
    ageAbove = decimalAgeArrayToUse[ageIndexBelow+1]
    linearInterpolatedValue = valueBelow + (((decimalAge - ageBelow)*valueAbove-valueBelow))/(ageAbove-ageBelow)
    return linearInterpolatedValue

def cubicInterpolation( measuredValue: float,  decimalAge: float, ageIndexBelow: int, measurementArrayToUse: list, decimalAgeArrayToUse: list) -> float:
    cubicInterpolatedValue = 0.0

    # t = 0.0 #actual age
    tt0 = 0.0
    tt1 = 0.0
    tt2 = 0.0
    tt3 = 0.0

    t01 = 0.0
    t02 = 0.0
    t03 = 0.0
    t12 = 0.0
    t13 = 0.0
    t23 = 0.0

    ageTwoBelow = decimalAgeArrayToUse[ageIndexBelow-1]
    ageOneBelow = decimalAgeArrayToUse[ageIndexBelow]
    ageOneAbove = decimalAgeArrayToUse[ageIndexBelow+1]
    ageTwoAbove = decimalAgeArrayToUse[ageIndexBelow+2]

    measurementTwoBelow = measurementArrayToUse[ageIndexBelow-1]
    measurementOneBelow = measurementArrayToUse[ageIndexBelow]
    measurementOneAbove = measurementArrayToUse[ageIndexBelow+1]
    measurementTwoAbove = measurementArrayToUse[ageIndexBelow+2]

    # t = decimalAge


    tt0 = decimalAge - ageTwoBelow
    tt1 = decimalAge - ageOneBelow
    tt2 = decimalAge - ageOneAbove
    tt3 = decimalAge - ageTwoAbove

    t01 = ageTwoBelow - ageOneBelow
    t02 = ageTwoBelow - ageOneAbove
    t03 = ageTwoBelow - ageTwoAbove

    t12 = ageOneBelow - ageOneAbove
    t13 = ageOneBelow - ageTwoAbove
    t23 = ageOneAbove - ageTwoAbove

    cubicInterpolatedValue = measurementTwoBelow * tt1 * tt2 * tt3 /t01 / t02 / t03 - measurementOneBelow * tt0 * tt2 * tt3 / t01 / t12 /t13 + measurementOneAbove * tt0 * tt1 * tt3 / t02/ t12 / t23 - measurementTwoAbove * tt0 * tt1 * tt2 / t03 / t13 / t23

    return cubicInterpolatedValue

def calculateSDS( myL: float,  myM: float,  myS: float,  myMeasurement: float):
    SDS = 0.0
    if myL != 0.0:
        SDS = (((math.pow((myMeasurement / myM), myL))-1)/(myL*myS))
    else:
        SDS = (math.log(myMeasurement / myM)/myS)
    return SDS

def getLMS( measurement: str,  isMale: bool,  actualMeasurement: float,  decimalAge: float, decimalAgeArrayToUse: list) -> list:

    lArray = getMeasurementParameter(measurement, isMale, "L")
    mArray = getMeasurementParameter(measurement, isMale, "M")
    sArray = getMeasurementParameter(measurement, isMale, "S")

    l, m, s = 0.0, 0.0, 0.0

    ageMatched = thereIsADecimalAgeMatch(decimalAge)

    if ageMatched:
        ageIndex = indexForMatchedDecimalAge(decimalAge)
        l = getMatchedLMorSParameter(lArray,ageIndex)
        m = getMatchedLMorSParameter(mArray,ageIndex)
        s = getMatchedLMorSParameter(sArray,ageIndex)
    else:
        oneBelow = findAgeIndexOneBelow(decimalAge)
        if canUseCubicInterpolation(oneBelow):
            l = cubicInterpolation(actualMeasurement, decimalAge, oneBelow, lArray, decimalAgeArrayToUse)
            m = cubicInterpolation(actualMeasurement, decimalAge, oneBelow, mArray, decimalAgeArrayToUse)
            s = cubicInterpolation(actualMeasurement, decimalAge, oneBelow, sArray, decimalAgeArrayToUse)
        else:
            l = linearInterpolation(actualMeasurement, decimalAge, oneBelow, lArray, decimalAgeArrayToUse)
            m = linearInterpolation(actualMeasurement, decimalAge, oneBelow, mArray, decimalAgeArrayToUse)
            s = linearInterpolation(actualMeasurement, decimalAge, oneBelow, sArray, decimalAgeArrayToUse)

    lms = [l,m,s]

    return lms

def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return array[idx-1]
    else:
        return array[idx]
