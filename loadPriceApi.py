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
        'Cookie':'_gcl_au=1.1.1205078109.1698726326; exp_history={"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"vZj2v2cjSuCT8gIzugw5hw","msgt":"new_highlight","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w-V2","msgt":"popup","count":1}; SET_COOKIE_POLICY=20231111093657; visid_incap_2685219=sdb+LKEsToWrZTFRJ5LYj9PhZmUAAAAAQUIPAAAAAADUoXHQK1svDVddQuz4S+hI; visid_incap_2046605=R4oPAQZESECk5GE5N4iaxdThZmUAAAAAQUIPAAAAAAAqpoP6BGHk+JludZxYQne3; visid_incap_2771851=IYLnw5D+QrOpF4xkbdCLDkf6Z2UAAAAAQUIPAAAAAAAA8HK5A9Hr3xfeCoG6+IU3; _fbp=fb.2.1703263377990.1123658674; charlot=a9eb4c76-d751-44a0-b6d5-6c2360c76d42; nlbi_2046605=tQeRGcoNmXFlihnUU9DvIwAAAACsEFXOlWqQcRHvl3RYSm9Q; incap_ses_1262_2046605=A4yNM3joa3SjKnExR4eDEfKwj2UAAAAARSoFN9wTCOekbG1rLCmJbQ==; _cbclose=1; _cbclose23453=1; _uid23453=2EDF04D8.37; _ctout23453=1; landing_url=https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100; api_call_counter=1; _gid=GA1.3.1643976784.1703915778; _gat_UA-426404-8=1; incap_ses_1262_2771851=XGsTQhQlMh2VO3ExR4eDEQGxj2UAAAAA+VK7HuZK//Bvn0p+om1/hA==; _ga_6WS2P0P25V=GS1.1.1703915778.47.0.1703915778.60.0.0; _ga=GA1.1.518446968.1698726356; _ga_ET2H60H2CB=GS1.1.1703915778.47.0.1703915778.60.0.0',
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