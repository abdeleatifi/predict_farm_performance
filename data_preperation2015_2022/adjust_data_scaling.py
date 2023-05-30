from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def adjust_data_scaling(df):

    # Define the columns to be scaled
    ndvi_columns = ['ndvi_1', 'ndvi_2', ..., 'ndvi_27']
    land_area_column = ['land_area']

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
