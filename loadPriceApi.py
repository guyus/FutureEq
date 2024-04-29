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
    #url = 'https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100'
    headers = {
        'Referer':'https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100',
        'Cookie':'visid_incap_2685219=cghk3sCVQiGiCTLFVBW2fVfPC2YAAAAAQUIPAAAAAAAC9nCBacuKsdm0wYExNzQ8; _gcl_au=1.1.10485940.1712050009; visid_incap_2046605=1d5MwYHiThieEGQrk3euv1nPC2YAAAAAQUIPAAAAAADQt04dRWTSMAYGDpbqZxtr; visid_incap_2771851=F+CMpOrURA2dA+ZLRY/uCGn8DWYAAAAAQUIPAAAAAABCePBUygL/GbLK6cynUfdB; incap_ses_1007_2046605=CGNfAKQDzlxb1fDQLpX5DZPNEmYAAAAAhphD2b7B4DNp9Q/pumpLuA==; __lt__cid=e98c80f4-8a06-4a90-96b5-f2b1e646ca23; _cbclose=1; _cbclose23453=1; _fbp=fb.2.1712508356337.496222663; SET_COOKIE_POLICY=20231111093657; incap_ses_1007_2771851=THbxaF3wBGbb8vDQLpX5DczNEmYAAAAAe6dgJlJeqGgl3CqH2rSaWQ==; incap_ses_8225_2046605=2tgMNEZUBTm99lb2sRIlcjfPEmYAAAAAuu2b70goaYJlL3lmF9SJWg==; _hjSessionUser_3931504=eyJpZCI6IjFhMzAzYjM4LTI5NTMtNWZiMy04ZDZkLTMxZDg2ZTY4OWYwZiIsImNyZWF0ZWQiOjE3MTI1MDgzNTgzMjAsImV4aXN0aW5nIjp0cnVlfQ==; exp_history={"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w-V2","msgt":"popup","count":1}; incap_ses_705_2046605=nh25Bxooehe6RUx9SKrICf3QEmYAAAAAv+oKyPXiDpkD4etWuSywxQ==; incap_ses_9067_2046605=NzWIHQaJHFGIZjpGMHXUfT7REmYAAAAA2/0T3sIaXdHasH53zxZAEA==; incap_ses_1802_2046605=tObgWRyDPEGEVRWAhv0BGX0/E2YAAAAAi/42iD1F+w4W4wqkhd6HOQ==; charlot=1f194ee6-1342-4532-ac33-46b5e017decf; nlbi_2046605=fULeMAos60tcPdYhU9DvIwAAAACYCKhL+7a/NoXk9m7saGwI; incap_ses_148_2046605=w9fZKO3VPiVgfCxQvs0NAl26FmYAAAAAsFZbp86spH8KYOorNvJPwA==; landing_url=https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100; __lt__sid=0a3c50e0-eda92263; _uid23453=D5705AAF.4; _ctout23453=1; _hjSession_3931504=eyJpZCI6IjhjZjUzM2Y4LTkyYTQtNDI3My1iOGMxLWI1MjE1YjQ0ZDI2MiIsImMiOjE3MTI3NjU1NDE0NDIsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_ET2H60H2CB=GS1.1.1712765542.5.0.1712765543.59.0.0; _ga_6WS2P0P25V=GS1.1.1712765543.5.0.1712765543.60.0.0; _ga=GA1.3.1284817477.1712050015; _gid=GA1.3.656036860.1712765543; _gat_UA-426404-8=1; api_call_counter=2',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th'
        }
    r = requests.get(url,headers=headers)
    #print('data:'+r.text)
    #print(r.cookies.get_dict)
    #exit() 
    if r.status_code==200:
        data = r.json()
    else:
        print(r.status_code)
        exit()

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