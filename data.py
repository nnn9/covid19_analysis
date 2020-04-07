from bs4 import BeautifulSoup  # Include BS web scraping module
import requests
import git
import pandas as pd
import numpy as np

## Pull Country Data

url = "https://www.worldometers.info/world-population/population-by-country/"
res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
print(res.status_code)
soup = BeautifulSoup(res.text, "html.parser")  # Parses HTTP Response

table_head = soup.findChildren('thead')[0]
column_header = [i.get_text() for i in table_head.findAll('th')]
column_header

table_data = soup.findChildren('tbody')[0]
rows = table_data.findChildren(['th', 'tr'])

country_data = []
for row in rows:
    cells = row.findChildren('td')
    country_data.append([i.string for i in cells])

country_data_df = pd.DataFrame(country_data, columns=column_header)
## Need to clean data frame

country_data_df['Population (2020)'] = country_data_df['Population (2020)'].map(lambda x: int(x.replace(',', '')))
country_data_df['Net Change'] = country_data_df['Net Change'].map(lambda x: int(x.replace(',', '')))

country_data_df['Yearly Change'] = country_data_df['Yearly Change'].map(lambda x: float(x.replace('%', '')))

country_data_df[['Urban Pop %', 'World Share']] = country_data_df[['Urban Pop %', 'World Share']].applymap(lambda x: x.replace('%', ''))
country_data_df[['Urban Pop %', 'World Share']] = country_data_df[['Urban Pop %', 'World Share']].applymap(lambda x: x.replace('N.A.', ''))

## Pull Covid Data

# git.Git("./public_data").clone("https://github.com/CSSEGISandData/COVID-19.git")
# git.Git("./public_data").clone("https://github.com/nytimes/covid-19-data.git")

git.cmd.Git("./public_data/COVID-19").pull()
git.cmd.Git("./public_data/covid-19-data").pull()

# Read time_series covid19
global_confirmed_ts = pd.read_csv(
    "public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
global_recovered_ts = pd.read_csv(
    "public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
global_deaths_ts = pd.read_csv(
    "public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
