from datetime import date, datetime
from datetime import timedelta
from dateutil import relativedelta
import math

"""
3 functions to calculate ages
 - chronological_decimal_age: returns a decimal age from 2 dates (takes birth_date and observation_date)
 - corrected_decimal_age: returns a corrected decimal age accounting for prematurity (takes birth_date: date, observation_date: date, gestation_weeks: int, gestation_supplementary_days: int, pregnancy_length_day [optional])
 - chronological_calendar_age: returns a calendar age as a string (takes birth_date or estimated_date_delivery and observation_date)
 - estimated_date_delivery: returns estimated date of delivery in a known premature infant (takes birth_date, gestation_weeks, gestation_supplementary_days, pregnancy_length_days[optional])
"""

#constants
TERM_PREGNANCY_LENGTH_DAYS = 40 * 7
TERM_LOWER_THRESHOLD_LENGTH_DAYS = 37 * 7
EXTREME_PREMATURITY_THRESHOLD_LENGTH_DAYS = 32 * 7

def chronological_decimal_age(birth_date: date, observation_date: date) -> float:

    """
    Calculates a decimal age from two dates supplied as raw dates without times.
    Returns value floating point
    :param birth_date: date of birth
    :param observation_date: date observation made
    """

    days_between = observation_date - birth_date
    chronological_decimal_age = days_between.days / 365.25
    return chronological_decimal_age
    
def corrected_decimal_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_supplementary_days: int, pregnancy_length_days = 0)->float:
    """
    Corrects for gestational age. 
    Corrects for 1 year, if gestation at birth >= 32 weeks and < 37 weeks
    Corrects for 2 years, if gestation at birth <32 weeks
    Otherwise returns decimal age without correction
    :param birth_date: date of birth
    :param observation_date: date observation made
    :param gestation_weeks: weeks of gestation up to 40
    :param gestation_supplementary_days: days in excess of weeks
    """

    correction_days = 0

    if pregnancy_length_days == 0:
        pregnancy_length_days = (gestation_weeks * 7) + gestation_supplementary_days
    
    try:
        uncorrected_age = chronological_decimal_age(birth_date, observation_date)
    except ValueError as err:
        return err

    prematurity = TERM_PREGNANCY_LENGTH_DAYS - pregnancy_length_days

    if pregnancy_length_days >= TERM_LOWER_THRESHOLD_LENGTH_DAYS:
        #term baby
        return uncorrected_age

    elif pregnancy_length_days < EXTREME_PREMATURITY_THRESHOLD_LENGTH_DAYS and uncorrected_age <= 2:
        #correct age for 2 years
        correction_days = prematurity
        edd = birth_date + timedelta(days=correction_days)
        return chronological_decimal_age(edd, observation_date)

    elif (pregnancy_length_days >= EXTREME_PREMATURITY_THRESHOLD_LENGTH_DAYS) and (pregnancy_length_days < TERM_LOWER_THRESHOLD_LENGTH_DAYS) and uncorrected_age <=1:
        #correct age for 1 year
        correction_days = prematurity
        edd = birth_date + timedelta(days=correction_days)
        return chronological_decimal_age(edd, observation_date);
    
    else:
        return uncorrected_age

def chronological_calendar_age(birth_date: date, observation_date: date) -> str:
    """
    returns age in years, months, weeks and days: to return a corrected calendar age use passes EDD instead of birth date
    """
    difference = relativedelta.relativedelta(observation_date, birth_date)
    years = difference.years
    months = difference.months
    weeks = difference.weeks
    days = difference.days
    # hours = difference.hours
    # minutes = difference.minutes

    date_string = []

    if years == 1:
        date_string.append(str(years) + " year")
    if years > 1:
        date_string.append(str(years) + " years")
    if months > 1:
        date_string.append(str(months) + " months")
    if months == 1:
        date_string.append(str(months) + " month")
    if days == 1:
        date_string.append(str(days) + " day")
    if days > 1:
        if weeks > 0:
            remainingdays = days - (weeks*7)
            if weeks == 1:
                date_string.append(str(weeks) + " week")
            elif weeks > 1:
                date_string.append(str(weeks) + " weeks")
            if remainingdays == 1:
                date_string.append(str(remainingdays) + " day")
            if remainingdays > 1:
                date_string.append(str(remainingdays) + " days")
    if len(date_string) > 1:
        return (', '.join(date_string[:-1])) + ' and ' + date_string[-1]
    elif len(date_string) == 1:
        return date_string[0]
    elif birth_date == observation_date:
        return 'Happy Birthday'
    else:
        return ''

