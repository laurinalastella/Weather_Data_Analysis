import requests
import pandas as pd
import json
import datetime
import numpy as np
# for position API
import http.client, urllib.parse


# Error handling: Country
class CoutryNotStringError(Exception):
    pass
# Error handling: City
class CityNotStringError(Exception):
    pass
# Error handling: PositionStack API Call
class PositionAPIBadCallError(Exception):
    pass
# Error handling: PositionStack API Request
class PositionAPIBadRequestError(Exception):
    pass
# Error handling: PositionStack API Load
class PositionAPIBadLoadError(Exception):
    pass
# Error handling: Weather API Call
class WeatherAPIBadCallError(Exception):
    pass
# Error handling: Weather API Load
class WeatherAPIBadLoadError(Exception):
    pass



# get_latt_long gets(country, city) latitude and longitude 
# for a given country (2-character code) and city (name or postal code) (="query")
# from positionstack.com
def get_latt_long(country, city):

    if not isinstance(country, str):
        raise CoutryNotStringError
    if not isinstance(city, str):
        raise CityNotStringError

    try:
        conn = http.client.HTTPConnection('api.positionstack.com')
    except:
        raise PositionAPIBadCallError

    params = urllib.parse.urlencode({
        'access_key': '1fbf7de4ce05274e9b9005659970c429',
        # Variables get live user input.
        'country': country,
        'query': city,
        # "limit" of 1 ensures only 1 Lat/Lon will be passed below. 
        'limit': 1
    })

    try:
        conn.request('GET', '/v1/forward?{}'.format(params))
        res = conn.getresponse()
    except:
        raise PositionAPIBadRequestError

    try:
        geo = res.read()
        geo_str = (geo.decode('utf-8'))
        # Convert string to json (which is a dictionary).
        geo_json = json.loads(geo_str)
        # extract latitude
        geo_json_lat = geo_json['data']
        var_lat = [] 
        for x in geo_json_lat:
            var_lat.append((x['latitude']))
        # extract longitude
        geo_json_lon = geo_json['data']
        var_lon = []
        for x in geo_json_lon:
            var_lon.append((x['longitude']))
        return (var_lat[0], var_lon[0])
    except:
        raise PositionAPIBadLoadError


# The next two functions assemble urls for weather API requests
# from https://archive-api.open-meteo.com/v1/era5
# The time interval is hard-coded to be whole years; also hard-coded:
# variables drawn, imperial (USian) units used, (PDT) timezone.

def get_hourly_weather_url(latitude, longitude, start_year, end_year):
    url_snip_hr = {}
    # Break URL into snippets to be assembled below, hourly:
    url_snip_hr[1] = "https://archive-api.open-meteo.com/v1/era5?latitude=" 
    url_snip_hr[2]= str(latitude)
    url_snip_hr[3] = "&longitude="
    url_snip_hr[4] = str(longitude)
    url_snip_hr[5] = "&start_date="
    url_snip_hr[6] = str(start_year)
    url_snip_hr[7] = "-01-01&end_date="  # month and day of start_year
    url_snip_hr[8] = str(end_year)
    url_snip_hr[9] = "-12-31&hourly="   # elements, hourly
    url_snip_hr[10] = "temperature_2m,"   # data element
    url_snip_hr[11] = "relativehumidity_2m,"   # data element
    url_snip_hr[12] = "rain,"   # data element
    url_snip_hr[13] = "snowfall,"   # data element
    url_snip_hr[14] = "cloudcover,"   # data element
    url_snip_hr[15] = "windspeed_10m,"   # data element
    url_snip_hr[16] = "winddirection_10m"   # data element
    url_snip_hr[17] = "&timezone=America%2FLos_Angeles"   # time zone
    url_snip_hr[18] = "&temperature_unit=fahrenheit"   # temp unit
    url_snip_hr[19] = "&windspeed_unit=mph"   # windspeed unit
    url_snip_hr[20] = "&precipitation_unit=inch"   # precip unit
    weather_url_hr = ""
    for i in range(20):
        weather_url_hr += url_snip_hr[i+1]
    return weather_url_hr



