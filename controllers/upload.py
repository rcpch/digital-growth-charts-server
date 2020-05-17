import pandas as pd 
from os import path, remove
import rcpchgrowth.rcpchgrowth as calculations
from datetime import date


def import_excel_sheet(file_path: str, can_delete: bool):
    #TODO test excel sheet in appropriate format to receive data
    
    data_frame = pd.read_excel(file_path, dtype={'decimal_age': float, 'measurement_type': str, 'measurement_value': float, 'sex': str}, parse_dates=['birth_date', 'observation_date', 'estimated_date_delivery'])
    
    ## delete the file if not dummy_data.xlsx
    if can_delete:
        remove(file_path)

    ## check all columns present

    ## check columns data-type correct
    data_frame['gestation_days'] = data_frame['gestation_days'].fillna(0).astype(int) 
    data_frame['gestation_weeks'] = data_frame['gestation_weeks'].fillna(0).astype(int)
    data_frame['decimal_age'] = data_frame['decimal_age'].fillna(0).astype(float)
    data_frame['birth_date']=data_frame['birth_date'].astype('datetime64[ns]')
    data_frame['observation_date']=data_frame['observation_date'].astype('datetime64[ns]')
    data_frame['estimated_date_delivery']=data_frame['observation_date'].astype('datetime64[ns]')
    data_frame['measurement_type']=data_frame['measurement_type'].astype(str)
    data_frame['sex']=data_frame['sex'].astype(str)
    data_frame['decimal_age']=data_frame.apply(lambda row: decimal_age_if_decimal_age_is_empty(row['decimal_age'], row['birth_date'], row['observation_date'], row['gestation_weeks'], row['gestation_days']), axis=1)
    data_frame['sds']=data_frame.apply(lambda row: sds_if_parameters(row['decimal_age'], row['measurement_type'], row['measurement_value'], row['sex']), axis=1)
    data_frame['centile']=data_frame.apply(lambda row: calculations.centile(row['sds']), axis=1)
    return data_frame.to_html(classes="ui very basic small collapsing celled table")

def decimal_age_if_decimal_age_is_empty(decimal_age, dob, obs_date, gestation_weeks, gestation_days):
    if decimal_age:
        return decimal_age
    else:
        return calculations.corrected_decimal_age(dob, obs_date, gestation_weeks, gestation_days)

def sds_if_parameters(decimal_age, measurement_type, measurement_value, sex):
    if decimal_age and measurement_type and measurement_value and sex:
        return calculations.sds(decimal_age, measurement_type, measurement_value, sex)
    else:
        return 0