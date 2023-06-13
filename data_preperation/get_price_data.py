from bs4 import BeautifulSoup
import requests
import re


def get_price_data(df):

    df = df.copy()
    
    # Make a GET request to the webpage
    url = "https://www.macrotrends.net/2534/wheat-prices-historical-chart-data"
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    table_tag = soup.find('table' , class_= "table")
    tbody_tag = table_tag.find("tbody")
    # Iterate over the rows of the table
    for row in tbody_tag.find_all("tr"):

        first_cell = row.find("td").text.strip()

        if first_cell == str(df['Year']):
            df.loc['average_price'] = float(re.sub(r'[^0-9.]', '', row.find_all("td")[1].text.strip())) # in dollars $
            df.loc['year_open'] = float(re.sub(r'[^0-9.]', '', row.find_all("td")[2].text.strip())) # in dollars $
            df.loc['year_high'] = float(re.sub(r'[^0-9.]', '', row.find_all("td")[3].text.strip())) # in dollars $
            df.loc['year_low'] = float(re.sub(r'[^0-9.]', '', row.find_all("td")[4].text.strip())) # in dollars $
            df.loc['year_close'] = float(re.sub(r'[^0-9.]', '', row.find_all("td")[5].text.strip())) # in dollars $
            

    return df
