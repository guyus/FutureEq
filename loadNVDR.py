import pandas as pd
import sqlite3
# Create your connection.
cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://classic.set.or.th/set/nvdrbystock.do?type=value&sort=total&language=en&country=US')
df=df[0]
df.columns = df.columns.droplevel()
df.rename(columns = {'%*':'Percent'}, inplace = True)
df = df.drop(df.columns[[1,2]],axis='columns')
df['TrdDate'] = pd.to_datetime('today').date()
#df['TrdDate'] = df['TrdDate'].apply(pd.DateOffset(-1))
sql = "select * from sNVDR where TrdDate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, cnx)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sNVDR', con=cnx, if_exists='append')
print(df)