import ee

def retrieve_mean_ndvi(start_date, end_date, countyBoundary, winterWheatFC): 
    
    if not(winterWheatFC.size().getInfo()):
        return None
    
    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(countyBoundary) \
            .filterDate(start_date, end_date) 

    landsat7 = ee.ImageCollection('LANDSAT/LE07/C02/T1')\
            .filterBounds(countyBoundary) \
            .filterDate(start_date, end_date)
        
    landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1')\
            .filterBounds(countyBoundary) \
            .filterDate(start_date, end_date)

    if landsat7.size().getInfo() and landsat8.size().getInfo() and sentinel2.size().getInfo():

        sentinel2 = sentinel2.mosaic()
        landsat8 = ee.Algorithms.Landsat.simpleComposite(landsat8)
        landsat7 = ee.Algorithms.Landsat.simpleComposite(landsat7)

        ndvi_sentinel2 = sentinel2.normalizedDifference(['B8', 'B4'])
        ndvi_landsat7 = landsat7.normalizedDifference(['B4', 'B3'])
        ndvi_landsat8 = landsat8.normalizedDifference(['B5', 'B4'])

        combined_ndvi = ee.Image.cat([ndvi_sentinel2, ndvi_landsat8, ndvi_landsat7])
        
    elif landsat7.size().getInfo() and landsat8.size().getInfo():

        landsat8 = ee.Algorithms.Landsat.simpleComposite(landsat8)
        landsat7 = ee.Algorithms.Landsat.simpleComposite(landsat7)

        ndvi_landsat7 = landsat7.normalizedDifference(['B4', 'B3'])
        ndvi_landsat8 = landsat8.normalizedDifference(['B5', 'B4'])

        combined_ndvi = ee.Image.cat([ndvi_landsat8, ndvi_landsat7])
    
    elif sentinel2.size().getInfo() and landsat8.size().getInfo():
        
        sentinel2 = sentinel2.mosaic()
        landsat8 = ee.Algorithms.Landsat.simpleComposite(landsat8)

        ndvi_sentinel2 = sentinel2.normalizedDifference(['B8', 'B4'])
        ndvi_landsat8 = landsat8.normalizedDifference(['B5', 'B4'])

        combined_ndvi = ee.Image.cat([ndvi_sentinel2, ndvi_landsat8])
    
    elif sentinel2.size().getInfo() and landsat7.size().getInfo():

        sentinel2 = sentinel2.mosaic()
        landsat7 = ee.Algorithms.Landsat.simpleComposite(landsat7)

        ndvi_sentinel2 = sentinel2.normalizedDifference(['B8', 'B4'])
        ndvi_landsat7 = landsat7.normalizedDifference(['B4', 'B3'])

        combined_ndvi = ee.Image.cat([ndvi_sentinel2, ndvi_landsat7])

    elif sentinel2.size().getInfo():

        sentinel2 = sentinel2.mosaic()

        ndvi_sentinel2 = sentinel2.normalizedDifference(['B8', 'B4'])

        combined_ndvi = ndvi_sentinel2

    elif landsat7.size().getInfo():

        landsat7 = ee.Algorithms.Landsat.simpleComposite(landsat7)

        ndvi_landsat7 = landsat7.normalizedDifference(['B4', 'B3'])

        combined_ndvi = ndvi_landsat7

    elif landsat8.size().getInfo():

        landsat8 = ee.Algorithms.Landsat.simpleComposite(landsat8)

        ndvi_landsat8 = landsat8.normalizedDifference(['B5', 'B4'])

        combined_ndvi = ndvi_landsat8

    else:

        return None
    
    clippedNDVI = combined_ndvi.clipToCollection(winterWheatFC)

    mean_ndvi = clippedNDVI.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=winterWheatFC,
        scale=30
    ).getInfo().get('nd')

    return mean_ndvi
    