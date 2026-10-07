# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 13:58:23 2026

@author: ryans
"""

from Data_Analyse_Vraag import Demand
from Data_Analyse_Aanbod import Offer

unique_locations = Demand().unique_locations
unique_bikes = Demand().unique_bikes

print(unique_locations)
print(unique_bikes)
location = 'Regional Warehouse Tilburg - Breda'
bike_type = unique_bikes[1]

# Voor vraag
Demand().plot_demand_per_location_and_bike_type(location, bike_type)

# Voor aanbod
Offer().plot_offer_per_location_and_bike_type(location, bike_type)


