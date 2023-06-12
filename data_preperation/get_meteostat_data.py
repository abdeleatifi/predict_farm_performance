import datetime
from meteostat import Daily, Stations
from get_ndvi_data import ras_to_vec
import ee

def get_meteostat_data(df):

    df = df.copy()

    start_date = datetime.datetime.strptime(df['Planting_Dates']+'-'+str(df['Year']-1), '%d-%b-%Y')
    har_date = datetime.datetime.strptime(df['Harvesting_Dates']+'-'+str(df['Year']), '%d-%b-%Y')

    countyBoundary, crop_geometry = ras_to_vec(df['State_ANSI'], df['County_ANSI'], start_date, har_date)
    
    if not(crop_geometry.size().getInfo()):
        df.loc['gdd'] = None
        df.loc['ehdd'] = None
        df.loc['ecdd'] = None
        return df
    
    geometries = countyBoundary.geometry().geometries().getInfo()
    longitude, latitude = ee.Geometry(geometries[0]).centroid().getInfo()['coordinates']
    
    stations = Stations()
    stations = stations.nearby(latitude, longitude)

    # Get the closest weather station
    station = stations.fetch(1)

    # Fetch the daily weather data for the specified time period from the nearest station
    data = Daily(station, start=start_date, end=har_date)
    data = data.fetch()

    temperatures = data['tavg'].dropna().tolist()

    T_base = 5  # Base temperature for wheat crop (in degrees Celsius)
    T_upper = 30  # Upper temperature for wheat crop (in degrees Celsius)

    gdd = sum([max(temperature - T_base, 0) for temperature in temperatures]) # (in degrees Celsius)

    ehdd = sum([max(temperature - T_upper, 0) for temperature in temperatures]) # (in degrees Celsius)

    ecdd = sum([max(T_base - temperature, 0) for temperature in temperatures]) # (in degrees Celsius)


    df.loc['gdd'] = gdd # (in degrees Celsius)
    df.loc['ehdd'] = ehdd # (in degrees Celsius)
    df.loc['ecdd'] = ecdd # (in degrees Celsius)

    return df