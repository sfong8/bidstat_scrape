
import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime
import time

url = r'http://bidstats.uk/tenders/?ntype=award&value=high'



from pandas.io.html import read_html
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
driver = webdriver.Chrome(r'D:\Chrome Download\chromedriver_win32\chromedriver')
driver.get(url)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date,timedelta
import calendar
seven_days_ago = date.today()- timedelta(days=7)
seven_days_ago=seven_days_ago.strftime('%a %d %b %Y' )
WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/ul/li[3]"))).click()
from selenium.webdriver.common.keys import Keys
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    print(elem.get_attribute("href"))
    j=2
elements = driver.find_elements_by_xpath("//table[@class = 'nl-table']//td[2]/a")
# elements = driver.find_elements_by_xpath("//table[@class = 'nl-table']//td[@class = nlt-title]/a")
for element in elements:
    print(element.get_attribute("href"))


