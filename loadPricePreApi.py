import json
import sqlite3
import pandas as pd
import config
import numpy as np
import requests
import sys
from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])

# Argrument
# ex. python .\c-volprofiles.py -m:2 multiply by 2
sMultiply = 2
def setArg(para,sType):
    sArg = para[para.find("-")+1:2]
    #print(sArg)
    #print(sys.argv[2].find("-")+2)
    if sArg=="m":
        sMultiply = para[para.find("-")+3:]
    return sMultiply

for x in sys.argv:
    sMultiply= setArg(x,sMultiply)

#f = open('./data/NVDRstock-trading31-01-23.json')
#data = json.load(f)
#data = pd.read_json('./data/NVDRstock-trading31-01-23.json')
# 'Accept': 'application/json',
#         'Host': 'www.set.or.th',
#         'Origin': 'https://www.set.or.th',
# 'Cookie': 'id=KqKgOXZeJxapT8k8AL1rOg%3D%3D00000000'
from http.client import HTTPConnection
HTTPConnection._http_vsn_str = 'HTTP/1.1'

sSource = "api"
if sSource=="file":
    with open('./data/Pricecomposition02-02-23.json','r',encoding='utf-8') as f:
        data = json.loads(f.read())
elif sSource=="api":
    url = 'https://www.set.or.th/api/set/index/set100/composition?lang=en'
    headers = {
        'Referer':'https://www.set.or.th/en/market/product/stock/search?market=set&index=SET100',
        'Cookie':'first_user_visit=2022-04-22T07:53:55.134+07:00; _fbp=fb.2.1650982553450.869229828; clientUuid=bdf24f34-fd40-4e24-8357-66ec61994c0f; SET_COOKIE_POLICY=20220826121703; exp_history={"go_expid":"PK7lCwnwQ9aCptaRi7cQsw","msgt":"popup","count":1}|{"go_expid":"0DR_O1RjTXKxa4v1ZWGzSg","msgt":"footerbanner","count":2}|{"go_expid":"5xhLwqZcT2K1C6YEAngupw","msgt":"popup","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w","msgt":"popup","count":1}|{"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"cVRrr1SkS_euqRqxvDUGpA","msgt":"footerbanner","count":3}|{"go_expid":"vZj2v2cjSuCT8gIzugw5hw","msgt":"new_highlight","count":1}; lifetime_session=38; _ga_ET2H60H2CB=deleted; _tt_enable_cookie=1; _ttp=GGM1jHNHCUiqiMU6oEyhTKcx58_; _ga_ET2H60H2CB=deleted; visid_incap_2771851=tj7sxnxiRnepb+4CquDDZHMAQWQAAAAAQUIPAAAAAAAGdpoKm6+BJTgjQQgiuSoJ; visid_incap_2685219=TQS67KmIS7+/k3v8kEBjahnjQWQAAAAAQUIPAAAAAABavm8RciSKYIXRNHu6nEX2; _gcl_au=1.1.1883776542.1682302702; recent-search=%5B%22KKP%22%2C%22TKN%22%2C%22CPN%22%2C%22STGT%22%2C%22BEM%22%2C%22TVO%22%2C%22GLOBAL%22%5D; visid_incap_2046605=F5y/6M6FSOiQPiC22VbmbHMAQWQAAAAAQkIPAAAAAACAx+yrATHnKmQi2KQyvFrz4sXX4ohYBw7Q; my-quote=%5B%22STARK%22%2C%22AH%22%2C%22EGCO%22%2C%22SCGP%22%2C%22KKP%22%2C%22BBL%22%2C%22M%22%2C%22TPIPP%22%2C%22TKN%22%2C%22TRUE%22%2C%22BDMS%22%2C%22BCPG%22%2C%22CPN%22%2C%22TVO%22%2C%22STGT%22%2C%22GLOBAL%22%2C%22BGRIM%22%2C%22BEM%22%2C%22ADVANC%22%2C%22JMT%22%5D; nlbi_2046605=BqG3WKEQrgYi9aLcx+ze1wAAAAB0BWm6NeRrcgU80abghdn/; _cbclose=1; _cbclose23453=1; incap_ses_501_2771851=kZM7I2ImFDO5L9ZZwenzBuyktGQAAAAAjzBQSFJj8nw4OApimOPNYg==; nlbi_2685219=3sWDQkAIc2xyJv5MJHvigwAAAAASJ2eW7yg0P/LKgr1Juak0; incap_ses_501_2685219=o2MfYGGHOhHuV+NZwenzBk+utGQAAAAAppyz13SKebEpbFj5vDCvCw==; incap_ses_501_2046605=OnPwV/9lenfCWONZwenzBlCutGQAAAAAf4SiIshOHg/4aa8Ke9QeCw==; incap_ses_961_2046605=pAZPXLFIvCipBWteWClWDeYvt2QAAAAA8n2WQGOE3g0niqzd6+T1Ug==; _gid=GA1.3.1041687549.1689823060; charlie=42a30d40-c5ce-49c1-883e-923e66a4258d; api_call_counter=5; route=1d47dbe8563e165d38d06ac6d2f1ea46; incap_ses_957_2685219=viDZVhrVQisuPS5sfvNHDfPauWQAAAAAc+1yu8xU5+tDDZ2HlRp4Xg==; uref=7253157; id=KqKgOXZeJxapT8k8AL1rOg%3D%3D00000000; incap_ses_957_2046605=owdwStXu+WNZBXtsfvNHDQ7/uWQAAAAABXoPni/lIrY+utJZi40aSw==; bull-popup-hidden=1; incap_ses_957_2771851=I3zyWHQzkgXLn4xtfvNHDdJKumQAAAAAthoFmHPx8krB6AILEUrYtA==; incap_ses_1007_2046605=Y6+7CdDT01NPbl5fcJj5DTqOumQAAAAAe53n1e/RN13ZCVRksp6/9w==; _uid23453=01F8D841.354; _ctout23453=1; landing_url=https://www.set.or.th/th/market/product/stock/search?market=set&index=SET100; _ga=GA1.1.1319572553.1630812666; incap_ses_1007_2771851=Xgc/BRK5d3c+g2xfcJj5DZKlumQAAAAA4b8xfZbOlYStDqspPnOMsQ==; _ga_ET2H60H2CB=GS1.1.1689952225.108.1.1689953890.60.0.0; nlbi_2663994_2540197=bApySKHAe1DAOEPjohrIEgAAAABGlpK09uHYZjTlZ9orcB94; visid_incap_2663994=zyGWQ23gTRCRD68n2teQs3amumQAAAAAQUIPAAAAAAD6Pk08JEZ7DxrjWclQm1hR; incap_ses_1006_2663994=zuzGDaGlPnUmhJDYJAr2DXamumQAAAAAR0Pt6jqEzjc1KztQcwalyg==',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th'
        }
    r = requests.get(url,headers=headers)
    #print('data:'+r.text)
    
    if r.status_code==200:
        data = r.json()
    else:
        print(r.status_code)
        exit

