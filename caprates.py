# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 16:30:48 2021

@author: rayde
"""



class CapRates:
    def __init__(self, cap_rates, occupancy):
        self.cap_rates = cap_rates
        self.occupancy = occupancy
        
    def calc_cap_rate(self, operating_income_col='operating_income', property_val_col = 'Price', cap_rate_col = 'cap_rate'):
        self.cap_rates[cap_rate_col] = self.cap_rates[operating_income_col]/self.cap_rates[property_val_col]
        return self.cap_rates
    
    def top_10_by_cap_rate(self, cap_rate_col = 'cap_rate'):
        cap_rates = self.cap_rates
        cond = cap_rates[cap_rate_col] > self.__average_cap_rate()
        return self.cap_rates[cond].sort_values(by=cap_rate_col, ascending=False).head(10)
    
    def top_10_cap_demand(self, cap_rate_col = 'cap_rate'):
        self.cap_rates['cap_demand'] = self.cap_rates.cap_rate*self.occupancy.median_occupied_365
        cond = self.cap_rates[cap_rate_col] > self.__average_cap_rate()
        return self.cap_rates[cond].sort_values(by='cap_demand', ascending=False).head(10)
        
    def filter_by_demand(self, vacancy_rates, cap_rate_col='cap_rate', zipcode_col = 'zipcode', vacancy_zipcode_col='zipcode', median_vacancy_col = 'median_vacancy_30', vacancy_threshold=0, imputed_income_col='imputed_operating_income'):
        cap_rates = self.cap_rates
        cond = (cap_rates[cap_rate_col] > self.__average_cap_rate()) 
        cond2 = (cap_rates[zipcode_col].isin(vacancy_rates[vacancy_rates[median_vacancy_col]==vacancy_threshold][vacancy_zipcode_col]))
        cond3 = (cap_rates[imputed_income_col] == True)
        return self.cap_rates[cond & (cond2 | cond3)].sort_values(by=cap_rate_col, ascending=False)
        
    def __average_cap_rate(self, cap_rate_col = 'cap_rate'):
        return self.cap_rates[cap_rate_col].mean()
     

