

import pandas as pd
from datetime import datetime
from selenium import webdriver

def scapePage(url):
    driver = webdriver.Chrome(r'D:\Chrome Download\chromedriver_win32\chromedriver')
    driver.get(url)
    sector = driver.find_element_by_xpath("/html/body/div/article/section[1]/div[2]/dl/dd[1]/a").text
    source = driver.find_element_by_xpath("/html/body/div/article/section[1]/div[1]/dl/dd[1]").text
    buyer = driver.find_element_by_xpath("/html/body/div/article/div/section[1]/ul/li/a").text
    date = driver.find_element_by_xpath("/html/body/div/article/section[1]/div[2]/dl/dd[2]").text
    date2 = datetime.strptime(date, '%d %b %Y')
    date2 = date2.strftime('%Y-%m-%d')
    suppliers = driver.find_elements_by_xpath('//*[@id="notice-awards"]/table/tbody/tr/td[2]/b/a')
    title=  driver.find_element_by_xpath("/html/body/div/article/header/h1").text
    description=  driver.find_element_by_xpath("/html/body/div/article/section[4]/p").text
    value =  driver.find_element_by_xpath("/html/body/div/article/section[1]/div[1]/dl/dd[4]").text
    x=[]
    for supplier in suppliers:
        x.append(supplier.text)


    x2 = list(set(x))

    row = [date,source,buyer,sector,title,description]
    columns = ['DATE','SOURCE','BUYER','SECTOR','TITLE','DESCRIPTION']
    df = pd.DataFrame(row).T
    df.columns = columns
    df2 = pd.DataFrame(x2)
    df2.columns = ['SUPPLIER']

    supplier_list = list(set(x))

    df2 = pd.DataFrame(supplier_list)
    df2.columns = ['SUPPLIER']
    df2['DATE']=date
    df2['SOURCE']=source
    df2['BUYER']=buyer
    df2['SECTOR']=sector
    df2['TITLE']=title
    df2['DESCRIPTION']=description
    df2['VALUE']=value
    df2['NUM_SUPPLIERS']=df2.shape[0]
    df2=df2[['DATE','SOURCE','BUYER','SECTOR','TITLE','VALUE','NUM_SUPPLIERS','SUPPLIER','DESCRIPTION']]
    driver.close()
    return df2

