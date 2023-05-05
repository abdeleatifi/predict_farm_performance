import ee
import numpy as np
import pandas as pd
from datetime import datetime as dt

ee.Authenticate()
ee.Initialize()

region = ee.Geometry.Polygon([[-7.791558613934031,33.01490300783628], [-7.792003860630503,33.01324314924896], [-7.788286318935862,33.01286529089581], [-7.788710107960215,33.014507163639024], [-7.791558613934031,33.01490300783628]])

start_date = '2023-01-01'
end_date = '2023-04-30'

# Define a function to calculate NDVI
def addNDVI(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('ndvi')
    return image.addBands(ndvi)

# Define a function to mask out clouds and shadows
def maskClouds(image):
    cloudBitMask = 1 << 10
    shadowBitMask = 1 << 3
    qa = image.select('QA60')
    mask = qa.bitwiseAnd(cloudBitMask).eq(0) and (qa.bitwiseAnd(shadowBitMask).eq(0))
    return image.updateMask(mask)

# Load Sentinel-2 imagery
s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterBounds(region) \
    .filterDate(start_date, end_date) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .map(addNDVI) \
    .map(maskClouds)

# Load crop data
crop_data = pd.read_csv('crop_data.csv')

# Join crop data with the Sentinel-2 imagery using the date field
def get_image_data(date):
    image = s2.filterDate(date, date.advance(1, 'day')).first()
    mean_ndvi = image.reduceRegion(reducer=ee.Reducer.mean(), geometry=region, scale=10).get('ndvi').getInfo()
    return mean_ndvi

crop_data['ndvi'] = crop_data['date'].apply(lambda date: get_image_data(ee.Date(date).format('YYYY-MM-dd')))

# Calculate loss and add it as a feature
crop_data['loss'] = (crop_data['expected_yield'] - crop_data['actual_yield']) / crop_data['expected_yield']
crop_data['loss_over_10_percent'] = crop_data['loss'] > 0.1

# Export the final data to a CSV file
crop_data.to_csv('crop_loss_data.csv', index=False)
