from meteostat import Daily, Stations
import ee

# get weather data for a new datapoint
def get_meteostat_data(crop_geometry, start_date, har_date):
    
    if not(crop_geometry.size().getInfo()):
        weather_data = {'gdd' : None,
                    'ehdd' : None,
                    'ecdd' : None}
        return weather_data
    
    geometries = crop_geometry.geometry().geometries().getInfo()
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

    weather_data = {'gdd' : gdd,
                    'ehdd' : ehdd,
                    'ecdd' : ecdd}

    return weather_data # (in degrees Celsius)