import pandas as pd
import sqlite3
# Create your connection.
cnx = sqlite3.connect('EquityTrend.db')

df=pd.read_html('https://www.set.or.th/set/nvdrbystock.do?type=value&sort=total&language=en&country=US')
#df=pd.read_html('https://www.set.or.th/set/nvdrbystock.do?sort=&type=value&date=04%2F01%2F2021&language=en&country=US')
df=df[0]
df.columns = df.columns.droplevel()
df.rename(columns = {'%*':'Percent'}, inplace = True)
#df = df.drop(df.columns[[1,2]],axis='columns')
df['TrdDate'] = pd.to_datetime('today').date()
df['TrdDate'] = df['TrdDate'].apply(pd.DateOffset(-1)).apply(lambda x : x.date())
sql = "select * from sNVDR where TrdDate = '"+ df.iloc[0,6].strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, cnx)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sNVDR', con=cnx, if_exists='append')
cur = cnx.cursor()
cur.execute("DELETE FROM sNVDRsum")
cur.execute("INSERT into sNVDRsum(Symbol, sumN, counts) SELECT Symbol, sumN, counts FROM NVDRsum")
cnx.commit()
print(df)