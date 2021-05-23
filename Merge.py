# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 16:26:06 2021

@author: rayde
"""

import pandas as pd

class MergeZillowAirBnb:
    
    def merge_datasets(operating_income, zillow, zillow_date_col = 'Date', date='2017-06', zillow_cols = ['RegionName', 'Price'], operating_income_zipcode_col = 'zipcode', zillow_zipcode_col = 'RegionName' , how='outer'):
        cap_rates = operating_income.merge(zillow[(zillow[zillow_date_col] == date)][zillow_cols], left_on = operating_income_zipcode_col, right_on = zillow_zipcode_col, how = how)
        return cap_rates
    
    def identify_imputed_values(cap_rates, cols):
        for col in cols:
            cap_rates[f'imputed_{col}'] = pd.isnull(cap_rates[col])
        return cap_rates
    
    def impute_median(cap_rates, col='Price'):
        cap_rates[col].fillna((cap_rates[col].median()), inplace=True)
        return cap_rates
    
    def fill_missing_zipcodes(cap_rates, zipcode_col_airbnb= 'zipcode', zipcode_col_zillow= 'RegionName'):
        cap_rates[zipcode_col_airbnb].fillna(cap_rates[zipcode_col_zillow], inplace=True)
        cap_rates.drop(zipcode_col_zillow, axis=1, inplace=True)
        return cap_rates

