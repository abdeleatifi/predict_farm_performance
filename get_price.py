from bs4 import BeautifulSoup
import requests
import re

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