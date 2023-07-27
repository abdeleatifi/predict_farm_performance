import ee

# Initialize Earth Engine
ee.Initialize()


# simple function calculates the size of the geometry variable(land)
def get_land_area(geometry):

    geometry = geometry.geometry()

    # Create an EE geometry object
    ee_geometry = ee.Geometry(geometry)

    # Create an area reducer and calculate the area
    area = ee.Number(ee_geometry.area())

    # Convert area to square kilo meters and return the result
    area_sq_m = area.divide(1e6).getInfo()  # Convert to square kilo meters

    return area_sq_m * 100 # in Hectare