def get_daily_weather_url(latitude, longitude, start_year, end_year):
    url_snip_dy = {}
    # Break URL into snippets to be assembled below, daily:
    url_snip_dy[1] = "https://archive-api.open-meteo.com/v1/era5?latitude=" 
    url_snip_dy[2] = str(latitude)   # latitude, input from previous json
    url_snip_dy[3] = "&longitude="
    url_snip_dy[4] = str(longitude)   # longitude, input from previous json
    url_snip_dy[5] = "&start_date="
    url_snip_dy[6] = str(start_year)
    url_snip_dy[7] = "-01-01&end_date="  # month and day of start_year
    url_snip_dy[8] = str(end_year)
    url_snip_dy[9] = "-12-31&daily="   # elements, daily
    url_snip_dy[10] = "temperature_2m_max,"   # data element
    url_snip_dy[11] = "temperature_2m_min,"   # data element
    url_snip_dy[12] = "rain_sum,"   # data element
    url_snip_dy[13] = "snowfall_sum,"   # data element
    url_snip_dy[14] = "precipitation_hours"   # data element
    url_snip_dy[15] = "&timezone=America%2FLos_Angeles"   # time zone
    url_snip_dy[16] = "&temperature_unit=fahrenheit"   # temp unit
    url_snip_dy[17] = "&windspeed_unit=mph"   # windspeed unit
    url_snip_dy[18] = "&precipitation_unit=inch"   # precip unit
    weather_url_dy = ""
    for i in range(18):
        weather_url_dy += url_snip_dy[i+1]
    return weather_url_dy

# get_weather_url calls one of the above two functions
# daily_or_hourly should be a string, 'daily' or 'hourly'
#  ### needs error-handling ###

def get_weather_url(latitude, longitude, start_year, end_year, daily_or_hourly):
    if daily_or_hourly == 'daily':
        return get_daily_weather_url(latitude, longitude, start_year, end_year)
    elif daily_or_hourly== 'hourly':
        return get_hourly_weather_url(latitude, longitude, start_year, end_year)
    else:
        return 'error'

# this function retrieves weather data for given lattitue/longitude coordinates
# from https://archive-api.open-meteo.com/v1/era5
# for the given years; 
# e.g. if start_year=2010 and end_year=2020, 11 years of data are retrieved,
# starting 2010-01-01 and ending 2020-12-31, inclusive
# again, daily_or_hourly must be one of the two strings
# note that wind_direction in hourly is null when windspeed is 0
# we do nothing with wind direction, so don't bother fixing it
# gaierror means check your internet connection.

def get_weather(latitude, longitude, start_year, end_year, daily_or_hourly):
    url = get_weather_url(latitude, longitude, start_year, end_year, daily_or_hourly)
    
    try:
        # Data comes in as one long string:
        weather_hr_str = requests.get(url).text
    except:
        raise WeatherAPIBadCallError
    
    try:
        # So convert string to dictionary.
        weather_hr_json = json.loads(weather_hr_str)
        # now turn dictionary into dataframe
        weather_raw = pd.DataFrame.from_records(weather_hr_json[daily_or_hourly])
    except:
        raise WeatherAPIBadLoadError

    # convert the provided ISO string 'time' into a 'pure_date' in python datetime format
    # for aggregating and joining with daily data
    weather_raw["pure_date"] = weather_raw['time'].map(lambda x: 
                                                        datetime.datetime.fromisoformat(x[0:10]))
    # forget the string with the hour
    weather_raw.drop('time', axis=1, inplace=True)
    return weather_raw

# this auxillary function will be used to aggreagte hourly data into daily
# for example, getting the temperature of 6th hottest hour answers questions like:
# Were there at least 6 hours above 80F? and Were there at least 18 hours below 32F?

def enth(x, n):
    return x.sort_values().iloc[n]

# this function takes in the hourly and daily weather dataframes made by get_weather
#  ### behaviour if different time periods ###
# the returned dataframe is indexed by pure_date, so same number of rows as daily input
# the returned dataframe has all the columns of the daily input,
# plus a bunch of aggregates of data from hourly
# yes, max_wind = wind_high and temp_high is also a rename; someday, we fix this inefficiency

