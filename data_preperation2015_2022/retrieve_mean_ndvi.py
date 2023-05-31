import ee

def retrieve_mean_ndvi(start_date, end_date, countyBoundary, winterWheatFC): 
    
    if not(winterWheatFC.size().getInfo()):
        return None

    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(countyBoundary) \
            .filterDate(start_date, end_date) 
        
    landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1')\
            .filterBounds(countyBoundary) \
            .filterDate(start_date, end_date)

    if sentinel2.size().getInfo():

        sentinel2 = sentinel2.mosaic()

        combined_ndvi = sentinel2.normalizedDifference(['B8', 'B4'])

        clippedNDVI = combined_ndvi.clipToCollection(winterWheatFC)

        mean_ndvi = clippedNDVI.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=winterWheatFC,
            bestEffort=True,
            scale=30
        ).getInfo().get('nd')
        
    elif landsat8.size().getInfo():

        landsat8 = ee.Algorithms.Landsat.simpleComposite(landsat8)

        combined_ndvi = landsat8.normalizedDifference(['B5', 'B4'])

        clippedNDVI = combined_ndvi.clipToCollection(winterWheatFC)

        mean_ndvi = clippedNDVI.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=winterWheatFC,
            bestEffort=True,
            scale=30
        ).getInfo().get('nd')

    else:

        return None

    return mean_ndvi
    