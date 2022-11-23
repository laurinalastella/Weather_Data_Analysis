# our datacleaning functions
import GetCleanData as gcda
# huh, i need to re-import stuff that is already imported into a file i'm importing?
import json


cities = [
    {'geo' : 'gb | London', 'latitude': 51.509648, 'longitude': -0.099076, 'name': 'London', 'region': 'Greater London', 'region_code': None, 'country': 'United Kingdom', 'country_code': 'GBR'}, 
    {'geo' : 'de | Berlin','latitude': 52.524932, 'longitude': 13.407032, 'name': 'Berlin', 'region': 'Berlin', 'region_code': 'BE', 'country': 'Germany', 'country_code': 'DEU'}, 
    {'geo' : 'jp | Tokyo', 'latitude': 35.695126, 'longitude': 139.75391, 'name': 'Tokyo', 'region': 'Tokyo', 'region_code': 'TK', 'country': 'Japan', 'country_code': 'JPN'}, 
    {'geo' : 'us | New York', 'latitude': 40.68295, 'longitude': -73.9708, 'name': 'New York', 'region': 'New York', 'region_code': 'NY', 'country': 'United States', 'country_code': 'USA'}, 
    {'geo' : 'us | San Francisco', 'latitude': 37.778008, 'longitude': -122.431272, 'name': 'San Francisco', 'region': 'California', 'region_code': 'CA',  'country': 'United States', 'country_code': 'USA'}
    ]

#years = [2010, ..., 2019]
years = [2010 + i for i in range(10)]

# includes both year endpoints: to get one year, strat_year = end_year
def get_multi_annual_adjective_stats(latitude, longitude, start_year, end_year):
    daf = gcda.get_clean_weather(latitude, longitude, start_year, end_year)
    # add boolean columns
    daf = gcda.add_bool_col_for_adj(daf)
    # get stats and return them
    return gcda.bool_to_stats(daf)

def all_years_five_cities():
    output = {'geo': [], 'weatherdata' : []}
    for city in cities:
        output['geo'].append(city['geo'])
        weather = get_multi_annual_adjective_stats(city['latitude'], city['longitude'],  2010, 2019)
        weather['geo'] = city['geo']
        weather['city'] = city['name']
        weather['country'] = city['country']
        output['weatherdata'].append(weather)
    return output

def make_json_all_years_five_cities():
    stuff = all_years_five_cities()
    with open("five_cities_2010_to_2019.json", "w") as outfile:
        json.dump(stuff, outfile)

