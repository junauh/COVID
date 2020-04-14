import datetime as datetime
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import glob, os


from selenium.webdriver.chrome.options import Options
today = datetime.datetime.now().strftime("%m/%d/%Y")

trends_url = 'https://trends.google.com/trends/story/US_cu_p8y_23ABAABolM_en' 

def download_data(url):
  chrome_options = Options()
  chrome_options.add_argument("user-data-dir=selenium") 
  browser = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
  browser.get(url)
  browser.maximize_window()

  element = browser.find_element_by_xpath('/html/body/div[2]/div[2]/md-content/div/div/div[1]')
  element.screenshot("/Users/junyoung.auh/Desktop/Corona/test.png")
  browser.quit()

download_data(trends_url)

#end_of_day_df.to_csv('/Volumes/GoogleDrive/My Drive/Covid/IndexEndofday.csv'.) 
