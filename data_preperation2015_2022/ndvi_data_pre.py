import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# the df must be full of just ndvi values, 
# step 1: slice it before feed it to this function
def ndvi_data_pre(df):

    # Step 2: Check for empty rows and drop them
    ndviserie_clean = df.dropna(how='all')

    # Step 3: Perform machine learning-based imputation
    imputer = IterativeImputer()
    ndviserie_imputed = pd.DataFrame(imputer.fit_transform(ndviserie_clean), columns=ndviserie_clean.columns)

    return ndviserie_imputed