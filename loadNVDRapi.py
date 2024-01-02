import json
import sqlite3
import pandas as pd
import config
import numpy as np
import requests
import sys

from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])

sSource = "api"
if sSource=="file":
    with open('./data/NVDRstock-trading31-01-23.json','r') as f:
        data = json.loads(f.read())
elif sSource=="api":
    sdate = '' #'&date=22%2F12%2F2023'
    url = 'https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol'+sdate
    #r = requests.get('https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol')
    #url = 'https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol&date=09/03/2023'
    headers = {
        'Content-Type': 'application/json',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th',
        'Referer' : 'https://www.set.or.th/th/market/statistics/nvdr/trading-by-stock',
        'Cookie': '_gcl_au=1.1.1205078109.1698726326; exp_history={"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"vZj2v2cjSuCT8gIzugw5hw","msgt":"new_highlight","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w-V2","msgt":"popup","count":1}; SET_COOKIE_POLICY=20231111093657; visid_incap_2685219=sdb+LKEsToWrZTFRJ5LYj9PhZmUAAAAAQUIPAAAAAADUoXHQK1svDVddQuz4S+hI; visid_incap_2046605=R4oPAQZESECk5GE5N4iaxdThZmUAAAAAQUIPAAAAAAAqpoP6BGHk+JludZxYQne3; visid_incap_2771851=IYLnw5D+QrOpF4xkbdCLDkf6Z2UAAAAAQUIPAAAAAAAA8HK5A9Hr3xfeCoG6+IU3; _fbp=fb.2.1703263377990.1123658674; charlot=a9eb4c76-d751-44a0-b6d5-6c2360c76d42; nlbi_2046605=tQeRGcoNmXFlihnUU9DvIwAAAACsEFXOlWqQcRHvl3RYSm9Q; _cbclose=1; _cbclose23453=1; _gid=GA1.3.1643976784.1703915778; incap_ses_1262_2046605=n/5sabuWWVmNDIwxR4eDEXTLj2UAAAAA0X25AcuAvAzj5TB5V3l7vQ==; _uid23453=2EDF04D8.38; _ctout23453=1; landing_url=https://www.set.or.th/th/market/statistics/nvdr/trading-by-stock; api_call_counter=4; _ga=GA1.1.518446968.1698726356; incap_ses_1262_2771851=jmOGHCcEW0CtLIwxR4eDEZnLj2UAAAAAmOt2N3cFFL2d9yIiIlshgg==; _ga_ET2H60H2CB=GS1.1.1703922570.48.1.1703922799.60.0.0; _ga_6WS2P0P25V=GS1.1.1703922570.48.1.1703922799.60.0.0; visit_time=217'
        }
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        data = r.json()
    else:
        print("Error from server: " + str(r.content))
        exit

#df = pd.json_normalize(r.json(), record_path =['nvdrTradings'])

cdate = pd.DataFrame(data).iloc[0].astype(str).str[:10]['date']
#df.info()
print(cdate)
df = pd.json_normalize(data, record_path =['nvdrTradings'])
df.drop(['buyVolume', 'sellVolume','netVolume', 'totalVolume','underlyingVolume', 'percentVolume'], axis=1, inplace=True)


#print(df)
df.rename(columns = {'date': 'trddate', 'buyValue': 'buy', 'sellValue': 'sell', 'netValue': 'net', 'totalValue': 'total', 'percentValue': 'percent', 'underlyingValue':'trdvalue'}, inplace = True)
df['ft']=df['total']/df['trdvalue']*100
df['ft'].round(2)
#df.info()
print(df)
sql = "select * from snvdr where trddate = '"+ cdate + "'"
print(sql)
df = df.loc[~((df['buy'] == '-') | (df['sell'] == '-') | (df['net'] == '-'))]
print(df)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='snvdr', con=engine, if_exists='append')
cur = engine.connect()
cur.execute("DELETE FROM snvdrsum")
cur.execute("INSERT into snvdrsum(Symbol, sumn, counts) select symbol,round(sum(net)) as sumn,count(symbol)counts from snvdr group by symbol")
