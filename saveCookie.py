from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium") 
driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

driver.get('https://www.investing.com/indices/us-spx-500-historical-data')