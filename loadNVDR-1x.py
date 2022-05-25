import pandas as pd
# import sqlite3
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')

cur = engine.connect()
cur.execute("DELETE FROM snvdrsum")
cur.execute("INSERT into snvdrsum(Symbol, sumn, counts) select symbol,round(sum(net)) as sumn,count(symbol)counts from snvdr group by symbol")

sqlAvg = "UPDATE snvdr SET ft= \
(SELECT round(abs(n1.net) / (s.value + 1::numeric) / 10::numeric, 1) as tf FROM snvdr n1 inner join sprice s on n1.symbol = s.series and n1.TrdDate=s.trddate where n1.Symbol = snvdr.symbol AND n1.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)) \
where snvdr.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)"
#cur.execute(sqlAvg)

sqlAvg = "UPDATE ssfoi \
SET Avg5 = (SELECT round(avg(n1.Net)) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 5))) \
, Avg10 = (SELECT round(avg(n1.Net)) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 10))) \
, ftavg5 = (SELECT round(avg(n1.ft),1) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 5))) \
, ftavg10 = (SELECT round(avg(n1.ft),1) FROM sNVDR n1 WHERE (n1.Symbol = ssfOI.Series AND n1.TrdDate > (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 10))) \
WHERE ssfOI.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)"
#cur.execute(sqlAvg)



cur.close()
