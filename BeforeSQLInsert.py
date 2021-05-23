# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 14:45:07 2021

@author: rayde
"""
import numpy as np
import pandas as pd
import json
from SQL_functions import SQL_functions

class BeforeSQLInsert:
    def __init__(self, airbnb_df):
        '''
        

        Parameters
        ----------
        airbnb_df : Dataframe containing AirBnB data for cleaning before insert into SQL.

        Returns
        -------
        BeforeSQLInsert class object.

        '''
        self.airbnb_df = airbnb_df
    
    def clean_airbnb(self):
        '''
        

        Returns
        -------
        airbnb_df : Alters the Airbnb Data by filling NULL values and stripping leading and trailing 
                    white spaces from columns of datatype STR.

        '''
        airbnb_df = self.airbnb_df
        airbnb_df.fillna(value=np.nan, inplace=True)
        airbnb_df = airbnb_df.replace({np.nan: None})
        for each in airbnb_df:
            try:
                airbnb_df[each] = airbnb_df[each].str.strip()
            except AttributeError:
                pass
        self.airbnb_df = airbnb_df    
        return airbnb_df
    
    def clean_price(self, price_cols = None):
        '''
        

        Parameters
        ----------
        price_cols : list, optional
            DESCRIPTION. The default is ['price', 'weekly_price', 'monthly_price', 'security_deposit', 'cleaning_fee'].

        Returns
        -------
        airbnb_df : Dataframe
            Alters the price column of the Airbnb dataframe by stripping strings from the column and 
            casting it as type float.

        '''
        if price_cols == None:
            price_cols = ['price', 'weekly_price', 'monthly_price', 'security_deposit', 'cleaning_fee']
        airbnb_df = self.airbnb_df
        for each in price_cols:
            try:
                airbnb_df[each] = airbnb_df[each].str.strip('$')
                airbnb_df[each] = airbnb_df[each].str.replace(',','')
                airbnb_df[each].astype(float)
            except:
                raise
        self.airbnb_df = airbnb_df
        return airbnb_df
    
    def clean_street(self, street_col = 'street', to_replace = "\n", replace_with =  ' '):
        '''
        

        Parameters
        ----------
        street_col : DataFrame Column, optional
            DESCRIPTION. The default is 'street'.
        to_replace : TYPE, optional
            DESCRIPTION. The default is "\n".
        replace_with : TYPE, optional
            DESCRIPTION. The default is ' '.

        Returns
        -------
        airbnb_df : Dataframe
            DESCRIPTION.

        '''
        airbnb_df = self.airbnb_df
        airbnb_df[street_col] = airbnb_df[street_col].str.upper()
        airbnb_df[street_col] = airbnb_df[street_col].str.strip()
        airbnb_df[street_col] = airbnb_df[street_col].str.replace(to_replace, replace_with)
        self.airbnb_df = airbnb_df
        return airbnb_df
    
    def clean_state(self, state_col = 'state', to_replace='NEW YORK', replace_with='NY'):
        airbnb_df = self.airbnb_df
        airbnb_df['state'] = airbnb_df['state'].str.upper()
        airbnb_df['state'] = airbnb_df['state'].replace(to_replace, replace_with)
        self.airbnb_df = airbnb_df
        return airbnb_df
    
    def clean_zipcodes(self, zipcode_col='zipcode'):
        airbnb_df = self.airbnb_df
        zipcode_series = airbnb_df[zipcode_col].astype(str)
        zipcode_series = zipcode_series.str.strip()
        zipcode_series = zipcode_series.str[:5]
        airbnb_df[zipcode_col] = zipcode_series
        self.airbnb_df = airbnb_df
        return airbnb_df
    
    def create_tables(self, engine, file_name='table_cols.json', if_exists='replace', index=False):
        '''
        

        Parameters
        ----------
        engine : SQL engine from SQLAlchemy or other connection to database.
        file_name : TYPE, optional
            DESCRIPTION. filepath to location where dictionary object containing keys (table name) and 
                            values(table columns)
            The default is 'table_cols.json'.
        if_exists : TYPE, optional
            DESCRIPTION. The default is 'replace'. Would you like to replace the table if it exists or throw an error?
        index : TYPE, optional
            DESCRIPTION. The default is False. Does not import the Pandas dataframe index to SQL database.

        Returns
        -------
        None.

        '''
        with open(file_name) as table_cols:
            table_cols = json.load(table_cols)
        for table_name, col_list in table_cols.items():
            self.airbnb_df[col_list].to_sql(table_name, con=engine, if_exists=if_exists, index=index)
        print("Successfully created tables from file.")

    
if __name__ == '__main__':
    airbnb = pd.read_csv('listings.csv.gz', compression='gzip', header=0, sep=',', quotechar='"', low_memory=False)
    bsi = BeforeSQLInsert(airbnb)
    airbnb = bsi.clean_airbnb()    
    airbnb = bsi.clean_street()
    airbnb = bsi.clean_price()
    airbnb = bsi.clean_state()
    airbnb = bsi.clean_zipcodes()
    
    sql = SQL_functions()
    conn = sql.sql_connection()
    engine = sql.sql_alchemy_engine()
    bsi.create_tables(engine=engine, df=airbnb)
    
    zillow = pd.read_csv('zillow.csv')
    zillow['RegionName'] = zillow['RegionName'].astype('str')

    #From wide to long - and then if trend analysis by zipcode is necessary, can convert back to wide later
    zillow = pd.melt(zillow, id_vars=['RegionID', 'RegionName', 'City', 'State', 'Metro', 'CountyName', 'SizeRank'], 
        var_name='Date', value_name='Price')

    zillow.to_sql('zillow', con=engine, if_exists='replace', index=False)
