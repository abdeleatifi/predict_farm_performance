# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_TEXTURE-CLASS_USDA-TT_M_v02
# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_ORGANIC-CARBON_USDA-6A1C_M_v02
# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_BULKDENS-FINEEARTH_USDA-4A1H_M_v02
# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_WATERCONTENT-33KPA_USDA-4B1C_M_v01


import ee
from get_ndvi_data import ras_to_vec
import datetime


# collect soil caracteristics using the OpenLandMap dataset
def get_soil_data(df):


    soil_dict = {1 : 'Clay',
                2 : 'Silty clay',
                3 : 'Sandy clay',
                4 : 'Clay loam',
                5 : 'Silty clay loam',
                6 : 'Sandy clay loam',
                7 : 'Loam',
                8 : 'Silt loam',
                9 : 'Sandy loam',
                10 : 'Silt',
                11 : 'Loamy sand',
                12 : 'Sand'}

    df = df.copy()

    start_date = datetime.datetime.strptime(df['Planting_Dates']+'-'+str(df['Year']-1), '%d-%b-%Y')
    har_date = datetime.datetime.strptime(df['Harvesting_Dates']+'-'+str(df['Year']), '%d-%b-%Y')    

    countyBoundary, crop_geometry = ras_to_vec(df['State_ANSI'], df['County_ANSI'], start_date, har_date)


    if not(crop_geometry.size().getInfo()):
        df.loc['soil_water'] = None
        df.loc['soil_carbon'] = None
        df.loc['soil_density'] = None
        df.loc['soil_type'] = None
        return df
        
    # Soil water content (volumetric %) for 33kPa and 1500kPa suctions predicted at 6 standard depths (0, 10, 30, 60, 100 and 200 cm) at 250 m resolution
    soil_water = ee.Image("OpenLandMap/SOL/SOL_WATERCONTENT-33KPA_USDA-4B1C_M/v01")\
                .clip(crop_geometry)\
                .select('b0')
    # Get the soil type image within the AOI
    soil_water = int(soil_water.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=crop_geometry,
        scale=250,
        maxPixels=3e9
    ).get('b0').getInfo())

    # Soil organic carbon content in x 5 g / kg at 6 standard depths (0, 10, 30, 60, 100 and 200 cm) at 250 m resolution
    soil_carbon = ee.Image("OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02")\
                .clip(crop_geometry)\
                .select('b0')
    # Get the soil type image within the AOI
    soil_carbon = int(soil_carbon.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=crop_geometry,
        scale=250,
        maxPixels=3e9
    ).get('b0').getInfo())

    # Soil bulk density (fine earth) 10 x kg / m3 at 6 standard depths (0, 10, 30, 60, 100 and 200 cm) at 250 m resolution.
    soil_density = ee.Image("OpenLandMap/SOL/SOL_BULKDENS-FINEEARTH_USDA-4A1H_M/v02")\
                .clip(crop_geometry)\
                .select('b0')
    # Get the soil type image within the AOI
    soil_density = int(soil_density.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=crop_geometry,
        scale=250,
        maxPixels=3e9
    ).get('b0').getInfo())

    # Soil texture classes (USDA system) for 6 soil depths (0, 10, 30, 60, 100 and 200 cm) at 250 m
    soil_type = ee.Image('OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02')\
                .clip(crop_geometry)\
                .select('b0')
    # Get the soil type image within the AOI
    soil_type = int(soil_type.reduceRegion(
        reducer=ee.Reducer.mode(),
        geometry=crop_geometry,
        scale=250,
        maxPixels=3e9
    ).get('b0').getInfo())

    df.loc['soil_water'] = soil_water # in %
    df.loc['soil_carbon'] = soil_carbon / 5 # in g/Kg
    df.loc['soil_density'] = soil_density * 10 # in kg/m3
    df.loc['soil_type'] = soil_dict[soil_type] # soil class name

    return df