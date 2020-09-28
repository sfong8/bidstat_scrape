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

for i in range(1,10):

    driver.execute_script("window.scrollTo(0, 0.2*document.body.scrollHeight);")

    #WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "action_wait")))
    time.sleep(2)
    # if  'Mon 21 Sep 2020' in Divs:
    #     print ('end')
    #     break
    # else:
    #     continue
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
x=True
j = 2
i = 1
master_df = pd.DataFrame()
from selenium.common.exceptions import NoSuchElementException
while x:
    try:
        if driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]/h2[{i}]').text == seven_days_ago:
            print('end')
            break

        table = driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]')
        table_html = table.get_attribute('innerHTML')

        df = read_html(table_html)[i-1]
        df['DATE']=driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]/h2[{i}]').text
        i+=1

    except NoSuchElementException:
        j+=1
        if i!=1:
            i=1
        table = driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]')
        df = read_html(table_html)[i-1]
        df['DATE'] = driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]/h2[{i}]').text
    master_df=pd.concat([df,master_df])