print(data['indexInfos'][0]['marketDateTime'][:10])
#cdate = pd.DataFrame(data).iloc[0].astype(str).str[:10]['date'], record_prefix=
#d1.info()
#print(cdate)
df = pd.json_normalize(data['composition']['stockInfos']) 
df.drop(['average', 'floor','ceiling', 'trVolume','trValue', 'aomVolume','aomValue', 'bids','offers'], axis=1, inplace=True)
df.rename(columns = {'symbol': 'series', 'last': 'close', 'percentChange': 'pchange','totalVolume': 'vol','totalValue': 'value'}, inplace = True)
df.drop(df.iloc[:, 11:],axis = 1, inplace=True)
df['value']=df['value']*sMultiply
df['vol']=df['vol']*sMultiply
df['trddate'] = data['indexInfos'][0]['marketDateTime'][:10] #pd.to_datetime('today').date() - pd.Timedelta("1 day")
#print(df['trddate'][0])
a = [0]
df = df[~df['close'].isin(a)]
df.info()
print(df)
# df['composition.stockInfos'].info()
# print(df['composition.stockInfos'])
sql = "select * from spricetmp where trddate = '"+ df['trddate'].astype(str)[0] + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='spricetmp', con=engine, if_exists='append')
p2 = pd.read_sql("select * from spricetmp where trddate = '"+ pd.to_datetime('today').strftime('%Y-%m-%d') + "'", con=engine)
print(p2)
len(df)