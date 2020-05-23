import pandas as pd 
from os import path, remove
from pathlib import Path
import rcpchgrowth.rcpchgrowth as calculations
from datetime import date
import json
import urllib


def import_excel_sheet(file_path: str, can_delete: bool):
    #TODO test excel sheet in appropriate format to receive data
    
    data_frame = pd.read_excel(file_path)
    unique = True
    
    ## delete the file if not dummy_data.xlsx
    if can_delete:
        remove(file_path)

    ## check all columns present
    expected_column_names = ['birth_date', 'observation_date', 'gestation_weeks','gestation_days', 'estimated_date_delivery', 'decimal_age', 'sex', 'measurement_type', 'measurement_value']
    # essential_column_names = ['birth_date', 'sex', 'measurement_type', 'measurement_value']
    columns = data_frame.columns.ravel().tolist()
    for column in columns:
        ## flag if column_names are missing or extra
        if column not in expected_column_names: 
            raise LookupError('Please include only the headings: birth_date, observation_date, gestation_days, estimated_date_delivery, decimal_age, sex, measurement_type, measurement_value')
    if len(columns) != len(expected_column_names):
        raise LookupError('Please include ALL the headings (even if columns left blank): birth_date, observation_date, gestation_days, estimated_date_delivery, decimal_age, sex, measurement_type, measurement_value')

    ## check no missing data in essential columns
    if(pd.isnull(data_frame['birth_date']).values.any() or pd.isnull(data_frame['observation_date']).values.any() or pd.isnull(data_frame['sex']).values.any() or pd.isnull(data_frame['measurement_type']).values.any() or pd.isnull(data_frame['measurement_value']).values.any()):
        remove(file_path)
        raise ValueError('birth_date, sex, measurement_type and measurement_value are all essential data fields and cannot be blank.')

    ## check columns data-type correct
    data_frame['gestation_days'] = data_frame['gestation_days'].fillna(0).astype(int) 
    data_frame['gestation_weeks'] = data_frame['gestation_weeks'].fillna(0).astype(int)
    data_frame['decimal_age'] = data_frame['decimal_age'].fillna(0).astype(float)
    data_frame['birth_date']=data_frame['birth_date'].astype('datetime64[ns]')
    data_frame['observation_date']=data_frame['observation_date'].astype('datetime64[ns]')
    data_frame['estimated_date_delivery']= data_frame['estimated_date_delivery'].astype('datetime64[ns]')
    data_frame['measurement_type']=data_frame['measurement_type'].astype(str)
    data_frame['measurement_type']=data_frame.apply(lambda  row: row['measurement_type'].lower(), axis=1) ## ensure sex and measurement_type are lowercase
    data_frame['sex']=data_frame['sex'].astype(str)
    data_frame['sex']=data_frame.apply(lambda  row: row['sex'].lower(), axis=1) ## ensure sex and measurement_type are lowercase
    data_frame['decimal_age']=data_frame.apply(lambda row: decimal_age_if_decimal_age_is_empty(row['decimal_age'], row['birth_date'], row['observation_date'], row['gestation_weeks'], row['gestation_days']), axis=1)
    data_frame['sds']=data_frame.apply(lambda row: sds_if_parameters(row['decimal_age'], row['measurement_type'], row['measurement_value'], row['sex']), axis=1)
    data_frame['centile']=data_frame.apply(lambda row: calculations.centile(row['sds']), axis=1)
    if data_frame['birth_date'].nunique() > 1:
        print('these are not the same patient') #do not chart these values
        unique = False
    
    return {
        'data': data_frame.to_json(orient='records', date_format='epoch'),
        'unique': unique
    }



def decimal_age_if_decimal_age_is_empty(decimal_age, dob, obs_date, gestation_weeks, gestation_days):
    if decimal_age:
        return decimal_age
    else:
        corrected_decimal_age = calculations.corrected_decimal_age(dob, obs_date, gestation_weeks, gestation_days)
        
        return corrected_decimal_age

def sds_if_parameters(decimal_age, measurement_type, measurement_value, sex):
    if decimal_age and measurement_type and measurement_value and sex:
        try:
            return calculations.sds(decimal_age, measurement_type, measurement_value, sex)
        except:
            print('could not calculate this value')
            return 0
    else:
        return 0

def download_excel(json_string: str):
    json_file = json.dumps(json_string)
    out_file_2 = Path.cwd().joinpath("static").joinpath('uploaded_data').joinpath('temp').joinpath("output.xlsx")
    excel_file = pd.read_json(json_file).to_excel(out_file_2)
    return excel_file