def agg_hourly_and_daily(hourly_df, daily_df):
    ## BEWARE arguments are passed by reference, don't mess with them ! ##
    output_df = hourly_df.groupby('pure_date').agg(
    # historical statistics (adjectives): humid_avg, wind_high, cloud_avg, temp_6
        humid_avg=('relativehumidity_2m', np.mean),
        wind_high = ('windspeed_10m', np.max),
        cloud_avg=('cloudcover', np.mean),
        temp_6= ('temperature_2m', lambda x: enth(x,18)),
    # machine learning: avg_humidity, median_wind, max_wind, cloud_4, cloud_12, cloud_20
        avg_humidity=('relativehumidity_2m', np.mean),
        median_wind = ('windspeed_10m', np.median),
        max_wind = ('windspeed_10m', np.max),
        cloud_4 = ('cloudcover', lambda x: enth(x,3)),
        cloud_12 = ('cloudcover', lambda x: enth(x,11)),
        cloud_20 = ('cloudcover', lambda x: enth(x,19)) )
    output_df = output_df.join(daily_df.set_index('pure_date'))
    output_df['temp_high'] = output_df['temperature_2m_max']
    # i want 'pure_date' to go back to being a regular column
    output_df.reset_index(inplace=True)
    return output_df

# The next function takes in a date interval, 
# generates the same intervals in previous years, and 
# returns the starts and ends of those intervals, starting with the original.

# start_date, end_date should be datetime; years >= 0 should integer; 
# if years=0, ([start_date*], [end_date*]) is returned;
# (*) with feb-29 is replaced by feb-28 for start_date, mar-01 for end_date


def backdate(start_date, end_date, years):
    # replace start_date feb-29 by feb-28
    if (start_date.month == 2 & start_date.day == 29):
        start_date = start_date - datetime.timedelta(days = 1)
    # replace end_date feb-29 by mar-01
    if (end_date.month == 2 & end_date.day == 29):
        end_date = end_date + datetime.timedelta(days = 1)
    starts = [start_date]
    ends = [end_date]
    for i in range(years):
        start_date = start_date.replace(year = start_date.year -1)
        end_date = end_date.replace(year = end_date.year -1)
        starts.append(start_date)
        ends.append(end_date)
    return (starts, ends)
    
# The next function ingests a dataframe with a column 'pure_date', 
# along with a date interval, and the number of years to go back by;
# and returns the rows of the input dataframe
# where the pure_date falls within one of the intervals, including both endpoints.

def date_period_filter(daf, start_date, end_date, years):
    starts_ends = backdate(start_date, end_date, years)
    # for each backdated interval, test whether pure_date falls in it, then
    # add up the booleans, get 0 if all false, more otherwise
    mask = sum( (daf['pure_date'] >= starts_ends[0][i]) &
               (daf['pure_date'] <= starts_ends[1][i]) for i in range(years) )
    # if interval is too big, backdated intervals may overlap, but we don't want 2 as a value
    # also, returns it to boolean from integer
    mask = (mask > 0)
    return daf[mask].copy()
    
# the next function labels the rows of the dataframe with booleans for adjectives
# ideally, the definitions of adjectives should be stored separately and
# passed to this function, for easier future adjustment.
# cleaning up this kludge is beyond the scope of this project :(

