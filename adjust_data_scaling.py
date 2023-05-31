from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def adjust_data_scaling(df):

    # Define the columns to be scaled
    ndvi_columns = ['08-20','09-03','09-17','10-01','10-15','10-29','11-12','11-26','12-10','12-24','01-07','01-21','02-04','02-18','03-04','03-18','04-01','04-15','04-29','05-13','05-27','06-10','06-24','07-08','07-22','08-05','08-19']
    land_area_column = ['Hectare Planted']

    # Create separate transformers for NDVI scaling and land area scaling
    ndvi_transformer = MinMaxScaler()
    land_area_transformer = MinMaxScaler()

    # Create the column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('ndvi', ndvi_transformer, ndvi_columns),
            ('land_area', land_area_transformer, land_area_column)
        ])

    # Fit and transform the data
    scaled_data = preprocessor.fit_transform(df)

    return scaled_data
