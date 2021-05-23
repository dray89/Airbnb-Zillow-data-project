# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 21:54:49 2021

@author: rayde
"""
import requests
import lxml
from lxml import html
import pandas
import numpy as np
import pickle 
from SQL_functions import SQL_functions

#Scrapes NYC zipcodes to filter observations to just those in NYC

def scrape_zipcodes(url = "https://www.nycbynatives.com/nyc_info/new_york_city_zip_codes.php"):
     page = requests.get(url)
     tree = html.fromstring(page.content)
     table = tree.xpath('//table')
     table = list(map(lambda x: pandas.read_html(lxml.etree.tostring(table[x], method='xml'))[0], range(0,len(table))))
     return table

def clean_output(table):     
     l1 = table[0].loc[:,0].values
     l2 = table[0].loc[:,3].values
     return np.concatenate((l1, l2))
 
def save_zipcodes(python_list, filename = 'nyc_zipcodes.txt'):
    with open(filename, 'wb') as zipcode_file:
        pickle.dump(python_list, zipcode_file)
    print('successfully saved list to file')

def open_zipcode_file(filepath= 'nyc_zipcodes.txt'):
    with open(filepath, "rb") as zipcode_file:
        loaded_list = pickle.load(zipcode_file)
    return loaded_list

def add_zipcodes(python_list, zipcodes_to_add = [10075, 10065, 10080, 10129]):
    for x in zipcodes_to_add:
        python_list.append(x)
    return python_list

def add_to_sql(python_list, engine, table_name = 'nyc_zipcodes', if_exists='replace', index=False):
    zipcodes = pandas.DataFrame(table_extended, columns = ['zipcodes'])
    zipcodes.to_sql(table_name, con=engine, if_exists=if_exists, index=index)
    print(f'{table_name} table created in SQL')
    
if __name__ == '__main__':
    table = scrape_zipcodes()
    table_clean = clean_output(table)
    python_list = list(table_clean)
    table_extended = add_zipcodes(python_list)
    save_zipcodes(table_extended)
    engine = SQL_functions().sql_alchemy_engine()
    add_to_sql(table_extended, engine)
    add_to_sql(table_extended, engine)
    