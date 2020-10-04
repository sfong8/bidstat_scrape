import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime
import time

from selenium.webdriver.chrome.options import Options

url = r'http://bidstats.uk/tenders/?ntype=award&value=high'



from pandas.io.html import read_html
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
driver = webdriver.Chrome(r'D:\Chrome Download\chromedriver_win32\chromedriver',   chrome_options=chrome_options)
driver.get(url)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import date,timedelta
from website_scraper import scapePage
import calendar
seven_days_ago = date.today()- timedelta(days=7)
seven_days_ago=seven_days_ago.strftime('%a %d %b %Y' )
WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/section/div[1]/ul/li[3]"))).click()
from selenium.webdriver.common.keys import Keys
elems = driver.find_elements_by_xpath("//a[@href]")
master_df = pd.DataFrame()
track_refs=[]
total_height = 10*int(driver.execute_script("return document.body.scrollHeight"))
from tqdm import tqdm
for i in range(1, total_height, 300):
    if driver.execute_script("return document.body.scrollHeight")==0:
        break
    else:
        driver.execute_script("window.scrollTo(0, {});".format(i))
        #time.sleep(5)
        #driver.execute_script("window.scrollTo(0, 0.5*document.body.scrollHeight);")
        elements = driver.find_elements_by_xpath("//table[@class = 'nl-table']//td[2]/a")
        for element in tqdm(elements):
            if str(element.get_attribute("href")) in track_refs:
                z = 0
            else:

                x = scapePage(str(element.get_attribute("href")))
                master_df = pd.concat([x, master_df])
                track_refs.append(str(element.get_attribute("href")))

# for i in range(1,5):
#
#     driver.execute_script("window.scrollTo(0, 0.5*document.body.scrollHeight);")
#
#     #WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "action_wait")))
#     time.sleep(5)
#     # if  'Mon 21 Sep 2020' in Divs:
#     #     print ('end')
#     #     break
#     # else:
#     #     continue
from datetime import datetime
now = datetime.now()
now2=now.strftime("%Y%m%d_%H_%M_%S")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

master_df.to_csv(fr'scraped_bidstat_{now2}.csv',index=None)
    #     if driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]/h2[{i}]').text == seven_days_ago:
    #         print('end')
    #         break
    #
    #     table = driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]')
    #     table_html = table.get_attribute('innerHTML')
    #
    #     df = read_html(table_html)[i-1]
    #     df['DATE']=driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]/h2[{i}]').text
    #     i+=1
    #
    # except NoSuchElementException:
    #     j+=1
    #     if i!=1:
    #         i=1
    #     table = driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]')
    #     df = read_html(table_html)[i-1]
    #     df['DATE'] = driver.find_element_by_xpath(fr'/html/body/div[1]/section/div[{j}]/h2[{i}]').text
    # master_df=pd.concat([df,master_df])
