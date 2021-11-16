import pandas as pd
import sqlite3
import sys
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')

# Argrument
if len(sys.argv)>=2:multi = sys.argv[1]
else:multi = 1
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://www.tfex.co.th/tfex/dailyMarketReport.html?periodView=A&selectedDate=P&marketListId=SF&instrumentId=&go=GO&locale=en_US')

df=df[0]
tdate = df.iloc[:1,12].apply(lambda x: x.replace('Trading date: ',''))
tdate.values[0]
df1=df[df.Series.str.contains('Total',case=False)]

df2 = df1[['Series','Vol','OI']]
df2['Series'] = df2['Series'].apply(lambda x: x.replace(' Futures',''))
df2['Series'] = df2['Series'].apply(lambda x: x.replace('Total ',''))


#df2 = df1[['series','vol','oi']]
#print(df2)


#df2.loc[:,'series'] = df2.loc[:,'series'].apply(lambda x: x.replace(' Futures','',))
#df2.loc[:,'series'] = df2.loc[:,'series'].apply(lambda x: x.replace('Total ',''))
df2 = df2.apply(lambda x: x.replace('-',0))
df2.rename(columns={'Series': 'series', 'Vol': 'vol', 'OI': 'oi'}, inplace=True)
df2['voltemp'] = df2['vol'].apply(lambda x: int(x)*int(multi))
df2['oitemp'] = df2['oi']

#print(df2)
keptDate = pd.to_datetime(tdate.values[0]).date()
df2['trddate'] = pd.to_datetime(tdate.values[0]).date()

#filter = df2["Series"]=="AAV"
sql = "select * from ssfoitemp where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, engine)
print(len(rst.axes[0]))
print(df2)
#if len(rst.axes[0]) == 0:df2.to_sql(name='ssfOITemp', con=cnx, if_exists='append')
if len(rst.axes[0]) > 0:
    cur = engine.connect()
    sql = "DELETE FROM ssfoitemp where trddate ='"+ keptDate.strftime('%Y-%m-%d') + "'"
    cur.execute(sql)
    cur.close()

df2.to_sql(name='ssfoitemp', con=engine, if_exists='append')
p2 = pd.read_sql("select * from ssfoitemp where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'", engine)
print(p2)