def add_bool_col_for_adj(daf):
    daf_with_bool = daf.copy()
    
    # temp
    # freezing = >19hours with <32F: Use "temp_6" (6th highest temp of day) as cutoff.
    # cold = high <60F
    # hot = >6hours with >80F
    # warm = leftovers
    daf_with_bool['freezing'] = (daf_with_bool['temp_6'] <= 32)
    daf_with_bool['cold'] = (daf_with_bool['temp_high'] <= 60) & (daf_with_bool['freezing'] == 0)
    daf_with_bool['hot'] = (daf_with_bool['temp_6'] >= 80)
    daf_with_bool['warm'] = (daf_with_bool['freezing'] == 0) & (daf_with_bool['cold'] == 0) & (daf_with_bool['hot'] == 0)

    # clouds
    # average hourly "percent cloud cover"
    # clear = <=33%
    # cloudy = >= 67%
    # partly_cloudy = leftovers
    daf_with_bool['clear'] = (daf_with_bool['cloud_avg'] <= 30)
    daf_with_bool['cloudy'] = (daf_with_bool['cloud_avg'] >= 60)
    daf_with_bool['partly_cloudy'] = (daf_with_bool['clear'] == 0) & (daf_with_bool['cloudy'] == 0)

    # rain
    # not_rainy = 0 hours, or  <2.5 mm total rain (Laurina changing to 0.5 inches)
    # very_rainy = >=6 hour and >=10mm (Laurina changing to 2 inches)
    # lightly_rainy = leftovers
    daf_with_bool['not_rainy'] = (daf_with_bool['rain_sum'] <= 0.5) | (daf_with_bool['precipitation_hours'] == 0)
    daf_with_bool['very_rainy'] = (daf_with_bool['rain_sum'] >= 2) | (daf_with_bool['precipitation_hours'] >= 6)
    daf_with_bool['lightly_rainy'] = (daf_with_bool['not_rainy'] == 0) & (daf_with_bool['very_rainy'] == 0)

    # snow
    # data used: total snow for the day
    # not_snowy = 0
    # very_snowy = >6"
    # lightly_snowy = >0
    # (unlike rain, we ignore hours)   
    daf_with_bool['not_snowy'] = (daf_with_bool['snowfall_sum'] == 0)
    daf_with_bool['very_snowy'] = (daf_with_bool['snowfall_sum'] >= 6)
    daf_with_bool['lightly_snowy'] = (daf_with_bool['not_snowy'] == 0) & (daf_with_bool['very_snowy'] == 0)

    # wind
    # windy = maximum	> ?? mph
    # maybe 8? mayb 12  
    daf_with_bool['windy'] = (daf_with_bool['wind_high'] >= 12)

    # humidity
    # average hourlies, then:
    # low_humidity = <30%
    # high_humidity = >60%
    # medium_humidity = leftovers

    daf_with_bool['low_humidity'] = (daf_with_bool['humid_avg'] <= 30)
    daf_with_bool['high_humidity'] = (daf_with_bool['humid_avg'] >= 60)
    daf_with_bool['medium_humidity'] = (daf_with_bool['low_humidity'] == 0) & (daf_with_bool['high_humidity'] == 0)

    return daf_with_bool
    
# the next function aggregates boolean columns into frequency statistics.
# ### THIS SHOULD USE BUILT-IN AVERAGE !!! like daf['warm'].mean()

def bool_to_stats(daf):
    # list of column names to be aggregated
    bool_cols = ['freezing', 'cold', 'warm', 'hot',
                'not_rainy', 'lightly_rainy', 'very_rainy',
                'not_snowy', 'lightly_snowy', 'very_snowy',
                'windy',
                'low_humidity', 'medium_humidity', 'high_humidity',
                'clear', 'partly_cloudy', 'cloudy']
    # denominators for rate/likelyhood
    row_count = len(daf)
    # initialize storage
    stats_dict = {}
    # aggregate
    for stat in bool_cols:
        stats_dict[stat] = daf[stat].sum() / row_count
    return stats_dict

# now some wrapper functions

def get_clean_weather(lattitude, longitude, start_year, end_year):
    hourly_df = get_weather(lattitude, longitude, start_year, end_year, 'hourly')
    daily_df = get_weather(lattitude, longitude, start_year, end_year, 'daily')
    return agg_hourly_and_daily(hourly_df, daily_df)

def get_clean_weather_loc(country, city, start_year, end_year):
    coords = get_latt_long(country, city)
    return get_clean_weather(coords[0], coords[1], start_year, end_year)

# user-facing function, so start_date, end_date are ISO strings, not datetime

def get_adjective_stats(lattitude, longitude, start_date_iso, end_date_iso, years):
    start_date = datetime.datetime.fromisoformat(start_date_iso[0:10])
    end_date = datetime.datetime.fromisoformat(end_date_iso[0:10])
    # latest year for which full-year data exist
    end_year = datetime.datetime.today().year - 1
    # get-weather includes both endpoints, so gives 10 years with start=n, end=n+9
    start_year = end_year -years +1
    # get weather data
    daf = get_clean_weather(lattitude, longitude, start_year, end_year)
    # filter by dates  
    # adding extra years in case requested dates are far in the future
    daf = date_period_filter(daf, start_date, end_date, years+3)
    # add boolean columns
    daf = add_bool_col_for_adj(daf)
    # get stats and return them
    return bool_to_stats(daf)

def get_adjective_stats_loc(country, city, start_date_iso, end_date_iso):
    coords = get_latt_long(country, city)
    return get_adjective_stats(coords[0], coords[1], start_date_iso, end_date_iso, 20)


