import pandas as pd
import http.client
import config
import json
import requests

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
# import sqlite3
# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')

#df=pd.read_html('https://www.tfex.co.th/api/set/tfex/marketlist/TXS_F/instrument-trading?tradeDateType=P')
#df=pd.read_html('ss15.html');

sSource = "api"
if sSource=="file":
    with open('./data/Pricecomposition02-02-23.json','r',encoding='utf-8') as f:
        data = json.loads(f.read())
elif sSource=="api":
    url = 'https://www.tfex.co.th/api/set/tfex/marketlist/TXS_F/instrument-trading?tradeDateType=P'
    headers = {
        'Referer':'https://www.tfex.co.th/th/market-data/daily-market-quotation/trading-quotation-by-series?instrumentType=TXS_F&instrumentClass=all&contractMonth=all&series=all&tradeDateType=P',
        'Cookie':'visid_incap_1430333=9bsubBq7SqWuvivTDOnh82WBQGUAAAAAQUIPAAAAAAAIEwv50ObdiMroGymjEvZ1; _gcl_au=1.1.1213552736.1698726337; _uid52571=EA06BE2D.7; _ga_4RC3LFML0H=GS1.1.1699579789.7.0.1699579790.59.0.0; _ga_4RC3LFML0H=deleted; __gads=ID=3cc14107813175fe:T=1698726356:RT=1699580282:S=ALNI_MbVcdCKMNVfv63w9dTjEcYjoZuGqw; __gpi=UID=00000c7ce0d377d8:T=1698726356:RT=1699580282:S=ALNI_MYMl7kmkt3BZCo0BKiEkeJUiMw8WQ; _ga_4RC3LFML0H=GS1.1.1699579789.7.1.1699580299.31.0.0; visid_incap_2942677=y+9IgSWOROSDY4TjQmMz0LeFUWUAAAAAQUIPAAAAAAC2ArCwWcRXZkwBks1uIgRf; _gid=GA1.3.2053564612.1699841517; SET_COOKIE_POLICY=20231111093657; nlbi_2942677=lQftTA2RHzzUwISdDnHfpwAAAAC81ngLFaLFqyM/0MpCGNgf; route=3d64b3424ad92089eaa38aa58222db78; recent-search=%5B%22cpn%22%5D; charlot=a05d673e-9819-4dcd-a25c-5b39a7de6df9; incap_ses_705_2942677=LMjKUZz9g1MtL4qVLKrICU8ZUmUAAAAAtko0yNYnEh9Ih1eOffGOyQ==; nlbi_2942677_2912505=OPf+BalCEg9Q37OODnHfpwAAAADoih55sijNlWRBa/eZBuwL; landing_url=https://www.tfex.co.th/th/market-data/daily-market-quotation/trading-quotation-by-series?instrumentType=TXS_F&instrumentClass=all&contractMonth=all&series=all&tradeDateType=P; _gat_UA-84943730-2=1; _ga=GA1.1.1200361762.1698726342; _ga_6WS2P0P25V=GS1.1.1699879264.11.1.1699881174.58.0.0; _ga_Q9HP7W8GYH=GS1.1.1699879264.4.1.1699881174.58.0.0',
        'Host': 'www.tfex.co.th',
        'Origin': 'https://www.tfex.co.th'
        }
    r = requests.get(url,headers=headers)
    #print('data:'+r.text)
    
    if r.status_code==200:
        data = r.json()
    else:
        print(r.status_code)
        exit
#---------- Data Process -------------------------------------
#print(data)
df = pd.json_normalize(data['instruments']) 
#print(df)
#df = df1[['Series','Vol','OI']]
df['symbol'] = df['symbol'].str[:-3]
df.rename(columns={'symbol': 'series', 'totalVolume': 'vol', 'totalOI': 'oi', 'tradingDate': 'trddate'}, inplace=True)
df = df[['series','vol','oi','trddate']]

keptDate = pd.to_datetime(df['trddate'].values[0]).date()
print(keptDate)

#---------- DB Insert -------------------------------------
from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])

sql = "select * from ssfoi where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='ssfoi', con=engine, if_exists='append')
p2 = pd.read_sql("select * from ssfoi where trddate = '"+ keptDate.strftime('%Y-%m-%d') + "'", con=engine)
print(p2)