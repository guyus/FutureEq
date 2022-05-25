import pandas as pd
import http.client
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
# import sqlite3
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('http://www.tfex.co.th/tfex/dailyMarketReport.html?periodView=A&selectedDate=P&marketListId=SF&instrumentId=&go=GO&locale=en_US')
#df=pd.read_html('ss15.html');
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')
df=df[0]
print(df)
tdate = df.iloc[:1,12].apply(lambda x: x.replace('Trading date: ',''))
tdate.values[0]
df1=df[df.Series.str.contains('Total',case=False)]
print(df1)
df2 = df1[['Series','Vol','OI']]
df2['Series'] = df2['Series'].apply(lambda x: x.replace(' Futures',''))
df2['Series'] = df2['Series'].apply(lambda x: x.replace('Total ',''))
#df2['Series']=df2['Series'].replace(' Futures','')
#df2['Series']=df2['Series'].replace('Total ','')
df2 = df2.apply(lambda x: x.replace('-',0))
df2.rename(columns={'Series': 'series', 'Vol': 'vol', 'OI': 'oi'}, inplace=True)
keptDate = pd.to_datetime(tdate.values[0]).date()
df2['trddate'] = pd.to_datetime(tdate.values[0]).date()

print(df2)
#filter = df2["Series"]=="AAV"
sql = "select * from ssfoi where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df2.to_sql(name='ssfoi', con=engine, if_exists='append')
p2 = pd.read_sql("select * from ssfoi where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'", con=engine)
print(p2)