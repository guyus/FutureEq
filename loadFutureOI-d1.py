import pandas as pd
import sqlite3
import sys
# Argrument
if len(sys.argv)>=2:multi = sys.argv[1]
else:multi = 1
# Create your connection.
cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://www.tfex.co.th/tfex/dailyMarketReport.html?periodView=A&selectedDate=P&marketListId=SF&instrumentId=&go=GO&locale=en_US')

df=df[0]
tdate = df.iloc[:1,12].apply(lambda x: x.replace('Trading date: ',''))
tdate.values[0]
df1=df[df.Series.str.contains('Total',case=False)]

df2 = df1[['Series','Vol','OI']]
#print(df2)
df2.loc[:,'Series'] = df2.loc[:,'Series'].apply(lambda x: x.replace(' Futures','',))
df2.loc[:,'Series'] = df2.loc[:,'Series'].apply(lambda x: x.replace('Total ',''))
df2 = df2.apply(lambda x: x.replace('-',0))
df2['VolTemp'] = df2['Vol'].apply(lambda x: int(x)*int(multi))
df2['OITemp'] = df2['OI']

#print(df2)
keptDate = pd.to_datetime(tdate.values[0]).date()
df2['TrdDate'] = pd.to_datetime(tdate.values[0]).date()

#filter = df2["Series"]=="AAV"
sql = "select * from ssfOITemp where TrdDate = '"+ keptDate.strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, cnx)
print(len(rst.axes[0]))
print(df2)
#if len(rst.axes[0]) == 0:df2.to_sql(name='ssfOITemp', con=cnx, if_exists='append')
if len(rst.axes[0]) > 0:
    sql = "DELETE FROM ssfOITemp WHERE TrdDate='"+ keptDate.strftime('%Y-%m-%d') + "'"
    cur = cnx.cursor()
    cur.execute(sql)
    cnx.commit()

df2.to_sql(name='ssfOITemp', con=cnx, if_exists='append')
p2 = pd.read_sql("select * from ssfOITemp where TrdDate = '"+ keptDate.strftime('%Y-%m-%d') + "'", cnx)
print(p2)