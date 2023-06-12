import datetime
import ee


def get_ndvi_serie(df):

    df = df.copy()

    start_date = datetime.datetime.strptime(df['Planting_Dates']+'-'+str(df['Year']-1), '%d-%b-%Y')
    har_date = datetime.datetime.strptime(df['Harvesting_Dates']+'-'+str(df['Year']), '%d-%b-%Y')

    countyBoundary, winterWheatFC = ras_to_vec(df['State_ANSI'], df['County_ANSI'], start_date, har_date)

    time_stamp = (har_date - start_date)/14
    s=0

    while start_date <= har_date:

        end_date = start_date + time_stamp - datetime.timedelta(days=1)

        mean_ndvi = retrieve_mean_ndvi(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), countyBoundary, winterWheatFC)
        s+=1
        df.loc['NDVI'+str(s)] = mean_ndvi

        start_date = end_date + datetime.timedelta(days=1)
    
    
    return df


def retrieve_mean_ndvi(start_date, end_date, countyBoundary, winterWheatFC): 
    
    if not(winterWheatFC.size().getInfo()):
        return None

    sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(countyBoundary) \
            .filterDate(start_date, end_date) 
        
    landsat8 = ee.ImageCollection('LANDSAT/LC08/C02/T1')\
            .filterBounds(countyBoundary) \
            .filterDate(start_date, end_date)
    
    landsat7 = ee.ImageCollection('LANDSAT/LE07/C02/T1')\
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

    elif landsat7.size().getInfo():

        landsat7 = ee.Algorithms.Landsat.simpleComposite(landsat7)

        combined_ndvi = landsat7.normalizedDifference(['B4', 'B3'])

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


def ras_to_vec(state, county, start_date, end_date):

    try:
        ee.Initialize()
    except:
        ee.Authenticate()
        ee.Initialize()
    
    state = str(state).zfill(2)
    county = str(county).zfill(3)

    # Define the boundary of Thomas County, Kansas
    countyBoundary = ee.FeatureCollection('TIGER/2018/Counties') \
        .filter(ee.Filter.eq("STATEFP", state)) \
        .filter(ee.Filter.eq("COUNTYFP", county))

    # Load the CropScape data for the year 2022
    cropscape = ee.ImageCollection('USDA/NASS/CDL') \
        .filter(ee.Filter.date(start_date, end_date)) \
        .first()

    # Select winter wheat (crop code: 3) from the CropScape data
    winterWheat = cropscape.select('cropland') \
        .eq(24) \
        .selfMask()

    # Clip the winter wheat layer to Thomas County boundary
    winterWheatClip = winterWheat.clip(countyBoundary)
    
    # Convert the clipped layer to a FeatureCollection
    winterWheatFC = winterWheatClip.reduceToVectors(
        geometry=countyBoundary,
        scale=30,
        geometryType='polygon',
        eightConnected=False,
        labelProperty='class',
        maxPixels= 1e9
    )

    return countyBoundary, winterWheatFC