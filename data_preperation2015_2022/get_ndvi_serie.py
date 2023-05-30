from ras_to_vec import ras_to_vec
from retrieve_mean_ndvi import retrieve_mean_ndvi
import datetime
import ee

def get_ndvi_serie(df):

    try:
        ee.Initialize()
    except:
        ee.Authenticate()
        ee.Initialize()

    df = df.copy()

    countyBoundary, winterWheatFC = ras_to_vec(df['State ANSI'], df['County'], df['Year'])
    
    year = df['Year']

    start_date = datetime.datetime(year-1, 8, 20)

    while start_date <= datetime.datetime(year, 8, 20):

        end_date = start_date + datetime.timedelta(weeks=2) - datetime.timedelta(days=1)

        mean_ndvi = retrieve_mean_ndvi(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), countyBoundary, winterWheatFC)
        
        df.loc[start_date.strftime('%m-%d')] = mean_ndvi

        start_date = end_date + datetime.timedelta(days=1)
    
    ee.Reset()
    
    return df
