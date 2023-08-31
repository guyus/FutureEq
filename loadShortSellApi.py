import json
import sqlite3
import pandas as pd
import config
import numpy as np
import requests

from sqlalchemy import create_engine
engine = create_engine('postgresql://'+config.db['user']+':'+config.db['password']+config.db['url'])
##--- SET CONFIG SOURCE
sSource = "api"
if sSource=="file":
    with open('./data/shortsales01-02-23.json','r') as f:
        data = json.loads(f.read())
elif sSource=="api":
    url = 'https://www.set.or.th/api/set/shortsales'
    headers = {
        'Content-Type': 'application/json',
        'Host': 'www.set.or.th',
        'Origin': 'https://www.set.or.th',
        'Referer' : 'https://www.set.or.th/en/market/statistics/short-sell',
        'Cookie': 'first_user_visit=2022-04-22T07:53:55.134+07:00; _fbp=fb.2.1650982553450.869229828; clientUuid=bdf24f34-fd40-4e24-8357-66ec61994c0f; SET_COOKIE_POLICY=20220826121703; exp_history={"go_expid":"PK7lCwnwQ9aCptaRi7cQsw","msgt":"popup","count":1}|{"go_expid":"0DR_O1RjTXKxa4v1ZWGzSg","msgt":"footerbanner","count":2}|{"go_expid":"5xhLwqZcT2K1C6YEAngupw","msgt":"popup","count":1}|{"go_expid":"5AD93i4KR9-ZVNOhL9Vr2w","msgt":"popup","count":1}|{"go_expid":"GusVq2U2QG2l2p9tGb5KTQ","msgt":"lightbox_exit_banner","count":1}|{"go_expid":"cVRrr1SkS_euqRqxvDUGpA","msgt":"footerbanner","count":3}|{"go_expid":"vZj2v2cjSuCT8gIzugw5hw","msgt":"new_highlight","count":1}; lifetime_session=38; _ga_ET2H60H2CB=deleted; _tt_enable_cookie=1; _ttp=GGM1jHNHCUiqiMU6oEyhTKcx58_; _ga_ET2H60H2CB=deleted; visid_incap_2771851=tj7sxnxiRnepb+4CquDDZHMAQWQAAAAAQUIPAAAAAAAGdpoKm6+BJTgjQQgiuSoJ; visid_incap_2685219=TQS67KmIS7+/k3v8kEBjahnjQWQAAAAAQUIPAAAAAABavm8RciSKYIXRNHu6nEX2; recent-search=%5B%22KKP%22%2C%22TKN%22%2C%22CPN%22%2C%22STGT%22%2C%22BEM%22%2C%22TVO%22%2C%22GLOBAL%22%5D; visid_incap_2046605=F5y/6M6FSOiQPiC22VbmbHMAQWQAAAAAQkIPAAAAAACAx+yrATHnKmQi2KQyvFrz4sXX4ohYBw7Q; my-quote=%5B%22STARK%22%2C%22AH%22%2C%22EGCO%22%2C%22SCGP%22%2C%22KKP%22%2C%22BBL%22%2C%22M%22%2C%22TPIPP%22%2C%22TKN%22%2C%22TRUE%22%2C%22BDMS%22%2C%22BCPG%22%2C%22CPN%22%2C%22TVO%22%2C%22STGT%22%2C%22GLOBAL%22%2C%22BGRIM%22%2C%22BEM%22%2C%22ADVANC%22%2C%22JMT%22%5D; uref=7253157; id=KqKgOXZeJxapT8k8AL1rOg%3D%3D00000000; bull-popup-hidden=1; _gcl_au=1.1.1909897484.1690160688; charlie=42a30d40-c5ce-49c1-883e-923e66a4258d; _gid=GA1.3.35014855.1690332575; nlbi_2046605=HsBZIpnGhFNyz/ivx+ze1wAAAADONFYdhunEP7t6Y0+5T+oq; incap_ses_899_2046605=r8wpV0NQ3QMnGxXMEuR5DLmrwWQAAAAA6977DFkHUW2+BduzZkY84g==; route=3d64b3424ad92089eaa38aa58222db78; _cbclose=1; _cbclose23453=1; _uid23453=01F8D841.361; _ctout23453=1; landing_url=https://www.set.or.th/th/market/statistics/short-sell; api_call_counter=4; display_expid={"popup":"5AD93i4KR9-ZVNOhL9Vr2w-V2"}; incap_ses_899_2771851=QAf0JNNvLEXzHhXMEuR5DMOrwWQAAAAAAaJ62u5xyidYWP83ZAmZqg==; _ga=GA1.3.1319572553.1630812666; _gat_UA-426404-8=1; _ga_ET2H60H2CB=GS1.1.1690413994.121.0.1690414033.21.0.0; nlbi_2663994_2540197=auSabyG3dSlR/JG4ohrIEgAAAAChEooRql0JA9r0TYLk4/qo; visid_incap_2663994=nhfQcc9UTcyTijUZp2Gxq+urwWQAAAAAQUIPAAAAAADcaYCasQU4I5M7Njetej39; incap_ses_1006_2663994=uUT0P/Bii1H5UT8nJwr2DeurwWQAAAAA1cORach1zh0Iz4CiX2lIMg=='
        }
    r = requests.get(url,headers=headers)
    #r = requests.get('https://www.set.or.th/api/set/shortsales')
    #https://www.set.or.th/api/set/shortsales?fromDate=09/03/2023&toDate=09/03/2023
    data = r.json()
    if r.status_code!=200:
        exit

#cdate = data['fromDate'][:10]
#d1.info()
print(data['fromDate'][:10])
df = pd.json_normalize(data['shortSales'])

df.info()
df.rename(columns = {'symbol': 'series', 'percentValue': 'per', 'percentVolume': 'perc'}, inplace = True)
df['trddate'] = data['fromDate'][:10] #pd.to_datetime('today').date() - pd.Timedelta("1 day")
#df.info()
print(df)
sql = "select * from sshortsell where trddate = '"+ data['fromDate'][:10] + "'"
print(sql)
rst = pd.read_sql(sql, con=engine)
print(len(rst.axes[0]))
if len(rst.axes[0]) == 0:df.to_sql(name='sshortsell', con=engine, if_exists='append')
print(df)