import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def ndvi_data_pre(df):

    # Step 1: Slice the last 27 columns
    ndviserie_sliced = df.iloc[:, -27:]

    # Step 2: Check for empty rows and drop them
    ndviserie_clean = ndviserie_sliced.dropna(how='all')

    # Step 3: Perform machine learning-based imputation
    imputer = IterativeImputer()
    ndviserie_imputed = pd.DataFrame(imputer.fit_transform(ndviserie_clean), columns=ndviserie_clean.columns)

    return ndviserie_imputed