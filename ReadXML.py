import pandas as pd

from lxml import etree
from bs4 import BeautifulSoup
import os
supplier_cols = ['SUPPLIER_NAME','SUPPLIER_ID','SUPPLIER_POSTCODE','SUPPLIER_COUNTRY']
def award_contract_funct(result):
    master_df = pd.DataFrame()
    for res in result:
        try:
            name = res.find('officialname').contents[0]
        except:
            name=None

        try:
            national_id = res.find('nationalid').contents[0]
        except:
            national_id=None
        try:
            country= getattr(res.find('country'),'attrs').get('value')
        except:
            country=None

        try:
            postcode = res.find('postal_code').contents[0]
        except:
            postcode=None
        temp_list = [name,national_id,postcode,country]
        temp_df = pd.DataFrame(temp_list).T
        master_df=pd.concat([master_df,temp_df])
    master_df=master_df.drop_duplicates()
    master_df.columns = supplier_cols
    master_df['NUM_SUPPLIERS']=master_df.shape[0]
    return master_df

all_contracts = pd.DataFrame()
for month_folder in os.listdir(r'C:\Users\S\PycharmProjects\bidstat_scrape\bidstat_scrape\Data'):
    if month_folder[-2:]=='gz':
        continue
    for daily_folder in os.listdir(fr'C:\Users\S\PycharmProjects\bidstat_scrape\bidstat_scrape\Data\{month_folder}'):
        print (daily_folder)
        for file in os.listdir(fr'C:\Users\S\PycharmProjects\bidstat_scrape\bidstat_scrape\Data\{month_folder}\{daily_folder}'):
            with open(fr'C:\Users\S\PycharmProjects\bidstat_scrape\bidstat_scrape\Data\{month_folder}\{daily_folder}\{file}',encoding="utf-8") as f:
                x= f.read()

            y = BeautifulSoup(x, "lxml")
            contract_type = y.find('td_document_type').contents[0]
            z = getattr(y.find('iso_country'), 'attrs')
            if (contract_type == 'Contract award notice') and z.get('value') == 'UK':
                try:
                    value = y.find('val_total').contents[0]
                    value_currency = getattr(y.find('val_total'), 'attrs').get('currency')
                    if int(float(value))<1000000:
                        continue
                except:
                    try:
                        value_low = y.find('value_range').find('low').contents[0]
                    except:
                        continue
                    if int(float(value_low))<1000000:
                        continue
                    value_high = y.find('value_range').find('high').contents[0]
                    value=str(value_low)+'-'+str(value_high)
                    value_currency = getattr(y.find('value_range'), 'attrs').get('currency')

                print('yes - ', file)
                organisation = y.find('address_contracting_body')
                organisation_name = organisation.find('officialname').contents[0]
                try:
                    organisation_pc = organisation.find('postal_code').contents[0]
                except:
                    organisation_pc=None
                ###contract details
                contract_info = y.find('object_contract')
                contract_title = contract_info.find('title').find('p').contents[0]
                contract_desc = contract_info.find('short_descr').find('p').contents[0]
                url = y.find('uri_list').find('uri_doc').contents[0]
                contract_pub_date = y.find('date_pub').contents[0]
                ##awarded supplier
                awarded_contact = y.findAll('award_contract')




                date_pub = y.find('date_pub').contents[0]


                contract_df = award_contract_funct(awarded_contact)
                contract_df['CONTRACT_BUYER'] = organisation_name
                contract_df['CONTRACT_BUYER_POSTCODE'] = organisation_pc
                contract_df['CONTRACT_TITLE'] = contract_title

                contract_df['CONTRACT_DATE'] = contract_pub_date
                contract_df['CONTRACT_DESC'] = contract_desc
                contract_df['CONTRACT_URL'] = url
                contract_df['CONTRACT_VALUE'] = value
                contract_df['CONTRACT_CURRENCY'] = value_currency
                all_contracts=pd.concat([all_contracts,contract_df])
                del value
            f.close()
#364133_2020



