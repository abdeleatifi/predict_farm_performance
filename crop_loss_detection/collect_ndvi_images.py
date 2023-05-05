import ee
# 4/1AbUR2VOtoJr-n9uHwcXvaD0m2VuWeeVh_2iOaX1I9OiKaJjI3pcV6PiUKOU

ee.Authenticate()
ee.Initialize()

start_date = '2023-01-01'
end_date = '2023-04-30'

aoi = ee.Geometry.Polygon([[-7.791558613934031,33.01490300783628], [-7.792003860630503,33.01324314924896], [-7.788286318935862,33.01286529089581], [-7.788710107960215,33.014507163639024], [-7.791558613934031,33.01490300783628]])

s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
        .filterDate(start_date, end_date) \
        .filterBounds(aoi) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .sort('CLOUD_COVER') \
        .map(lambda image: image.addBands(image.normalizedDifference(['B8', 'B4']).rename('NDVI')))

# Print the number of images in the collection
print('Number of images: ', s2.size().getInfo())

# Print the first image in the collection
print('First image: ', s2.first().getInfo())