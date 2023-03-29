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
    r = requests.get('https://www.set.or.th/api/set/shortsales')
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