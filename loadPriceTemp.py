import pandas as pd
import sqlite3
# Create your connection.
cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://www.settrade.com/C13_MarketSummary.jsp?detail=SET100&order=N&industry=&sector=&market=SET&sectorName=O_SET100')
df[3].rename(columns = {'หลักทรัพย์':'Series','เปิด':'Open','สูงสุด':'High','ต่ำสุด':'Low','ล่าสุด':'Close','เปลี่ยนแปลง':'Change','%เปลี่ยนแปลง':'Pchange',"มูลค่า('000 บาท)":'Value'}, inplace = True)
df1 = df[3]
df = df1.drop(df1.columns[[7,8,9]],axis='columns')
df['Series'] = df['Series'].apply(lambda x: x.replace(' <XD>',''))
df['TrdDate'] = pd.to_datetime('today').date()
#filter = df2["Series"]=="AAV"
sql = "select * from sPriceTemp where TrdDate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, cnx)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sPriceTemp', con=cnx, if_exists='append')
print(df)