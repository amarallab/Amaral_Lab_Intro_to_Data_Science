import json
import requests

import pandas as pd

from datetime import datetime
from io import StringIO
# from pytz import timezone



##########################################################################################
def get_stations( api_url, my_keys, longitude, latitude, delta ):
    """
    This functions produces a dictionary where the keys are station
    names and the values are station indices from a search within a 
    box around a given longitude and latitute and a given width
    in degrees of longitude and latitude.
    
    Inputs:
        api_url -- str
        my_keys -- str
        longitude -- float (negative values for W)
        latitude -- float (negative values for S)
        delta -- float

    Returns:
        dict
    """
    my_parameters = { 'api_key': my_keys['Read Key'], 
                      'fields': 'name',
                      'nwlng': longitude-delta, 'nwlat': latitude+delta,
                      'selng': longitude+delta, 'selat': latitude-delta }
    
    response = requests.get(api_url, my_parameters)
    print( f"Request was completed with code {response.status_code}.\n" )

    data = json.loads(response.text)
    
    station_names = {}
    for item in data['data']:
        station_names[item[1]] = str( item[0] )
        
    return station_names


##########################################################################################
def get_info_for_station( api_url, my_station_id = '4395', my_parameters = {} ):
    """ 
    This function returns a dictionary with the info for a given PurpleAir station. 
    Returns None if station ID does not exist.
    Default value is ID for 'West Rogers Park' station.

    input:
        api_url -- a string with a web address
        my_station_id -- a string with a number
        my_parameters -- a dictionary with READ KEY
        
    output:
        data -- a dictionary if there is data or None
    """
    built_url = f"{api_url}{my_station_id}/"
    response = requests.get(built_url, my_parameters)
#     print(response.url)
    print( f"Request was completed with code {response.status_code}.\n" )
    
    data = json.loads(response.text)
    print(data.keys())
    print()
    if len(data) > 0:
        return data
    else:        
        return None    


##########################################################################################
def get_station_data( api_url, my_station_id = '4395', my_parameters = {}, 
                      verbose = False ):
    """ 
    This function returns a dataframe with the data obtained using the API.
    You can retrieve historical data by providing a start time_stamp.  
    The maximum request is 3 days of data.
    
    If the response code is 429 you have been making too many request and 
    have to wait a bit.
    
    input:
        api_url -- a string with a web address
        my_station_id -- a string with a number
        my_parameters -- a dictionary with READ KEY, start and end 
                         time stamps, and strings of fields
        verbose -- a Boolean for determining whether to write extra stuff
    
    output:
        a Pandas dataframe if data is retrieved or None
    """
    built_url = f"{api_url}{my_station_id}/history/csv/"
    response = requests.get(built_url, params = my_parameters)
    if verbose:
        print( f"Request was completed with code {response.status_code}.\n" )

    if response.status_code == 200:
        return pd.read_csv( StringIO(response.text) )
    
    else:
        print( f"Request was completed with code {response.status_code}.\n" )
        print(response.text)
        return None


##########################################################################################
def clean_station_data( df ):
    """ 
    This function returns a dataframe with the data provided by the 
    station and a human readable date and time of measurements.  
    Notice that data was also time ordered.

    input:
        df -- dataframe with data returned by API
    
    output:
        dataframe        
    """ 
    if len(df) == 0:
        return None
    
    local_date_n_times = []
    for i in range(len(df)):
        date_n_time = datetime.utcfromtimestamp( df.time_stamp[i]  )
        local_date_n_times.append( date_n_time )

    df['Date & Time'] = local_date_n_times

    return df.sort_values('time_stamp')
