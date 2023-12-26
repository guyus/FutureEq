import json
import sqlite3
import pandas as pd
import config
import numpy as np
import requests

from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])
##--- SET CONFIG SOURCE
sSource = "api"
if sSource=="file":
    with open('./data/shortsales01-02-23.json','r') as f:
        data = json.loads(f.read())
elif sSource=="api":
    sdate = '' #'?fromDate=22%2F12%2F2023&toDate=22%2F12%2F2023'
    url = 'https://www.set.or.th/api/set/shortsales'+''
    headers = {
        'Content-Type': 'application/json',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th',
        'Referer' : 'https://www.set.or.th/en/market/statistics/short-sell',
        'Cookie': 'clientUuid=46dba5c0-33e9-4222-b6b8-212425c3ea1d; _tt_enable_cookie=1; _ttp=9T89l8YjGpqV5ow2UPNAxsXVjJu; charlot=ef3a9076-1a49-497c-8ba8-434468c8103d; nlbi_2046605=gZ6FbffIFDBskqwhU9DvIwAAAAD/NqNSRqjdg5e/uXAxrk54; visid_incap_2046605=Lofvijs0QW6Kl0cV+9x45qJahGUAAAAAQUIPAAAAAACaWcrrdmEcukUqvcFyFwgK; incap_ses_705_2046605=MUfHKj4I8h0xZHo9MarICaJahGUAAAAA1m8R6QkJ4F2EfweUX+79EA==; _cbclose=1; _cbclose23453=1; _uid23453=576C222F.3; _ctout23453=1; _gcl_au=1.1.217156769.1703172775; landing_url=https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100; _fbp=fb.2.1703172776501.822757007; SET_COOKIE_POLICY=20231111093657; _gid=GA1.3.1633165460.1703172783; _gat_UA-426404-8=1; display-exit-ad=true; lightbox_exit_banner_timeout=1; exp_history={"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}; visid_incap_2771851=G5foQuU9SzGsbFinOZG7IbFahGUAAAAAQUIPAAAAAAAWDM8XlZAMoIyFi1udW5R2; incap_ses_705_2771851=xRIIa1mBXzoXcXo9MarICbFahGUAAAAA+Bigse0z0QsromFKFTDOIw==; _ga=GA1.1.1498211339.1680279077; _ga_ET2H60H2CB=GS1.1.1703172783.3.1.1703172802.41.0.0; _ga_6WS2P0P25V=GS1.1.1703172784.1.1.1703172802.42.0.0; api_call_counter=2'
        }
    r = requests.get(url,headers=headers)
    #r = requests.get('https://www.set.or.th/api/set/shortsales')
    #https://www.set.or.th/api/set/shortsales?fromDate=09/03/2023&toDate=09/03/2023
    data = r.json()
    if r.status_code!=200:
        exit

#cdate = data['fromDate'][:10]
#d1.info()
print(data['fromDate'][:10])
df = pd.json_normalize(data['shortSales'])

df.info()
df.rename(columns = {'symbol': 'series', 'percentValue': 'per', 'percentVolume': 'perc'}, inplace = True)
df['trddate'] = data['fromDate'][:10] #pd.to_datetime('today').date() - pd.Timedelta("1 day")
#df.info()
print(df)
sql = "select * from sshortsell where trddate = '"+ data['fromDate'][:10] + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sshortsell', con=engine, if_exists='append')
print(df)