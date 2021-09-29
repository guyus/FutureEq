import pandas as pd
#import sqlite3
# Create your connection.
#cnx = sqlite3.connect('EquityTrend.db')
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')

df=pd.read_html('https://www.settrade.com/C13_MarketSummary.jsp?detail=SET100&order=N&industry=&sector=&market=SET&sectorName=O_SET100')
df[3].rename(columns = {'หลักทรัพย์':'Series','เปิด':'Open','สูงสุด':'High','ต่ำสุด':'Low','ล่าสุด':'Close','เปลี่ยนแปลง':'Change','%เปลี่ยนแปลง':'Pchange',"มูลค่า('000 บาท)":'Value'}, inplace = True)
df1 = df[3]
df = df1.drop(df1.columns[[7,8,9]],axis='columns')
df['Series'] = df['Series'].apply(lambda x: x.replace(' <XD>',''))
df['Series'] = df['Series'].apply(lambda x: x.replace(' <XA>',''))
df['TrdDate'] = pd.to_datetime('today').date() - pd.Timedelta("1 day")
dT = pd.to_datetime('today').date() - pd.Timedelta("1 day")
#filter = df2["Series"]=="AAV"
sql = "select * from sPrice where TrdDate = '"+ dT.strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sPrice', con=engine, if_exists='append')
print(df)