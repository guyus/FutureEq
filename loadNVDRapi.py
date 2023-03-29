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
    r = requests.get('https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol')
    #https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol&date=09/03/2023
    data = r.json()
    if r.status_code!=200:
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
