#from sklearn.metrics import mean_squared_error
import pandas as pd
import io
import requests
import datetime as datetime
import matplotlib.pyplot as plt


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
confirmed['Country/Region']= confirmed['Country/Region'].str.replace("United Kingdom", "GB")
death['Country/Region']= death['Country/Region'].str.replace("United Kingdom", "GB")
recover['Country/Region']= recover['Country/Region'].str.replace("United Kingdom", "GB")
confirmed['Country/Region']= confirmed['Country/Region'].str.replace("Korea, South", "KR")
death['Country/Region']= death['Country/Region'].str.replace("Korea, South", "KR")
recover['Country/Region']= recover['Country/Region'].str.replace("Korea, South", "KR")

confirmed=confirmed.drop(['Province/State', 'Lat', 'Long'], axis=1)
confirmed = confirmed.groupby(['Country/Region'], as_index=False).sum()
confirmed = confirmed.rename(columns={'Country/Region': 'Country'})
death=death.drop(['Province/State', 'Lat', 'Long'], axis=1)
death = death.groupby(['Country/Region'], as_index=False).sum()
death = death.rename(columns={'Country/Region': 'Country'})
recover=recover.drop(['Province/State', 'Lat', 'Long'], axis=1)
recover = recover.groupby(['Country/Region'], as_index=False).sum()
recover = recover.rename(columns={'Country/Region': 'Country'})

# Check the dates of the latest JHU CSSE data
confirmed.columns[-1:]

# read population data for each province. China is divided into region whereas other regions of the world is nation 
population=pd.read_csv('https://raw.githubusercontent.com/Rank23/COVID19/master/population.csv', sep=',', encoding='latin1')
population=population.drop(['Province/State'], axis=1)
population = population.groupby(['Country/Region'], as_index=False).sum() 
population = population.rename(columns={'Country/Region': 'Country'})
population.head()

confirmed=pd.merge(confirmed, population,how='left' ,on=['Country'])
death=pd.merge(death, population,how='left' ,on=['Country'])
recover=pd.merge(recover, population,how='left' ,on=['Country'])

Volvo_Top10_Korea = ['US','GB','Germany','China','Sweden','Netherlands','Spain','France','Canada','Italy','KR']
confirmed = confirmed[confirmed.Country.isin(Volvo_Top10_Korea)]
death = death[death.Country.isin(Volvo_Top10_Korea)]
recover = recover[recover.Country.isin(Volvo_Top10_Korea)]

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
print(ts.columns)
#print(confirmed.columns)
CA = ts[['Canada']]
CA.columns = ['Confirmed']
CA['diff'] = CA['Confirmed'].diff()
CA['diff'].fillna(0, inplace=True)
CA['Date'] = CA.index
CA['Country'] = ['CA']*row

CN = ts[['China']]
CN.columns = ['Confirmed']
CN['diff'] = CN['Confirmed'].diff()
CN['diff'].fillna(0, inplace=True)
CN['Date'] = CN.index
CN['Country'] = ['CN']*row

FR = ts[['France']]
FR.columns = ['Confirmed']
FR['diff'] = FR['Confirmed'].diff()
FR['diff'].fillna(0, inplace=True)
FR['Date'] = FR.index
FR['Country'] = ['FR']*row

DE = ts[['Germany']]
DE.columns = ['Confirmed']
DE['diff'] = DE['Confirmed'].diff()
DE['diff'].fillna(0, inplace=True)
DE['Date'] = DE.index
DE['Country'] = ['DE']*row

IT = ts[['Italy']]
IT.columns = ['Confirmed']
IT['diff'] = IT['Confirmed'].diff()
IT['diff'].fillna(0, inplace=True)
IT['Date'] = IT.index
IT['Country'] = ['IT']*row

NL = ts[['Netherlands']]
NL.columns = ['Confirmed']
NL['diff'] = NL['Confirmed'].diff()
NL['diff'].fillna(0, inplace=True)
NL['Date'] = NL.index
NL['Country'] = ['NL']*row

ES = ts[['Spain']]
ES.columns = ['Confirmed']
ES['diff'] = ES['Confirmed'].diff()
ES['diff'].fillna(0, inplace=True)
ES['Date'] = ES.index
ES['Country'] = ['ES']*row

SE = ts[['Sweden']]
SE.columns = ['Confirmed']
SE['diff'] = SE['Confirmed'].diff()
SE['diff'].fillna(0, inplace=True)
SE['Date'] = SE.index
SE['Country'] = ['SE']*row

US = ts[['US']]
US.columns = ['Confirmed']
US['diff'] = US['Confirmed'].diff()
US['diff'].fillna(0, inplace=True)
US['Date'] = NL.index
US['Country'] = ['US']*row

KR = ts[['KR']]
KR.columns = ['Confirmed']
KR['diff'] = KR['Confirmed'].diff()
KR['diff'].fillna(0, inplace=True)
KR['Date'] = KR.index
KR['Country'] = ['KR']*row

GB = ts[['GB']]
GB.columns = ['Confirmed']
GB['diff'] = GB['Confirmed'].diff()
GB['diff'].fillna(0, inplace=True)
GB['Date'] = GB.index
GB['Country'] = ['GB']*row

f_ts = pd.concat([CA,CN,FR,ES,IT,NL,US,GB,KR,SE,DE])

f_ts['Date'] = pd.to_datetime(f_ts['Date'])

print(f_ts.head())

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
