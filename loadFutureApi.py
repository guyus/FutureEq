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
        'Cookie':'visid_incap_3037351=OAxWdGjxR8+4gsHLvRckPI2rDGYAAAAAQUIPAAAAAABiJD9Kdf5rE/4hNI4/skdg; SET_COOKIE_POLICY=20231111093657; nlbi_3037351=JuB7LgIZjBrhMXfKCH0ekwAAAAAiZd7dWpqYghymfj7CwD7V; incap_ses_943_3037351=sdsAF07+KALuLDqyBTYWDYbOEmYAAAAAtcLY3LoXH+E/4GApwQgBNQ==; route=3d64b3424ad92089eaa38aa58222db78; _fbp=fb.2.1712508554664.1054006594; nlbi_3037351_2922083=AHhHLc4hXB7ISv7fCH0ekwAAAABgqt4MDGX6NYaYpefGzeKs; incap_ses_8085_3037351=RJO9KGW5Ui20p72FbbEzcLjOEmYAAAAAl4jBfPaGRjJNLc+jW32u9w==; incap_ses_630_3037351=hL3uG2QPMhHzJ2PoKza+CMLOEmYAAAAA7+SbvSTolVKzkWC/eD8QUA==; incap_ses_8225_3037351=fTBeZHs5+hfp71b2sRIlcgjPEmYAAAAA6ZEY2zwpTaX4Y212pM35pA==; incap_ses_705_3037351=13YkaEdBCgZGR0x9SKrICQLREmYAAAAAKuwmbPUDr6evFFbZvuttaw==; incap_ses_9067_3037351=BtFrJMQhGm+yZjpGMHXUfT7REmYAAAAAJPD8mgYrXh3soMEdcFf71Q==; incap_ses_1802_3037351=Ms4+c+Is0RQD3hSAhv0BGWA/E2YAAAAABTjlDFsE3Am42UtUavbSSA==; charlot=2f224438-0833-478c-a432-bfd361d96493; incap_ses_148_3037351=+P+zeExVnWjAuyxQvs0NAha6FmYAAAAAhRvkqJ5txATCFJImfHTp1g==; landing_url=https://www.tfex.co.th/th/market-data/daily-market-quotation/trading-quotation-by-series?instrumentType=TXS_F&instrumentClass=all&contractMonth=all&series=all&tradeDateType=P; _gid=GA1.3.2054919411.1712765466; _gat_UA-84943730-2=1; _ga_6WS2P0P25V=GS1.1.1712765469.4.0.1712765469.60.0.0; _ga=GA1.1.664471224.1712192584; _ga_Q9HP7W8GYH=GS1.1.1712765469.4.0.1712765469.60.0.0',
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