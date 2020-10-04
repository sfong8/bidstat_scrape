import pandas as pd
from io import StringIO
bid = pd.read_csv(r'scraped_bidstat_20201002_20_34_17.csv')




dict={'\r':' ','\n':' ','\t':''}
import re
def clean_name(x):
    x=x.upper()
    for key in dict.keys():
        x=x.replace(key,dict.get(key))
    x = re.sub(r'\t', ' ', x)
    return ' '.join([y.strip() for y in x.split()])

bid['BUYER']=bid['BUYER'].apply(lambda x: clean_name(x))

unique_names = bid[['BUYER']].drop_duplicates().reset_index(drop=True)

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
x = vectorizer.fit_transform(unique_names['BUYER'])


y = pd.DataFrame([vectorizer.get_feature_names(),x.toarray().sum(axis=0) ]).T
y=y.sort_values(1,ascending=False)



###do the same for the suppliers
q=pd.DataFrame(bid[['SECTOR','SUPPLIER']].groupby(['SECTOR','SUPPLIER']).size().reset_index(name='count'))
q=q.sort_values('count',ascending=False)