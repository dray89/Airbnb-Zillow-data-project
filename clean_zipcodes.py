# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:01:38 2021

@author: rayde
"""

import pandas as pd
import numpy as np
import random

class Zipcodes:
    def __init__(self, airbnb_df):
        self.airbnb_df = airbnb_df
    
    def input_random_zipcode(self, neighbourhood_column='neighbourhood_cleansed', zipcode_column='zipcode'):
        #Primary function that gets the zipcodes and inputs a random value into the zipcode column where zipcode is null
        airbnb_df = self.airbnb_df
        airbnb_df[zipcode_column] = airbnb_df[zipcode_column].replace('nan', np.nan)
        for neighbourhood, zipcode_list in self.__get_zipcodes(airbnb_df, neighbourhood_column, zipcode_column).items():
            try:
                airbnb_df.loc[airbnb_df[neighbourhood_column]==neighbourhood, zipcode_column] = airbnb_df[airbnb_df[neighbourhood_column]==neighbourhood][zipcode_column].map(lambda x: x if not np.nan else self.__choose_random_zipcode(zipcode_list))
            except:
                raise
        return airbnb_df
    
    def __get_zipcodes(self, airbnb_df, neighbourhood_column='neighbourhood_cleansed', zipcode_column='zipcode', null_value = None):
        #Takes the list of neighbourhoods with null values in the zipcode column and matches them to a list of 
        # zipcodes in those neighbourhoods based on their presence in the data set.
        zipcode_mapping = {}
        for neighbourhood in self.__get_affected_neighbourhoods(airbnb_df, neighbourhood_column, zipcode_column):
            try:
                zipcode_series = airbnb_df[airbnb_df[neighbourhood_column]==neighbourhood][zipcode_column]
                zipcodes = list(zipcode_series.unique())
                zipcodes.remove(null_value)
                zipcode_mapping[neighbourhood]=zipcodes
            except:
                raise
        return zipcode_mapping
    
    def __choose_random_zipcode(self, zipcode_list):
        #Impute missing zipcode via random choice from list of neighbourhoods and zipcodes within those neighbourhoods
        try:
            return random.choice(zipcode_list)
        except:
            raise
    
    def __get_affected_neighbourhoods(self, airbnb_df, neighbourhood_column='neighbourhood_cleansed', zipcode_column='zipcode'):
        #Get neighbourhoods containing null values in the zipcode column
        return airbnb_df[pd.isnull(airbnb_df[zipcode_column])][neighbourhood_column].unique()