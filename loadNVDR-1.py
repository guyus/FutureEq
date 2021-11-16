import pandas as pd
# import sqlite3
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')
df=pd.read_html('https://www.set.or.th/set/nvdrbystock.do?type=value&sort=total&language=en&country=US')
#df=pd.read_html('https://www.set.or.th/set/nvdrbystock.do?sort=&type=value&date=04%2F01%2F2021&language=en&country=US')
df=df[0]
df.columns = df.columns.droplevel()
df.rename(columns = {'Symbol':'symbol','Buy':'buy','Sell':'sell','Total':'total','Net':'net','%*':'percent'}, inplace = True)
#df = df.drop(df.columns[[1,2]],axis='columns')
df['trddate'] = pd.to_datetime('today').date()
df['trddate'] = df['trddate'].apply(pd.DateOffset(-1)).apply(lambda x : x.date())
sql = "select * from snvdr where trddate = '"+ df.iloc[0,6].strftime('%Y-%m-%d') + "'"
print(sql)
df = df.loc[~((df['buy'] == '-') | (df['sell'] == '-') | (df['net'] == '-'))]
print(df)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='snvdr', con=engine, if_exists='append')
cur = engine.connect()
cur.execute("DELETE FROM snvdrsum")
cur.execute("INSERT into snvdrsum(Symbol, sumn, counts) select symbol,round(sum(net)) as sumn,count(symbol)counts from snvdr group by symbol")

sqlAvg = "UPDATE snvdr SET ft= \
(SELECT round(abs(n1.net) / (s.value + 1::numeric) / 10::numeric, 1) as tf FROM snvdr n1 inner join sprice s on n1.symbol = s.series and n1.TrdDate=s.trddate where n1.Symbol = snvdr.symbol AND n1.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)) \
where snvdr.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)"
cur.execute(sqlAvg)

sqlAvg = "UPDATE ssfoi \
SET Avg5 = (SELECT round(avg(n1.Net)) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 5))) \
, Avg10 = (SELECT round(avg(n1.Net)) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 10))) \
, ftavg5 = (SELECT round(avg(n1.ft),1) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 5))) \
, ftavg10 = (SELECT round(avg(n1.ft),1) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 10))) \
WHERE ssfOI.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)"
cur.execute(sqlAvg)



cur.close()
print(df)