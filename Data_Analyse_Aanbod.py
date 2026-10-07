# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 13:41:22 2026

@author: ryans
"""

import pandas as pd
import matplotlib.pyplot as plt
# plt.style.use('seaborn-v0_8')
plt.style.use('bmh')

# loading data
path = "G:\\Mijn Drive\\School\\Toegepaste Wiskunde\\Jaar 4 (2026 - 2027)\\Semester 1\\Project 5\\Python\\Scripts\\"
inventory = pd.read_excel(path+'Metric Store - Inventory.xlsx')

# data preperation
inventory['Geographical Indicator'] = inventory['Geographical Indicator'].ffill()
inventory = inventory.fillna(0)

class Offer:
    def __init__(self, input_df=inventory):
        self.input_df = input_df

    @property
    def unique_locations(self):
        return list(self.input_df['Geographical Indicator'].unique())

    @property
    def unique_bikes(self):
        return list(self.input_df['Colour Category'].unique()) 
        
    def offer_per_location(self, location):
        return self.input_df[self.input_df['Geographical Indicator'] == location]

    def offer_per_location_and_bike_type(self, location, bike_type):
        offer_per_location = self.offer_per_location(location)
        return offer_per_location[offer_per_location['Colour Category'] == bike_type]

    def return_dict_info(self, location, bike_type):
        try:
            info_dict = dict(self.offer_per_location_and_bike_type(location, bike_type).iloc[0])
            info_dict = dict(list(info_dict.items())[2:])
        except IndexError:
            raise ValueError('No info over location or bike type.')
        
        return info_dict

    def plot_offer_per_location_and_bike_type(self, location, bike_type):
        info_dict = self.return_dict_info(location, bike_type) # retrieving the data
 
        # plotting
        dict_values = list(info_dict.values())[:-1]
        dict_keys = list(info_dict.keys())[:-1]
        plt.plot(dict_values)
        plt.xticks(list(range(len(dict_values))), dict_keys)
        plt.xticks(rotation=90)
        plt.xlabel('Maand')
        plt.ylabel('Aantal Fietsen [Inventory]')
        plt.title(f'Aanbod in {location} voor {bike_type}')
        plt.show()
        
