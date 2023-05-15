# 4/1AbUR2VOtoJr-n9uHwcXvaD0m2VuWeeVh_2iOaX1I9OiKaJjI3pcV6PiUKOU
import ee

#ee.Authenticate()
ee.Initialize()

start_date = '2023-01-01'
end_date = '2023-04-30'

parcel_coords = [[-7.791558613934031,33.01490300783628], [-7.792003860630503,33.01324314924896], [-7.788286318935862,33.01286529089581], [-7.788710107960215,33.014507163639024], [-7.791558613934031,33.01490300783628]]

def get_sentinel2_images(parcel_id, start_date, end_date, parcel_coords):
    # Define the area of interest using the parcel coordinates
    aoi = ee.Geometry.Polygon(parcel_coords)

    # Define the Sentinel-2 collection
    sentinel2_collection = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi) \

    # Create a function to add NDVI band to each image in the collection
    def add_ndvi(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)

    # Map the NDVI function over the collection
    sentinel2_with_ndvi = sentinel2_collection.map(add_ndvi)

    # Convert the collection to a list
    sentinel2_list = sentinel2_with_ndvi.toList(sentinel2_with_ndvi.size())

    # Loop through the list and add each image to a new list
    sentinel2_images = []
    for i in range(sentinel2_list.size().getInfo()):
        sentinel2_image = ee.Image(sentinel2_list.get(i))
        sentinel2_images.append(sentinel2_image)

    # Return the list of Sentinel-2 images
    return sentinel2_images
