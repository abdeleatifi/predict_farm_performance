import rasterio
import numpy as np
import ee
import datetime
import os

ee.Authenticate()
ee.Initialize()

# Define the area of interest (AOI) as a polygon
aoi = ee.Geometry.Polygon([[-7.791558613934031,33.01490300783628], [-7.792003860630503,33.01324314924896], [-7.788286318935862,33.01286529089581], [-7.788710107960215,33.014507163639024], [-7.791558613934031,33.01490300783628]]) 

# Define the time range
start_date = datetime.date(2022, 1, 1) # Replace with your desired start date
end_date = datetime.date(2022, 2, 1) # Replace with your desired end date

# Define the Sentinel-2 collection
s2_collection = ee.ImageCollection('COPERNICUS/S2_SR')

# Filter the collection by the AOI and time range
filtered_collection = s2_collection.filterBounds(aoi).filterDate(start_date, end_date)

# Get the number of images in the collection
num_images = filtered_collection.size().getInfo()
print('Number of images found:', num_images)

# Iterate over the images in the collection and download them
for i in range(num_images):
    # Get the image
    image = ee.Image(filtered_collection.toList(num_images).get(i))
    
    # Get the image ID and date
    image_id = image.id().getInfo()
    image_date = datetime.datetime.utcfromtimestamp(image.get('system:time_start').getInfo()/1000.0).strftime('%Y-%m-%d')

    # Define the export parameters
    export_params = {
        'image': image,
        'description': 'Sentinel2_' + image_id + '_' + image_date,
        'scale': 10, # Replace with your desired scale
        'crs': 'EPSG:4326', # Replace with your desired CRS
        'region': aoi
    }

    # Export the image to Google Drive
    task = ee.batch.Export.image.toDrive(**export_params)
    task.start()

    # Wait for the task to complete
    print('Exporting image', i+1, 'of', num_images, '- ID:', image_id, '- Date:', image_date)
    while task.active():
        task.sleep(1)

sat_data = rasterio.open('path/to/satellite/image.tif')

red_band = sat_data.read(3)
nir_band = sat_data.read(4)

ndvi = (nir_band - red_band) / (nir_band + red_band)

# Save the NDVI image
profile = sat_data.profile
profile.update(dtype=rasterio.float32, count=1)
with rasterio.open('path/to/ndvi/image.tif', 'w', **profile) as dst:
    dst.write(ndvi.astype(rasterio.float32), 1)
