import git
import pandas as pd

#git.Git("./public_data").clone("https://github.com/CSSEGISandData/COVID-19.git")
#git.Git("./public_data").clone("https://github.com/nytimes/covid-19-data.git")

git.cmd.Git("./public_data/COVID-19").pull()
git.cmd.Git("./public_data/covid-19-data").pull()

# Read time_series covid19
global_confirmed_ts = pd.read_csv("public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
global_recovered_ts = pd.read_csv("public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
global_deaths_ts = pd.read_csv("public_data/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
