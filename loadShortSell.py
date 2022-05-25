# not use 

import pandas as pd
import sqlite3
# Create your connection.
cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://classic.set.or.th/set/shortsales.do?language=en&country=US')

df[0].rename(columns = {'Securities':'Series','Volume (Shares)':'Volume','Turnover (Baht)':'Value',
'%Short Sale Volume Comparing with Auto Matching':'Perc'},inplace = True)
df[0]['TrdDate'] = pd.to_datetime('today').date()
#df=df[0]['Value'].apply(lambda x:x.replace('%',''))
df=df[0]

sql = "select * from sShortSell where TrdDate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, cnx)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sShortSell', con=cnx, if_exists='append')
print(df)