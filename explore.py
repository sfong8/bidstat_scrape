import pandas as pd
from io import StringIO
bid = pd.read_csv(r'scraped_bidstat_20201002_20_34_17.csv')

# master_df = pd.DataFrame()
# for i in range(1,6):
#
#     hmrc = pd.read_csv(fr'D:\Chrome Download\hmrc_contracts_{i}.csv')
#     master_df=pd.concat([master_df,hmrc])
#
# master_df=master_df.drop_duplicates()
master_df=pd.read_csv('hmrc_all.csv')

master_df2 = master_df[['Organisation Name', 'Status','Published Date', 'Title', 'Description', 'Awarded Value', 'Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]']]
master_df3 = master_df2.drop_duplicates()


master_df3['Published Date']=master_df3['Published Date'].apply(lambda x: str(x)[:10])
master_df3=master_df3.drop_duplicates()
master_df3=master_df3.reset_index(drop=True)
supplier = master_df3['Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]']

dict={'\r':' ','\n':' ','\t':''}
import re
def clean_name(x):
    for key in dict.keys():
        x=x.replace(key,dict.get(key))
    x = re.sub(r'\t', ' ', x)
    return ' '.join([y.strip() for y in x.split()])

master_df= pd.DataFrame()
for index, row in master_df3.iterrows():
    #print(supplier[index])
    x=supplier[index]
    x=clean_name(x)
    x3= x.replace('][',']\n[')
    x1=StringIO(x3)
    x2 = pd.read_csv(x1, delimiter='|', header=None,
                     names=['Name', 'Address', 'Ref type', 'Ref Number', 'Is SME', 'Is VCSE', 'index'])
    x2['index']=index
    x2['NUM_SUPPLIERS']=x2.shape[0]
    master_df=pd.concat([master_df,x2])

master_df.columns=['Name','Address','Ref type','Ref Number','Is SME','Is VCSE','index','NUM_SUPPLIERS']
master_df['Name']=master_df['Name'].apply(lambda x:str(x)[1:])
master_df['Is VCSE']=master_df['Is VCSE'].apply(lambda x:x[:-1])

df2 = master_df3.merge(master_df,how='left',left_on=master_df3.index,right_on=['index'])

df3=df2[['Organisation Name','Title', 'Description','Published Date', 'Awarded Value','NUM_SUPPLIERS','Name', 'Address', 'Ref type', 'Ref Number']].drop_duplicates()
bid_cf = bid[bid['SOURCE']=='Contracts Finder']
df3_ = pd.DataFrame(df3['Published Date'].value_counts().reset_index())
bid_cf_ =  pd.DataFrame(bid_cf['DATE'].value_counts().reset_index())

z= df3_.merge(bid_cf_,how='outer',on='index')


bid_feb14 = bid_cf[bid_cf['DATE']=='14 Feb 2020']
bid_feb14=bid_feb14.sort_values(['BUYER','NUM_SUPPLIERS'])
GOV_feb14 = df3[df3['Published Date']=='2020-02-14']
GOV_feb14=GOV_feb14.sort_values(['Organisation Name','NUM_SUPPLIERS'])

##unique company house id
company_house = df3[['Ref type','Ref Number']].drop_duplicates()