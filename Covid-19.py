#from sklearn.metrics import mean_squared_error
import pandas as pd
import io
import requests
import datetime as datetime
import matplotlib.pyplot as plt
from functools import reduce


# bring data from Novel Coronavirus (COVID-19) Cases, provided by Johns Hopkins University CSSE 
# https://github.com/CSSEGISandData/COVID-19

# confirmed cases dataframe
#col = ['Province/State','Country/Region','Lat','Long','1/22/20','1/23/20','1/24/20','1/25/20','1/26/20','1/27/20','1/28/20','1/29/20','1/30/20','1/31/20','2/1/20','2/2/20','2/3/20','2/4/20','2/5/20','2/6/20','2/7/20','2/8/20','2/9/20','2/10/20','2/11/20','2/12/20','2/13/20','2/14/20','2/15/20','2/16/20','2/17/20','2/18/20','2/19/20','2/20/20','2/21/20','2/22/20','2/23/20','2/24/20','2/25/20','2/26/20','2/27/20','2/28/20','2/29/20','3/1/20','3/2/20','3/3/20','3/4/20','3/5/20','3/6/20','3/7/20','3/8/20','3/9/20','3/10/20','3/11/20','3/12/20','3/13/20','3/14/20','3/15/20','3/16/20','3/17/20','3/18/20','3/19/20','3/20/20','3/21/20','3/22/20','3/23/20','3/24/20','3/25/20']
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
confirmed = pd.read_csv(url,error_bad_lines=False)

# deceased cases dataframe
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
death = pd.read_csv(url, error_bad_lines=False)

# recovered cases dataframe
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
recover = pd.read_csv(url, error_bad_lines=False)

# fix region names 
def assign_country_code(df,country,country_code):
  df['Country/Region'] = df['Country/Region'].str.replace(country,country_code)


assign_country_code(confirmed,"United Kingdom", "GB")
assign_country_code(death,"United Kingdom", "GB")
assign_country_code(recover,"United Kingdom", "GB")
assign_country_code(confirmed,"Korea, South", "KR")
assign_country_code(death,"Korea, South", "KR")
assign_country_code(recover,"Korea, South", "KR")

def clean_df(df):
  if 'Lat' in df.columns:
    df = df.drop(['Province/State', 'Lat', 'Long',], axis=1)
  else:
    df = df.drop(['Province/State'], axis=1)
  df = df.groupby(['Country/Region'], as_index=False).sum()
  df = df.rename(columns={'Country/Region': 'Country'})
  return df

confirmed = clean_df(confirmed)
death = clean_df(death)
recover = clean_df(recover)

# Check the dates of the latest JHU CSSE data
confirmed.columns[-1:]

# read population data for each province. China is divided into region whereas other regions of the world is nation 
population=pd.read_csv('https://raw.githubusercontent.com/Rank23/COVID19/master/population.csv', sep=',', encoding='latin1')
population = clean_df(population)

def merge_covid_pop(covid_df,pop_df):
  covid_df = pd.merge(covid_df, pop_df,how='left' ,on=['Country'])
  return covid_df

confirmed=merge_covid_pop(confirmed,population)
death=merge_covid_pop(death,population)
recover=merge_covid_pop(recover,population)

Top10_Korea = ['US','GB','Germany','China','Sweden','Netherlands','Spain','France','Canada','Italy','KR']

def filter_top_11(covid_df,country_list):
  covid_df = covid_df[covid_df.Country.isin(Top10_Korea)]
  return covid_df

confirmed = filter_top_11(confirmed,Top10_Korea)
death = filter_top_11(death,Top10_Korea)
recover = filter_top_11(recover,Top10_Korea)

# create timeseries dataframe for all infected regions
def create_ts(df):
  ts=df
  ts=ts.drop([' Population '], axis=1)
  ts.set_index('Country')
  ts=ts.T
  ts.columns=ts.loc['Country']
  ts=ts.drop('Country')
  ts=ts.fillna(0)
  ts=ts.reindex(sorted(ts.columns), axis=1)
  return (ts)

# confirmed case dataframe
ts=create_ts(confirmed)

# deceased case dataframe
ts_d=create_ts(death)

# recovered case dataframe
ts_rec=create_ts(recover)

# check recent 5 days of confirmed cases according to countries
row = ts.shape[0]
#print(ts.columns)
#print(confirmed.columns)

def calculate_diff(country,country_code,ts_df):
  country_df = ts_df[[country]]
  country_df.columns = ['Confirmed']
  country_df['diff'] = country_df['Confirmed'].diff()
  country_df['diff'].fillna(0, inplace=True)
  country_df['Date'] = country_df.index
  country_df['Country'] = [country_code]*row
  return country_df

CA = calculate_diff('Canada','CA',ts)
CN = calculate_diff('China','CN',ts)
FR = calculate_diff('France','FR',ts)
DE = calculate_diff('Germany','DE',ts)
IT = calculate_diff('Italy','IT',ts)
NL = calculate_diff('Netherlands','NL',ts)
SE = calculate_diff('Sweden','SE',ts)
ES = calculate_diff('Spain','ES',ts)
US = calculate_diff('US','US',ts)
KR = calculate_diff('KR','KR',ts)
GB = calculate_diff('GB','GB',ts)

f_ts = pd.concat([CA,CN,FR,ES,IT,NL,US,GB,KR,SE,DE])

f_ts['Date'] = pd.to_datetime(f_ts['Date'])

#print(f_ts.head())

f_ts.to_csv('/Volumes/GoogleDrive/My Drive/Covid/Total_COVID_confirmed.csv',index=False) 
#ts_d.to_csv('/Volumes/GoogleDrive/My Drive/Covid/Total_COVID_deceased{}.csv'.format(datetime.datetime.now().strftime("%Y%m%d")))
#ts_rec.to_csv('/Volumes/GoogleDrive/My Drive/Covid/Total_COVID_recovered{}.csv'.format(datetime.datetime.now().strftime("%Y%m%d")))

# sort regions with number of confirmed casses largest to smallest.
#p=ts.reindex(ts.max().sort_values(ascending=False).index, axis=1)
#p_r=ts_rec.reindex(ts.mean().sort_values(ascending=False).index, axis=1)
#p_d=ts_d.reindex(ts.mean().sort_values(ascending=False).index, axis=1)

# plot graph Daily Total - Top 10 countries
ts.iloc[:,:11].plot(marker='*',figsize=(14,14)).set_title('Daily Total Confirmed - Top 10 confirmed countries',fontdict={'fontsize': 22})
#plt.show()
#p_r.iloc[:,:11].plot(marker='*',figsize=(10,4)).set_title('Daily Total Recoverd - Top 10 confirmed countries',fontdict={'fontsize': 22})
#plt.show()
#p_d.iloc[:,:11].plot(marker='*',figsize=(10,4)).set_title('Daily Total Recoverd - Top 10 confirmed countrie',fontdict={'fontsize': 22})
#plt.show()
