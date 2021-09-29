import pandas as pd
import sqlite3
import sys

if len(sys.argv)>=2:multi = sys.argv[1]
#print(multi)
else:multi = 1
# Create your connection.
cnx = sqlite3.connect('EquityTrend.db')
df=pd.read_html('https://www.settrade.com/C13_MarketSummary.jsp?detail=SET100&order=N&industry=&sector=&market=SET&sectorName=O_SET100')
df[3].rename(columns = {'หลักทรัพย์':'Series','เปิด':'Open','สูงสุด':'High','ต่ำสุด':'Low','ล่าสุด':'Close','เปลี่ยนแปลง':'Change','%เปลี่ยนแปลง':'Pchange',"มูลค่า('000 บาท)":'Value'}, inplace = True)
df1 = df[3]
df = df1.drop(df1.columns[[7,8,9]],axis='columns')
df['Series'] = df['Series'].apply(lambda x: x.replace(' <XD>',''))
df['Series'] = df['Series'].apply(lambda x: x.replace(' <XA>',''))
df['TrdDate'] = pd.to_datetime('today').date()
df['ValueTemp'] = df['Value'].apply(lambda x: x*float(multi))
#filter = df2["Series"]=="AAV"
TrdDate = pd.to_datetime('today').strftime('%Y-%m-%d')
sql = "select * from sPriceTemp where TrdDate = '"+ TrdDate + "'"
print(sql)
rst = pd.read_sql(sql, cnx)
print(len(rst.axes[0]))
if len(rst.axes[0]) > 0:
    sql = "DELETE FROM sPriceTemp WHERE TrdDate='"+ TrdDate + "'"
    cur = cnx.cursor()
    cur.execute(sql)
    cnx.commit()
df.to_sql(name='sPriceTemp', con=cnx, if_exists='append')

print(df)