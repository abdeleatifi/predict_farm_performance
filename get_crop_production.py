import pandas as pd
import yaml
import pcse
from pcse.models import Wofost72_PP
from pcse.base import ParameterProvider
from pcse.db import NASAPowerWeatherDataProvider
from pcse.fileinput import YAMLCropDataProvider
from pcse.util import WOFOST72SiteDataProvider, DummySoilDataProvider


# using the pcse model you can estimate the production of the crop
def get_prod(agrom):

    agro_yaml = """
    - {start}:
        CropCalendar:
            crop_name: {cname}
            variety_name: {vname}
            crop_start_date: {startdate}
            crop_start_type: emergence
            crop_end_date: {enddate}
            crop_end_type: harvest
            max_duration: {maxdur}
        TimedEvents: null
        StateEvents: null
    """.format(cname=agrom["crop_name"], vname=agrom["variety_name"], 
            start=agrom["campaign_start_date"], startdate=agrom["emergence_date"], 
            enddate=agrom["harvest_date"], maxdur=agrom["max_duration"])
    agro = yaml.safe_load(agro_yaml)

    # Weather data for Netherlands
    wdp = NASAPowerWeatherDataProvider(latitude=agrom["latitude"], longitude=agrom["longitude"])

    # Parameter sets for crop, soil and site
    # Standard crop parameter library
    cropd = YAMLCropDataProvider()
    # We don't need soil for potential production, so we use dummy values
    soild = DummySoilDataProvider()
    # Some site parameters
    sited = WOFOST72SiteDataProvider(WAV=50)

    # Retrieve all parameters in the form of a single object. 
    # In order to see all parameters for the selected crop already, we
    # synchronise data provider cropd with the crop/variety: 
    firstkey = list(agro[0])[0]
    cropcalendar = agro[0][firstkey]['CropCalendar'] 
    cropd.set_active_crop(cropcalendar['crop_name'], cropcalendar['variety_name'])
    params = ParameterProvider(cropdata=cropd, sitedata=sited, soildata=soild)

    wofost = Wofost72_PP(params, wdp, agro)
    wofost.run_till_terminate()

    df_results = pd.DataFrame(wofost.get_summary_output())

    return df_results