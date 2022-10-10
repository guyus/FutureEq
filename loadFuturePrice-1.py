from asyncio.windows_events import NULL
import pandas as pd
# import sqlite3
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://www.tfex.co.th/tfex/dailyMarketReport.html?periodView=A&selectedDate=P&marketListId=SF&instrumentId=&go=GO&locale=en_US')
#df=pd.read_html('ss15.html');
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')
df=df[0]

tdate = df.iloc[:1,12].apply(lambda x: x.replace('Trading date: ',''))
tdate.values[0]
df1=df[df.Series.str.contains('M22',case=False)]

df2 = df1[['Series','Last','Chg(%Chg)','Vol','OI']]
df2['chg'] = df2['Chg(%Chg)'].str.slice(start=0,stop=-9)
df2['Chg(%Chg)'].str.slice(start=-9)
df2['Chg(%Chg)'].replace('(','')
df2['Chg(%Chg)'].replace('%)','')

df2['Last'].replace('-','')
df2['Vol'].replace('-','')
df2['OI'].replace('-','')
df2['Series'].replace('H22X','')
df2['Series'].replace('H22','')
df2['Chg(%Chg)'] = pd.to_numeric(df2['Chg(%Chg)'],errors='coerce')

df2['chg'] = pd.to_numeric(df2['chg'],errors='coerce')
df2.rename(columns={'Series': 'series', 'Last': 'last', 'chg': 'chg', 'Vol': 'vol', 'OI': 'oi', 'Chg(%Chg)': 'pchg' }, inplace=True)

#df2['PChg'] = df2['Chg(%Chg)'].apply(lambda x: x.replace('Chg(%Chg)','PChg').replace())
keptDate = pd.to_datetime(tdate.values[0]).date()
df2['trddate'] = pd.to_datetime(tdate.values[0]).date()

df2= df2.fillna(0)
print(df2)

sql = "select * from ssfprice where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df2.to_sql(name='ssfprice', con=engine, if_exists='append')
p2 = pd.read_sql("select * from ssfprice where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'", con=engine)
print(p2)