# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_TEXTURE-CLASS_USDA-TT_M_v02
# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_ORGANIC-CARBON_USDA-6A1C_M_v02
# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_BULKDENS-FINEEARTH_USDA-4A1H_M_v02
# https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_WATERCONTENT-33KPA_USDA-4B1C_M_v01
import ee

# get soil data for a new datapoint
def get_soil_data(crop_geometry):


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


    if not(crop_geometry.size().getInfo()):
        soil_data = {'soil_water' : None,
            'soil_carbon' : None,
            'soil_density' : None,
            'soil_type' : None}
        return soil_data
        
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

    soil_data = {'soil_water' : soil_water,     # in %
                'soil_carbon' : soil_carbon,    # in g/Kg
                'soil_density' : soil_density,  # in kg/m3
                'soil_type' : soil_dict[soil_type]} # soil class name

    return soil_data