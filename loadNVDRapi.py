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
    sdate = '&date=21%2F03%2F2024' #'' #'&date=22%2F12%2F2023'
    url = 'https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol'#+sdate
    #r = requests.get('https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol')
    #url = 'https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol&date=05%2F02%2F2024'
    headers = {
        'Content-Type': 'application/json',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th',
        'Referer' : 'https://www.set.or.th/th/market/statistics/nvdr/trading-by-stock',
        'Cookie': 'visid_incap_2685219=cghk3sCVQiGiCTLFVBW2fVfPC2YAAAAAQUIPAAAAAAAC9nCBacuKsdm0wYExNzQ8; _gcl_au=1.1.10485940.1712050009; visid_incap_2046605=1d5MwYHiThieEGQrk3euv1nPC2YAAAAAQUIPAAAAAADQt04dRWTSMAYGDpbqZxtr; visid_incap_2771851=F+CMpOrURA2dA+ZLRY/uCGn8DWYAAAAAQUIPAAAAAABCePBUygL/GbLK6cynUfdB; incap_ses_1007_2046605=CGNfAKQDzlxb1fDQLpX5DZPNEmYAAAAAhphD2b7B4DNp9Q/pumpLuA==; __lt__cid=e98c80f4-8a06-4a90-96b5-f2b1e646ca23; _cbclose=1; _cbclose23453=1; _fbp=fb.2.1712508356337.496222663; SET_COOKIE_POLICY=20231111093657; incap_ses_1007_2771851=THbxaF3wBGbb8vDQLpX5DczNEmYAAAAAe6dgJlJeqGgl3CqH2rSaWQ==; incap_ses_8225_2046605=2tgMNEZUBTm99lb2sRIlcjfPEmYAAAAAuu2b70goaYJlL3lmF9SJWg==; _hjSessionUser_3931504=eyJpZCI6IjFhMzAzYjM4LTI5NTMtNWZiMy04ZDZkLTMxZDg2ZTY4OWYwZiIsImNyZWF0ZWQiOjE3MTI1MDgzNTgzMjAsImV4aXN0aW5nIjp0cnVlfQ==; exp_history={"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w-V2","msgt":"popup","count":1}; incap_ses_705_2046605=nh25Bxooehe6RUx9SKrICf3QEmYAAAAAv+oKyPXiDpkD4etWuSywxQ==; incap_ses_9067_2046605=NzWIHQaJHFGIZjpGMHXUfT7REmYAAAAA2/0T3sIaXdHasH53zxZAEA==; incap_ses_1802_2046605=tObgWRyDPEGEVRWAhv0BGX0/E2YAAAAAi/42iD1F+w4W4wqkhd6HOQ==; nlbi_2046605=fULeMAos60tcPdYhU9DvIwAAAACYCKhL+7a/NoXk9m7saGwI; incap_ses_148_2046605=w9fZKO3VPiVgfCxQvs0NAl26FmYAAAAAsFZbp86spH8KYOorNvJPwA==; _gid=GA1.3.656036860.1712765543; incap_ses_148_2771851=lyIRJ34gtVSCAi1Qvs0NAne6FmYAAAAA3RHq+dmjOsM1O4YYDKOlrw==; incap_ses_403_2046605=FQlaNdfo6VidRTfAX76XBc1KF2YAAAAACOfYWJR+ueSgC2gwxMpKnA==; charlot=1f194ee6-1342-4532-ac33-46b5e017decf; incap_ses_8025_2046605=LwFIZgTOdHgQwoSo/YZeb/lvGGYAAAAAdLrwTHuUNs872gqhIcO/BQ==; landing_url=https://www.set.or.th/th/market/statistics/nvdr/trading-by-stock; _uid23453=D5705AAF.6; _ctout23453=1; _hjSession_3931504=eyJpZCI6IjVkYmNiYjQxLTljYjAtNGNjMi1hODMxLTNhZTdlMzM3ODIzNyIsImMiOjE3MTI4Nzc1Njk1NDMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; incap_ses_8025_2771851=fPebB1LoaSBXxoSo/YZebwNwGGYAAAAAa3ZcjCj5O1jvN1uMweU3gw==; _ga_ET2H60H2CB=GS1.1.1712877571.8.0.1712877572.59.0.0; _ga_6WS2P0P25V=GS1.1.1712877572.7.0.1712877572.60.0.0; _ga=GA1.3.1284817477.1712050015; _gat_UA-426404-8=1; api_call_counter=5'
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
