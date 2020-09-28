import requests
from bs4 import BeautifulSoup
import pandas as pd

from datetime import datetime
import time
url= r'http://www.worldgovernmentbonds.com/sovereign-cds/'
page=requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

df_list = pd.read_html(url)