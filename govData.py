from io import StringIO

import pandas as pd

df = pd.read_csv('notices.csv')

supplier = df['Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]']
supplier2 = df[['Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]']]

''''create a function to extract out the companys'''
dict={'\r':'','\n':''}

def clean_name(x):
    for key in dict.keys():
        x=x.replace(key,dict.get(key))
    return x

master_df= pd.DataFrame()
for index, row in df.iterrows():
    #print(supplier[index])
    x=supplier[index]
    x=clean_name(x)
    x3= x.replace('][',']\n[')
    x1=StringIO(x3)
    x2=pd.read_csv(x1,delimiter='|',header=None)
    x2['index']=index
    master_df=pd.concat([master_df,x2])

master_df.columns=['Name','Address','Ref type','Ref Number','Is SME','Is VCSE','index']
master_df['Name']=master_df['Name'].apply(lambda x:x[1:])
master_df['Is VCSE']=master_df['Is VCSE'].apply(lambda x:x[:-1])

 = df.merge(master_df,how='left',left_on=df.index,right_on=['index'])

df3=df2[['Organisation Name','Title', 'Description','Awarded Date', 'Awarded Value','Name', 'Address', 'Ref type', 'Ref Number']]