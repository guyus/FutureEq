import os
import psycopg2
import logging
import sys
import webbrowser

# Argrument
# ex. python .\c-volprofiles.py -t:b
sType = "b"
def setArg(para,sType):
    sArg = para[para.find("-")+1:2]
    #print(sArg)
    #print(sys.argv[2].find("-")+2)
    if sArg=="t":
        sType = para[para.find("-")+3:]

    return sType

for x in sys.argv:
    sType= setArg(x,sType)

try:
    connection = psycopg2.connect(user="postgres",password="123", host="127.0.0.1",port="5432",database="EquityTrend")
    cursor = connection.cursor()
    if sType == "b":
        sql = "SELECT series FROM public.\"TrendOI_Avg_Buy\";"
    elif sType == "s":
        sql = "SELECT series FROM public.\"TrendOI_Avg_Sell\";"
    elif sType == "a":
        sql = "SELECT series FROM public.\"TrendOI_AvgAll\";"
    elif sType == "c":
        sql = "SELECT symbol FROM public.checksymbol;"
    elif sType == "t":
        sql = "SELECT series FROM public.trendoi-result WHERE dp>0;"
    elif sType == "u":
        sql = "SELECT series FROM public.\"TrendOI_AvgAll_Up\";"
    elif sType == "d":
        sql = "SELECT series FROM public.\"TrendOI_AvgAll_Dn\";"
    elif sType == "pre":
        sql = "SELECT x.* FROM public.trendp_oi_avg x ORDER BY x.pricer DESC,x.pval DESC;"
    elif sType == "v":
        sql = "SELECT x.* FROM public.trendoi x WHERE close > closeavg5 and v1 >volavg5 and fa5 >fa10 and fnet1 >fa10 and v1>1 and o1 >oiavg5  ORDER BY x.pricer DESC,x.pval DESC;"
    elif sType == "p":
        sql = "SELECT x.* FROM public.trendp_oi x WHERE pricer>0;"
    elif sType == "i":
        sql = "SELECT x.* FROM public.trendp_oi x WHERE pricer>0;"
    elif sType == "cb":
        sql = "SELECT series FROM public.\"TrendOI-Cont-Buy\";"
    elif sType == "dd":
        sql = "SELECT series FROM public.trendoi WHERE ft1>10 and fnet1 >0 and ((pval >0 and pricer  >0) or (pval  <0 and pricer <0)) and poi>=0;"

    if sType == "i":
        record = [['PTT'],['CPN'],['OR'],['TOA'],['CAPLL'],['RCL']]
    else:
        print(sql)
        cursor.execute(sql)
            # Fetch result
        record = cursor.fetchall()       

    for row in record:
        #print("c-volprofile.py -d:2021-08-02 -s:" + row[0])
        os.system("c-volprofile.py -d:2023-01-01 -s:" + row[0])
        webbrowser.open("https://stock.gapfocus.com/detail/" + row[0])
        webbrowser.open("https://www.tradingview.com/chart/SiqZg1n6/?symbol=SET%3A" + row[0])


except (Exception, psycopg2.Error) as error:
        #print("Error fetching data from PostgreSQL table =>", error)
        logging.exception(Exception)
finally:
    # closing database connection
    if connection:
            cursor.close()
            connection.close()