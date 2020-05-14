import pandas as pd 
from os import path
import rcpchgrowth.rcpchgrowth as calculations
from datetime import date


def import_excel_sheet(file_path: str):
    #TODO test excel sheet in appropriate format to receive data
    data_frame = pd.read_excel(file_path, dtype={'decimal_age': float, 'birth_date': date, 'observation_date': date, 'estimated_date_delivery': date, 'measurement_type': str, 'measurement_value': float, 'sex': str})
    # data_frame = data_frame.dropna()
    data_frame['sds']=data_frame.apply(lambda row: calculations.sds(row['decimal_age'], row['measurement_type'], row['measurement_value'], row['sex']), axis=1)
    data_frame['centile']=data_frame.apply(lambda row: calculations.centile(row['sds']), axis=1)
    return data_frame.to_html(classes="ui very basic small collapsing celled table")