def estimated_date_delivery(birth_date: date, gestation_weeks: int, gestation_supplementary_days: int, pregnancy_length_days = 0) -> date:
    """
    Returns estimated date of delivery from gestational age and birthdate
    Will still calculate an estimated date of delivery if already term (>37 weeks)
    """
    if pregnancy_length_days == 0:
        pregnancy_length_days = (gestation_weeks * 7) + gestation_supplementary_days
    
    prematurity = TERM_PREGNANCY_LENGTH_DAYS - pregnancy_length_days

    edd = birth_date + timedelta(days=prematurity)
    return edd

def corrected_gestational_age(birth_date: date, observation_date: date, gestation_weeks: int, gestation_supplementary_days: int)->str:
    """
    Returns a corrected gestational age
    """
    edd = estimated_date_delivery(birth_date, gestation_weeks, gestation_supplementary_days)
    forty_two_weeks_gestation_date = edd + timedelta(days=14)

    if observation_date >= forty_two_weeks_gestation_date:
        #beyond 2 weeks post term - chronological age measured in days / weeks / months years
        #no correction
        return ''
    
    pregnancy_length_days = (gestation_weeks * 7) + gestation_supplementary_days
    # time_alive = relativedelta.relativedelta(observation_date, birth_date)
    time_alive = observation_date - birth_date
    days_of_life = time_alive.days
    days_since_conception = days_of_life + pregnancy_length_days

    corrected_weeks = math.floor(days_since_conception / 7)
    corrected_supplementary_days = days_since_conception - (corrected_weeks * 7)

    return f"{corrected_weeks}+{corrected_supplementary_days} weeks"

# def string_to_date(convert_string):
    # return datetime.strptime(convert_string, '%d/%m/%Y')


# def tim_date_tests():
    # """
        # validation tests using dummy data
    # """
    # child_dobs = ["03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","09/07/2004","09/07/2004","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","03/12/2010","09/07/2004","09/07/2004","09/07/2004","09/07/2004","09/07/2004","09/07/2004","09/07/2004","09/07/2004","09/07/2004","09/07/2004","09/07/2004","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","01/04/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009","03/01/2009"]
    # child_measurement_dates = ["03/12/2010","20/12/2010","08/03/2012","22/06/2012","27/11/2014","11/10/2004","11/10/2004","01/04/2009","02/07/2009","21/07/2009","21/07/2009","28/07/2009","03/07/2011","25/01/2012","18/03/2013","05/07/2013","12/03/2014","05/06/2014","24/09/2014","21/05/2015","08/03/2012","12/03/2014","05/06/2014","24/09/2014","21/05/2015","09/07/2004","05/01/2005","30/05/2005","06/09/2005","12/12/2005","09/02/2006","20/10/2006","01/02/2007","05/01/2005","30/05/2005","06/09/2005","28/07/2009","18/08/2009","01/09/2009","04/12/2009","19/02/2010","23/02/2010","06/05/2010","16/09/2010","14/10/2010","16/12/2010","03/03/2011","18/08/2009","04/12/2009","19/02/2010","06/05/2010","16/09/2010","14/10/2010","16/12/2010","03/03/2011","03/05/2010","29/12/2010","13/09/2011","03/10/2011","02/04/2012","06/06/2012","04/03/2013","20/11/2013","18/12/2013","15/01/2014","15/04/2014","19/09/2014","11/12/2014","19/02/2015","03/06/2015","03/05/2010","13/09/2011","04/03/2013","20/11/2013","19/09/2014","11/12/2014","19/02/2015"]
    # child_gestation_months = [27,27,27,27,27,35,35,40,40,40,40,40,27,27,27,27,27,27,27,27,27,27,27,27,27,35,35,35,35,35,35,35,35,35,35,35,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40]
    # final_ages_list=[]
    # dob_ages_as_list = []
    # measurement_ages_as_dates = []
    # for m in range(len(child_dobs)):
        # age_as_date = string_to_date(child_dobs[m])
        # dob_ages_as_list.append(age_as_date)
    # for n in range(len(child_measurement_dates)):
        # measurement_age_as_date = string_to_date(child_measurement_dates[n])
        # measurement_ages_as_dates.append(measurement_age_as_date)
    # 
    # for i in range(len(child_dobs)):
        # child_corrected_age = corrected_decimal_age(dob_ages_as_list[i],measurement_ages_as_dates[i],child_gestation_months[i],0)
        # child_uncorrected_age = chronological_decimal_age(dob_ages_as_list[i], measurement_ages_as_dates[i])
        # final_ages_list.append(child_uncorrected_age)
    # 
    # return final_ages_list
    
