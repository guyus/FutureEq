import pandas as pd
# import sqlite3
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')

df=pd.read_html('https://www.settrade.com/C13_MarketSummary.jsp?detail=SET100&order=N&industry=&sector=&market=SET&sectorName=O_SET100')
df[3].rename(columns = {'หลักทรัพย์':'series','เปิด':'open','สูงสุด':'high','ต่ำสุด':'low','ล่าสุด':'close','เปลี่ยนแปลง':'change','%เปลี่ยนแปลง':'pchange',"มูลค่า('000 บาท)":'value'}, inplace = True)
df1 = df[3]
df = df1.drop(df1.columns[[7,8,9]],axis='columns')
df['series'] = df['series'].apply(lambda x: x.replace(' <XD>',''))
df['series'] = df['series'].apply(lambda x: x.replace(' <XA>',''))
df['trddate'] = pd.to_datetime('today').date()
#filter = df2["Series"]=="AAV"
sql = "select * from sprice where trddate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sprice', con=engine, if_exists='append')
print(df)