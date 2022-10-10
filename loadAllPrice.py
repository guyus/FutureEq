import pandas as pd
import numpy as np
import config

df=pd.read_html('https://classic.set.or.th/mkt/commonstocklistresult.do?market=SET&language=en&country=US')
#df=pd.read_html('sprice.htm')
from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])

def GetDf(i):
    return df[i]

frames = [ GetDf(f) for f in range(2,len(df)) ]
df2 = pd.concat(frames)
#for i in range(1,len(df)):
    
    #print(df[i])
i=2
df2.rename(columns={'Index': 'index','Symbol': 'series','Sign': 'sign','Open': 'open','High': 'high','Low': 'low','Last': 'close','Change': 'change','%Change': 'pchange','Bid': 'bid','Offer': 'offer','Volume(Shares)': 'vol','Value(\'000 Baht)': 'value'}, inplace=True)
df2 = df2.replace('-','0')
print(df2)
df2['open'] = df2['open'].astype(float)
df2['high'] = df2['high'].astype(float)
df2['low'] = df2['low'].astype(float)
df2['close'] = df2['close'].astype(float)
df2['change'] = pd.to_numeric(df2['change'], errors='coerce') #df2['change'].astype(float)
df2['pchange'] = pd.to_numeric(df2['pchange'], errors='coerce') #df2['pchg'].astype(float)
df2['bid'] = df2['bid'].astype(float)
df2['offer'] = df2['offer'].astype(float)
df2['vol'] = df2['vol'].astype(float)
df2['value'] = df2['value'].astype(float)

df2['trddate'] = pd.to_datetime('today').date()
a = [0]
df2 = df2[~df2['close'].isin(a)]

print(df2)
sql = "select * from sprice where trddate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df2.to_sql(name='sprice', con=engine, if_exists='append')
p2 = pd.read_sql("select * from sprice where trddate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'", con=engine)
print(p2)
len(df)