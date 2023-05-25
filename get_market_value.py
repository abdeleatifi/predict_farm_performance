import pandas as pd
import yaml
import pcse
from pcse.models import Wofost72_PP
from pcse.base import ParameterProvider
from pcse.db import NASAPowerWeatherDataProvider
from pcse.fileinput import YAMLCropDataProvider
from pcse.util import WOFOST72SiteDataProvider, DummySoilDataProvider

from bs4 import BeautifulSoup
import requests
import re


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


def get_price():

    # Make a GET request to the webpage
    url = "https://www.macrotrends.net/2534/wheat-prices-historical-chart-data"
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    div_tag = soup.find('div' , id = "chart_metadata")
    strong_tag = div_tag.find("strong").get_text()

    # Extract float using regex
    float_regex = r"\d+\.\d+"
    matches = re.findall(float_regex, strong_tag)

    # Convert matched float string to float value
    if matches:
        wheat_prica = float(matches[0])/27.216

    return wheat_prica


def get_market_value(agrom):
    market_value = get_prod(agrom).iloc[0,2] * get_price() * agrom['crop_area']
    return market_value

