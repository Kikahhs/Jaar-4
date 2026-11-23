# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 13:41:22 2026

@author: ryans
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8')
plt.style.use('bmh')

# loading data
path = "/data/home/s18097847/notebooks/Jaar-4/Data/"
InUse_Bikes = pd.read_excel(path+'Metric Store - InUse Bikes.xlsx')
Subscriptions = pd.read_excel(path+'Metric Store - Subscriptions.xlsx')

# data preparation
InUse_Bikes['Geographical Indicator'] = InUse_Bikes['Geographical Indicator'].ffill()
Subscriptions['Geographical Indicator'] = Subscriptions['Geographical Indicator'].ffill()

InUse_Bikes = InUse_Bikes.fillna(0)
Subscriptions = Subscriptions.fillna(0)

place_category = list(InUse_Bikes.columns)[:2]
months = list(InUse_Bikes.columns)[2:]

demand_df = Subscriptions[months] - InUse_Bikes[months] # vraag berekenen
demand_df = demand_df.mask(demand_df < 0) # negatieve waardes voor nan vervangen
demand_df = pd.concat([InUse_Bikes[place_category], demand_df], axis=1)
demand_df = demand_df.dropna() # alle nan waardes verwijderen
demand_df = demand_df[demand_df['Colour Category'] != 'Totaal']

class Demand:
    def __init__(self, input_df=demand_df):
        self.input_df = input_df
    
    
    @property
    def unique_locations(self):
        return list(self.input_df['Geographical Indicator'].unique())

    @property
    def unique_bikes(self):
        return list(self.input_df['Colour Category'].unique()) 
        
    def demand_per_location(self, location):
        return self.input_df[self.input_df['Geographical Indicator'] == location]

    def demand_per_location_summed(self, location):
        demand_df = self.demand_per_location(location)
        demand_df = demand_df.drop(["Geographical Indicator","Colour Category"], axis=1)
        demand_df.loc['total']= demand_df.sum()
        return demand_df.loc['total']
    
    def demand_per_location_and_bike_type(self, location, bike_type):
        demand_per_location = self.demand_per_location(location)
        return demand_per_location[demand_per_location['Colour Category'] == bike_type]
    
    def return_dict_info(self, location, bike_type):
        try:
            info_dict = dict(self.demand_per_location_and_bike_type(location, bike_type).iloc[0])
            info_dict = dict(list(info_dict.items())[2:])
        except IndexError:
            raise ValueError('No info over location or bike type.')

        return info_dict
        
    def demand_total_stores(self, store_list):
        total_merged = {}
        for store in store_list:
            for key, value in self.demand_per_location_summed(store).items():
                total_merged[key] = total_merged.get(key, 0) + value
        return total_merged


    
    def plot_demand_per_location_and_bike_type(self, location, bike_type):
        info_dict = self.return_dict_info(location, bike_type) # retrieving the data
 
        # plotting
        dict_values = list(info_dict.values())[:-1]
        dict_keys = list(info_dict.keys())[:-1]
        plt.plot(dict_values)
        plt.xticks(list(range(len(dict_values))), dict_keys)
        plt.xticks(rotation=90)
        plt.xlabel('Maand')
        plt.ylabel('Aantal Fietsen [Subscription - InUse Bikes]')
        plt.title(f'Vraag in {location} voor {bike_type}')
        plt.show()

    def plot_demand_total(self, dictionary1, dictionary2, magazijnnaam):
            lists1 = sorted(dictionary1.items()) # sorted by key, return a list of tuples
            x1, y1 = zip(*lists1) # unpack a list of pairs into two tuples
            plt.plot(x1, y1, label = 'Vraag winkels')
            lists2 = sorted(dictionary2.items()) # sorted by key, return a list of tuples
            x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
            plt.plot(x2, y2, label = 'Capaciteit magazijn Den Hoorn')
            plt.xticks(rotation=90)
            plt.xlabel('Maand')
            plt.ylabel('Aantal Fietsen')
            ax = plt.gca() 
            ax.set_facecolor("white")
            ax.legend(frameon=True, facecolor= "inherit")
            plt.title('Vraag winkels t.o.v. capaciteit Den Hoorn')
            return plt.show()