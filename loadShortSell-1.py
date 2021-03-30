import pandas as pd
import sqlite3
# Create your connection.
cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://www.set.or.th/set/shortsales.do?language=en&country=US')

df[0].rename(columns = {'Securities':'Series','Volume (Shares)':'Volume','Turnover (Baht)':'Value',
'%Short Sale Volume Comparing with Auto Matching':'Per'},inplace = True)
df[0]['TrdDate'] = pd.to_datetime('today').date()


df=df[0]
df['TrdDate'] = df['TrdDate'].apply(pd.DateOffset(-1)).apply(lambda x : x.date())
df['Per']=df['Per'].apply(lambda x:x.replace(' %',''))
sql = "select * from sShortSell where TrdDate = '"+ df.iloc[0,4].strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, cnx)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sShortSell', con=cnx, if_exists='append')
print(df)