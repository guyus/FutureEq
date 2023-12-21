import json
import sqlite3
import pandas as pd
import config
import numpy as np
import requests

from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])
#f = open('./data/NVDRstock-trading31-01-23.json')
#data = json.load(f)
#data = pd.read_json('./data/NVDRstock-trading31-01-23.json')
# 'Accept': 'application/json',
#         'Host': 'www.set.or.th',
#         'Origin': 'https://www.set.or.th',
# 'Cookie': 'id=KqKgOXZeJxapT8k8AL1rOg%3D%3D00000000'
from http.client import HTTPConnection
HTTPConnection._http_vsn_str = 'HTTP/1.1'

sSource = "api"
if sSource=="file":
    with open('./data/Pricecomposition02-02-23.json','r',encoding='utf-8') as f:
        data = json.loads(f.read())
elif sSource=="api":
    url = 'https://www.set.or.th/api/set/index/set100/composition?lang=en'
    headers = {
        'Referer':'https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100',
        'Cookie':'clientUuid=46dba5c0-33e9-4222-b6b8-212425c3ea1d; _tt_enable_cookie=1; _ttp=9T89l8YjGpqV5ow2UPNAxsXVjJu; charlot=ef3a9076-1a49-497c-8ba8-434468c8103d; nlbi_2046605=gZ6FbffIFDBskqwhU9DvIwAAAAD/NqNSRqjdg5e/uXAxrk54; visid_incap_2046605=Lofvijs0QW6Kl0cV+9x45qJahGUAAAAAQUIPAAAAAACaWcrrdmEcukUqvcFyFwgK; incap_ses_705_2046605=MUfHKj4I8h0xZHo9MarICaJahGUAAAAA1m8R6QkJ4F2EfweUX+79EA==; _cbclose=1; _cbclose23453=1; _uid23453=576C222F.3; _ctout23453=1; _gcl_au=1.1.217156769.1703172775; landing_url=https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100; _fbp=fb.2.1703172776501.822757007; SET_COOKIE_POLICY=20231111093657; _gid=GA1.3.1633165460.1703172783; _gat_UA-426404-8=1; display-exit-ad=true; lightbox_exit_banner_timeout=1; exp_history={"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}; visid_incap_2771851=G5foQuU9SzGsbFinOZG7IbFahGUAAAAAQUIPAAAAAAAWDM8XlZAMoIyFi1udW5R2; incap_ses_705_2771851=xRIIa1mBXzoXcXo9MarICbFahGUAAAAA+Bigse0z0QsromFKFTDOIw==; _ga=GA1.1.1498211339.1680279077; _ga_ET2H60H2CB=GS1.1.1703172783.3.1.1703172802.41.0.0; _ga_6WS2P0P25V=GS1.1.1703172784.1.1.1703172802.42.0.0; api_call_counter=2',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th'
        }
    r = requests.get(url,headers=headers)
    #print('data:'+r.text)
    
    if r.status_code==200:
        data = r.json()
    else:
        print(r.status_code)
        exit

#print(data['indexInfos'][0]['marketDateTime'][:10])
#cdate = pd.DataFrame(data).iloc[0].astype(str).str[:10]['date'], record_prefix=
#d1.info()
#print(cdate)
df = pd.json_normalize(data['composition']['stockInfos']) 
df.drop(['average', 'floor','ceiling', 'trVolume','trValue', 'aomVolume','aomValue', 'bids','offers'], axis=1, inplace=True)
df.rename(columns = {'symbol': 'series', 'last': 'close', 'percentChange': 'pchange','totalVolume': 'vol','totalValue': 'value'}, inplace = True)
df.drop(df.iloc[:, 11:],axis = 1, inplace=True)
df['trddate'] = data['indexInfos'][0]['marketDateTime'][:10] #pd.to_datetime('today').date() - pd.Timedelta("1 day")
#print(df['trddate'][0])
a = [0]
df = df[~df['close'].isin(a)]
df.info()
print(df)
# df['composition.stockInfos'].info()
# print(df['composition.stockInfos'])
sql = "select * from sprice where trddate = '"+ df['trddate'].astype(str)[0] + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sprice', con=engine, if_exists='append')
p2 = pd.read_sql("select * from sprice where trddate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'", con=engine)
print(p2)
len(df)