import requests
import datetime as datetime
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt

import schedule
import pandas as pd
import glob, os
#End of day index 'https://www.investing.com/indices/major-indices'
#Market_Indices = ['S&P 500','FTSE 100','DAX','Shanghai','OMXS30','AEX','IBEX 35','CAC 40','S&P/TSX','FTSE MIB','KOSPI']
#need to scrap from 1/22

from selenium.webdriver.chrome.options import Options
today = datetime.datetime.now().strftime("%m/%d/%Y")

SP500_url = 'https://www.investing.com/indices/us-spx-500-historical-data'
FTSE_url = 'https://www.investing.com/indices/uk-100-historical-data'
DAX_url = 'https://www.investing.com/indices/germany-30-historical-data'
Shanghai_url = 'https://www.investing.com/indices/shanghai-composite-historical-data'
OMXS30_url = 'https://www.investing.com/indices/omx-stockholm-30-historical-data'
AEX_url = 'https://www.investing.com/indices/netherlands-25-historical-data'
IBEX35_url = 'https://www.investing.com/indices/spain-35-historical-data'
CAC40_url = 'https://www.investing.com/indices/france-40-historical-data'
SPTSX_url = 'https://www.investing.com/indices/s-p-tsx-composite-historical-data'
FTSEMIB_url = 'https://www.investing.com/indices/it-mib-40-historical-data'
KOSPI_url = 'https://www.investing.com/indices/kospi-historical-data'

def download_data(url):
  chrome_options = Options()
  chrome_options.add_argument("user-data-dir=selenium") 
  browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)
  browser.get(url)

  time.sleep(10)
  #browser.find_element_by_xpath('//*[@id="column-content"]/div[4]/div/a').click()

  #login(browser)
  
  #time.sleep(5)

  date_box = browser.find_element_by_id('widgetFieldDateRange')
  date_box.click()

  startDate = browser.find_element_by_id('startDate')
  startDate.clear()
  startDate.send_keys('01/22/2020')

  endDate = browser.find_element_by_id('endDate')
  endDate.clear()
  endDate.send_keys(today)

  browser.find_element_by_id('applyBtn').click()
  
  time.sleep(5)

  browser.find_element_by_xpath('//*[@id="column-content"]/div[4]/div/a').click()
  #browser.find_element_by_class_name('newBtn LightGray downloadBlueIcon js-download-data').click()

  time.sleep(5)

  browser.quit()

  time.sleep(5)

def login(browser):
  email = browser.find_element_by_id("loginFormUser_email")
  password = browser.find_element_by_id("loginForm_password")

  email.send_keys('nil.nicklas@gmail.com')
  password.send_keys('kaffekopp1234')

  browser.find_element_by_xpath('//*[@id="signup"]/a').click()


download_data(KOSPI_url)

li = []

os.chdir('/Users/junyoung.auh/Downloads/')
for filename in glob.glob("*.csv"):
  try:
    df = pd.read_csv(filename, index_col=None, header=0, sep=',')
  except pd.errors.EmptyDataError:
    continue
  filepath = str(filename).split('/')[-1]
  index_name = filepath.split(' ')[0:2]
  f_index_name = ''.join(index_name)
  df['Index'] = f_index_name
  li.append(df)

end_of_day_df = pd.concat(li, axis=0, ignore_index=True)
#print(end_of_day_df.columns)
end_of_day_df = end_of_day_df[['Index','Date','Price']]
end_of_day_df.columns = ['Country','Date','Index']

#Market_Indices = ['S&P 500','FTSE 100','DAX','Shanghai','OMXS30','AEX','IBEX 35','CAC 40','S&P/TSX','FTSE MIB','KOSPI']

def replace_string(df,column,index,country_code):
  df[column] = df[column].str.replace(index,country_code)

replace_string(end_of_day_df,'Country','FTSE100', 'GB')
replace_string(end_of_day_df,'Country','OMXStockholm', 'SE')
replace_string(end_of_day_df,'Country','AEXHistorical', 'NL')
replace_string(end_of_day_df,'Country','DAXHistorical', 'DE')
replace_string(end_of_day_df,'Country','IBEX35', 'ES')
replace_string(end_of_day_df,'Country','S&P_TSXComposite', 'CA')
replace_string(end_of_day_df,'Country','CAC40', 'FR')
replace_string(end_of_day_df,'Country','ShanghaiComposite', 'CN')
replace_string(end_of_day_df,'Country','KOSPIHistorical', 'KR')
replace_string(end_of_day_df,'Country','S&P500', 'US')
replace_string(end_of_day_df,'Country','FTSEMIB', 'IT')
end_of_day_df = end_of_day_df.drop_duplicates(keep='first')
replace_string(end_of_day_df,'Index',',', '')
end_of_day_df['Index']= end_of_day_df['Index'].str.replace(',', '')

#print(end_of_day_df.head())
end_of_day_df['Date'] = pd.to_datetime(end_of_day_df['Date'])

end_of_day_df.to_csv('/Volumes/GoogleDrive/My Drive/Covid/IndexEndofday.csv') 

os.chdir('/Users/junyoung.auh/Downloads/')
for filename in glob.glob("*.csv"):
  os.remove(filename)

#print(type(end_of_day_df['Index'][0]))



# plot graph Daily Total - Top 10 countries
end_of_day_df.plot(x='Date',y='Index', kind = 'line')
#plt.show()