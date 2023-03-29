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
sSource = "api"
if sSource=="file":
    with open('./data/Pricecomposition02-02-23.json','r',encoding='utf-8') as f:
        data = json.loads(f.read())
elif sSource=="api":
    r = requests.get('https://www.set.or.th/api/set/index/set100/composition?lang=en')
    data = r.json()
    if r.status_code!=200:
        exit

print(data['indexInfos'][0]['marketDateTime'][:10])
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