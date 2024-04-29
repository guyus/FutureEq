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
    sdate = '?fromDate=21%2F03%2F2024&toDate=21%2F03%2F2024'
    url = 'https://www.set.or.th/api/set/shortsales'#+sdate
    url = 'https://www.set.or.th/api/set/shortsales/trading/list'
    headers = {
        'Content-Type': 'application/json',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th',
        'Referer' : 'https://www.set.or.th/en/market/statistics/short-sell',
        'Cookie': 'exp_history={"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"vZj2v2cjSuCT8gIzugw5hw","msgt":"new_highlight","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w-V2","msgt":"popup","count":1}; SET_COOKIE_POLICY=20231111093657; visid_incap_2685219=sdb+LKEsToWrZTFRJ5LYj9PhZmUAAAAAQUIPAAAAAADUoXHQK1svDVddQuz4S+hI; visid_incap_2046605=R4oPAQZESECk5GE5N4iaxdThZmUAAAAAQUIPAAAAAAAqpoP6BGHk+JludZxYQne3; visid_incap_2771851=IYLnw5D+QrOpF4xkbdCLDkf6Z2UAAAAAQUIPAAAAAAAA8HK5A9Hr3xfeCoG6+IU3; _fbp=fb.2.1703263377990.1123658674; _gcl_au=1.1.521886091.1706669757; lifetime_session=1; uref=7253157; id=B35cGaUHNGi8DkuV1P8RAA%3D%3D00000000; _ga_CYH05JDHY9=GS1.3.1710826306.1.1.1710826528.54.0.0; charlot=06371b2a-989e-4c92-b01e-7f720e74c926; nlbi_2046605=UQlqKBWs6heSy/0zPNFBJgAAAABQdBSFNXtp8v293Mp2sPKp; _cbclose=1; route=1d47dbe8563e165d38d06ac6d2f1ea46; _cbclose23453=1; incap_ses_7240_2771851=uuvuEwayuVEKxfVdUKZ5ZIBa/mUAAAAAZ/ctNLPVhDs8V5zcHWSm8Q==; _gid=GA1.3.2054429178.1711168130; incap_ses_7240_2046605=YFQbJyWVajXUPPtdUKZ5ZBFi/mUAAAAAommV+R7C03YK37fj8jPBdQ==; incap_ses_235_2046605=GDZRQLypFCkMP/BUweNCA7Cd/mUAAAAAPwTWB8+31PkbGWLZqRMwfA==; landing_url=https://www.set.or.th/th/market/statistics/nvdr/trading-by-stock; _uid23453=2EDF04D8.95; _ctout23453=1; incap_ses_235_2771851=51wwH33vAgBtd/FUweNCA2if/mUAAAAAtETCUAZyCwsaAxV4d0P8zw==; api_call_counter=5; _ga=GA1.1.518446968.1698726356; _ga_ET2H60H2CB=GS1.1.1711185759.121.1.1711186635.24.0.0; _ga_6WS2P0P25V=GS1.1.1711185759.121.1.1711186635.24.0.0'
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