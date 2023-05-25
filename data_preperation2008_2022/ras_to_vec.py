import ee

def ras_to_vec(state, county, year):
    
    state = str(state)
    year = str(year)
    county = county.capitalize()

    if len(state) == 1:
        state = '0'+state

    # Define the boundary of Thomas County, Kansas
    countyBoundary = ee.FeatureCollection('TIGER/2018/Counties') \
        .filter(ee.Filter.eq('STATEFP', state)) \
        .filter(ee.Filter.eq('NAME', county))

    start = year+'-01-01'
    end = year+'-12-31'
    # Load the CropScape data for the year 2022
    cropscape = ee.ImageCollection('USDA/NASS/CDL') \
        .filter(ee.Filter.date(start, end)) \
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
        labelProperty='class'
    )

    return countyBoundary, winterWheatFC