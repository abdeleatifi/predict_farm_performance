from bs4 import BeautifulSoup
import requests
import re

def get_latest_price():

    # Make a GET request to the webpage
    url = "https://www.macrotrends.net/2534/"
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


def get_year_price(year):
    
    # Make a GET request to the webpage
    url = "https://www.macrotrends.net/2534/"
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    table_tag = soup.find('table' , class_= "table")
    tbody_tag = table_tag.find("tbody")

    # Iterate over the rows of the table
    for row in tbody_tag.find_all("tr"):

        first_cell = row.find("td").text.strip()

        if first_cell == str(year):         

            price_data = {'average_price' : float(re.sub(r'[^0-9.]', '', row.find_all("td")[1].text.strip())), # in dollars $
                            'year_open' : float(re.sub(r'[^0-9.]', '', row.find_all("td")[2].text.strip())),
                            'year_high' : float(re.sub(r'[^0-9.]', '', row.find_all("td")[3].text.strip())),
                            'year_low' : float(re.sub(r'[^0-9.]', '', row.find_all("td")[4].text.strip())),
                            'year_close' : float(re.sub(r'[^0-9.]', '', row.find_all("td")[5].text.strip()))}
            break

    return price_data

