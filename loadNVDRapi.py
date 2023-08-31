import json
import sqlite3
import pandas as pd
import config
import numpy as np
import requests
import sys

from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])

sSource = "api"
if sSource=="file":
    with open('./data/NVDRstock-trading31-01-23.json','r') as f:
        data = json.loads(f.read())
elif sSource=="api":
    url = 'https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol'
    #r = requests.get('https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol')
    #url = 'https://www.set.or.th/api/set/nvdr-trade/stock-trading?sortBy=symbol&date=09/03/2023'
    headers = {
        'Content-Type': 'application/json',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th',
        'Referer' : 'https://www.set.or.th/th/market/statistics/nvdr/trading-by-stock',
        'Cookie': 'first_user_visit=2022-04-22T07:53:55.134+07:00; _fbp=fb.2.1650982553450.869229828; clientUuid=bdf24f34-fd40-4e24-8357-66ec61994c0f; SET_COOKIE_POLICY=20220826121703; exp_history={"go_expid":"PK7lCwnwQ9aCptaRi7cQsw","msgt":"popup","count":1}|{"go_expid":"0DR_O1RjTXKxa4v1ZWGzSg","msgt":"footerbanner","count":2}|{"go_expid":"5xhLwqZcT2K1C6YEAngupw","msgt":"popup","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w","msgt":"popup","count":1}|{"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"cVRrr1SkS_euqRqxvDUGpA","msgt":"footerbanner","count":3}|{"go_expid":"vZj2v2cjSuCT8gIzugw5hw","msgt":"new_highlight","count":1}; lifetime_session=38; _ga_ET2H60H2CB=deleted; _tt_enable_cookie=1; _ttp=GGM1jHNHCUiqiMU6oEyhTKcx58_; _ga_ET2H60H2CB=deleted; visid_incap_2771851=tj7sxnxiRnepb+4CquDDZHMAQWQAAAAAQUIPAAAAAAAGdpoKm6+BJTgjQQgiuSoJ; visid_incap_2685219=TQS67KmIS7+/k3v8kEBjahnjQWQAAAAAQUIPAAAAAABavm8RciSKYIXRNHu6nEX2; _gcl_au=1.1.1883776542.1682302702; recent-search=%5B%22KKP%22%2C%22TKN%22%2C%22CPN%22%2C%22STGT%22%2C%22BEM%22%2C%22TVO%22%2C%22GLOBAL%22%5D; visid_incap_2046605=F5y/6M6FSOiQPiC22VbmbHMAQWQAAAAAQkIPAAAAAACAx+yrATHnKmQi2KQyvFrz4sXX4ohYBw7Q; my-quote=%5B%22STARK%22%2C%22AH%22%2C%22EGCO%22%2C%22SCGP%22%2C%22KKP%22%2C%22BBL%22%2C%22M%22%2C%22TPIPP%22%2C%22TKN%22%2C%22TRUE%22%2C%22BDMS%22%2C%22BCPG%22%2C%22CPN%22%2C%22TVO%22%2C%22STGT%22%2C%22GLOBAL%22%2C%22BGRIM%22%2C%22BEM%22%2C%22ADVANC%22%2C%22JMT%22%5D; nlbi_2046605=BqG3WKEQrgYi9aLcx+ze1wAAAAB0BWm6NeRrcgU80abghdn/; _cbclose=1; _cbclose23453=1; incap_ses_501_2771851=kZM7I2ImFDO5L9ZZwenzBuyktGQAAAAAjzBQSFJj8nw4OApimOPNYg==; nlbi_2685219=3sWDQkAIc2xyJv5MJHvigwAAAAASJ2eW7yg0P/LKgr1Juak0; incap_ses_501_2685219=o2MfYGGHOhHuV+NZwenzBk+utGQAAAAAppyz13SKebEpbFj5vDCvCw==; incap_ses_501_2046605=OnPwV/9lenfCWONZwenzBlCutGQAAAAAf4SiIshOHg/4aa8Ke9QeCw==; incap_ses_961_2046605=pAZPXLFIvCipBWteWClWDeYvt2QAAAAA8n2WQGOE3g0niqzd6+T1Ug==; _gid=GA1.3.1041687549.1689823060; charlie=42a30d40-c5ce-49c1-883e-923e66a4258d; route=1d47dbe8563e165d38d06ac6d2f1ea46; incap_ses_957_2685219=viDZVhrVQisuPS5sfvNHDfPauWQAAAAAc+1yu8xU5+tDDZ2HlRp4Xg==; uref=7253157; id=KqKgOXZeJxapT8k8AL1rOg%3D%3D00000000; incap_ses_957_2046605=owdwStXu+WNZBXtsfvNHDQ7/uWQAAAAABXoPni/lIrY+utJZi40aSw==; bull-popup-hidden=1; incap_ses_957_2771851=I3zyWHQzkgXLn4xtfvNHDdJKumQAAAAAthoFmHPx8krB6AILEUrYtA==; incap_ses_1007_2046605=eZd8BGgKHmIX+5xfcJj5DeVKu2QAAAAAEjOe6fkzkNss9gyb8CzFiQ==; _uid23453=01F8D841.355; _ctout23453=1; landing_url=https://www.set.or.th/th/market/statistics/short-sell; incap_ses_1007_2771851=fkkMCcRJD2cXFaBfcJj5DX9Ru2QAAAAA7o+9YyvBVDpjLTkfrrNFRQ==; _ga=GA1.3.1319572553.1630812666; _ga_ET2H60H2CB=GS1.1.1689997629.109.1.1689997983.60.0.0; nlbi_2663994_2540197=tlDhU6MUmWhza064ohrIEgAAAABGRmjG517Nz1S+ZMcmdq4S; visid_incap_2663994=p1qC7plNQnCGsNrdhZI+/bJSu2QAAAAAQUIPAAAAAAA3Nos6bJvfUQHIJ0NKLDus; incap_ses_1006_2663994=rPwOW+TmnWr3+8jYJAr2DbJSu2QAAAAAy2ebaU5+QfHxmOiv3TbRFA==; api_call_counter=4'
        }
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        data = r.json()
    else:
        print("Error from server: " + str(r.content))
        exit

#df = pd.json_normalize(r.json(), record_path =['nvdrTradings'])

cdate = pd.DataFrame(data).iloc[0].astype(str).str[:10]['date']
#df.info()
print(cdate)
df = pd.json_normalize(data, record_path =['nvdrTradings'])
df.drop(['buyVolume', 'sellVolume','netVolume', 'totalVolume','underlyingVolume', 'percentVolume'], axis=1, inplace=True)


#print(df)
df.rename(columns = {'date': 'trddate', 'buyValue': 'buy', 'sellValue': 'sell', 'netValue': 'net', 'totalValue': 'total', 'percentValue': 'percent', 'underlyingValue':'trdvalue'}, inplace = True)
df['ft']=df['total']/df['trdvalue']*100
df['ft'].round(2)
#df.info()
print(df)
sql = "select * from snvdr where trddate = '"+ cdate + "'"
print(sql)
df = df.loc[~((df['buy'] == '-') | (df['sell'] == '-') | (df['net'] == '-'))]
print(df)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='snvdr', con=engine, if_exists='append')
cur = engine.connect()
cur.execute("DELETE FROM snvdrsum")
cur.execute("INSERT into snvdrsum(Symbol, sumn, counts) select symbol,round(sum(net)) as sumn,count(symbol)counts from snvdr group by symbol")
