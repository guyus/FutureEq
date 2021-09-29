import pandas as pd
# import sqlite3
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')
df=pd.read_html('https://www.set.or.th/set/shortsales.do?language=en&country=US')

df[0].rename(columns = {'Securities':'series','Volume (Shares)':'volume','Turnover (Baht)':'value',
'%Short Sale Volume Comparing with Auto Matching':'per'},inplace = True)
df[0]['trddate'] = pd.to_datetime('today').date()


df=df[0]
df['trddate'] = df['trddate'].apply(pd.DateOffset(-1)).apply(lambda x : x.date())
df['per']=df['per'].apply(lambda x:x.replace(' %',''))
sql = "select * from sshortsell where trddate = '"+ df.iloc[0,4].strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sshortsell', con=engine, if_exists='append')
print(df)