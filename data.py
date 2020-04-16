from bs4 import BeautifulSoup  # Include BS web scraping module
import requests
import git
import pandas as pd
import numpy as np

git.cmd.Git("./public_data/COVID-19").pull()
git.cmd.Git("./public_data/covid-19-data").pull()

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

# Read time_series covid19
global_confirmed_ts = pd.read_csv("public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
global_confirmed_ts_long = global_confirmed_ts.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_name='Cases', var_name='Date')
global_confirmed_ts_long['Province/State'].fillna('', inplace = True)

global_recovered_ts = pd.read_csv("public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
global_recovered_ts_long = global_recovered_ts.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_name='Cases', var_name='Date')
global_recovered_ts_long['Province/State'].fillna('', inplace = True)

global_deaths_ts = pd.read_csv("public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
global_deaths_ts_long = global_deaths_ts.melt(id_vars=['Country/Region', 'Country/Region', 'Lat', 'Long'], value_name='Cases', var_name='Date')
global_deaths_ts_long['Province/State'].fillna('', inplace = True)

##Merge Data Frames Together
gcr = pd.merge(global_confirmed_ts_long, global_recovered_ts_long, how='left', on=['Country/Region', 'Country/Region','Date'])
global_confirmed_ts_long.shape == gcr.shape



caribbean_nations = ['Antigua and Barbuda','Bahamas','Trinidad and Tobago', 'Jamaica','Barbados', 'Saint Kitts and Nevis','Saint Vincent and the Grenadines','Saint Lucia' ]
confirmed_caribbean = global_confirmed_ts_long[global_confirmed_ts_long['Country/Region'].isin(caribbean_nations)]

import seaborn as sns
import matplotlib.pyplot as plt

sns.lineplot(x="Date", y="Cases", hue="Country/Region",
                  estimator=None,
                  data = confirmed_caribbean)
plt.show()

confirmed_caribbean.plot(x='Date', y='Cases')