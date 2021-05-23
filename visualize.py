# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 08:41:16 2021

@author: rayde
"""
import matplotlib.pyplot as plt

class Visualize:

    def plot_barh(df, title, path_to_save, zipcode_col='zipcode', cap_rate_col='cap_rate', legend_label='Cap Rate', x_label= 'Cap Rate', y_label= 'Zipcode'):
        plt.barh(df[zipcode_col], df[cap_rate_col], label=legend_label)
        plt.legend()
    
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
    
        plt.show()
        plt.savefig(path_to_save)