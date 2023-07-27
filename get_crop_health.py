import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from get_land_use_area import *
import datetime
import ee


try:
    ee.Initialize()
except:
    ee.Authenticate()
    ee.Initialize()


# get the health of crop_geometry parcel using a pretrained model
def get_crop_health(crop_geometry, start_date, end_date):

    ndvi_serie = get_ndvi_serie(crop_geometry, start_date, end_date)

    #land_area = get_land_area(crop_geometry)

    loaded_scaler = joblib.load('best_scaler.pkl')

    new_data_scaled = loaded_scaler.transform(np.array(ndvi_serie).reshape(1, len(ndvi_serie)))

    # Load the model from memory
    loaded_model = joblib.load('best_model.pkl')

    # Use the loaded model for predictions
    crop_health = loaded_model.predict(new_data_scaled)

    return crop_health


# get the timeseries ndvi values of the crop_geometry parcel
def get_ndvi_serie(crop_geometry, start_date, end_date):

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    har_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    ndvi_serie = []

    while start_date <= har_date:

        end_date = start_date + datetime.timedelta(weeks=2) - datetime.timedelta(days=1)

        mean_ndvi = get_mean_ndvi(crop_geometry, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        ndvi_serie.append(mean_ndvi)

        start_date = end_date + datetime.timedelta(days=1)
    
    
    return ndvi_serie

# get the satellite image from start_date to end_date trasform it to ndvi map then calculate the mean ndvi value of the image
def get_mean_ndvi(crop_geometry, start_date, end_date): 
    
    if not(crop_geometry.size().getInfo()):
        return None

    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(crop_geometry) \
            .filterDate(start_date, end_date) 

    sentinel2 = sentinel2.mosaic()

    combined_ndvi = sentinel2.normalizedDifference(['B8', 'B4'])

    clippedNDVI = combined_ndvi.clipToCollection(crop_geometry)

    mean_ndvi = clippedNDVI.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=crop_geometry,
        bestEffort=True,
        scale=30
    ).getInfo().get('nd')

    return mean_ndvi
    


