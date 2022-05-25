import plotly.graph_objects as go
#import sqlite3
import pandas as pd
#from plotly.subplots import make_subplots
import sys
# Argrument
# ex. python .\c-volprofile.py -s:ptt -d:2021-08-02 

from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:123@localhost:5432/EquityTrend')

sField = "net"
sStartDate = "2021-08-01"
multi = ""

def setArg(para,multi,sField,sStartDate):
    sArg = para[para.find("-")+1:2]
    #print(sArg)
    #print(sys.argv[2].find("-")+2)
    if sArg=="d":
        sStartDate = para[para.find("-")+3:]
    if sArg=="f":
        sField = para[para.find("-")+3:] 
    if sArg=="s":
        multi = para[para.find("-")+3:] 
    return multi,sField,sStartDate

for x in sys.argv:
    multi,sField,sStartDate = setArg(x,multi,sField,sStartDate)

if multi=="" :
    multi = input('Stock: ')

#print(sStartDate)
#print(sField)

# Create your connection.
# cnx = sqlite3.connect('EquityTrend.db')
sSQL= "select sPrice.*,sNVDR.Net from sPrice INNER JOIN sNVDR ON Series = Symbol AND sPrice.TrdDate = sNVDR.TrdDate WHERE (Series = '"+multi.upper()+"') AND sPrice.TrdDate >='"+sStartDate+"'"
print(sSQL)
dt = pd.read_sql(sSQL, engine)
#print(dt)
fig = go.Figure()
dfSum = dt['net'].cumsum()
fig.add_trace(go.Histogram(name='FNet Profile', x=dt[sField], y=dt['close'], nbinsy=70, histfunc='sum', marker_color='blue', orientation="h",visible=True,yaxis="y2", xaxis="x2"))
fig.add_trace(go.Histogram(name='Vol Profile', x=[x*100 for x in dt.value.to_list()], y=dt['close'], nbinsy=70, marker_color='yellow', histfunc='sum',orientation="h",visible=True,yaxis="y2", xaxis="x2"))
fig.add_trace(go.Bar(name='FNet Sum', x=dt['trddate'], y=dfSum, yaxis="y", xaxis="x", marker_color='black',visible=True))
fig.add_trace(go.Bar(name='value', x=dt['trddate'], y=[x*1000 for x in dt.value.to_list()],marker_color='blue', yaxis="y", xaxis="x",visible=True))
#fig.add_trace(go.Bar(name='Net', x=dt['TrdDate'], y=['Net'],marker_color='#00ffff', yaxis="y", xaxis="x",visible=True))
#fig.add_trace(go.Bar(name='Value', x=dt['TrdDate'], y=[x*100 for x in dt.Value.to_list()], yaxis="y", xaxis="x2",visible=True))
fig.add_trace(go.Candlestick(
            x=dt['trddate'],
            open=dt['open'],
            high=dt['high'],
            low=dt['low'],
            close=dt['close'],
            xaxis="x",
            yaxis="y2",
            visible=True,
            showlegend=False
        ))

layout=go.Layout(
        title=go.layout.Title(text="Candlestick With Volume Profile = "+multi.upper()),
        xaxis=go.layout.XAxis(
            side="top",title="Date",
            #range=[0, 90000000],
            rangeslider=go.layout.xaxis.Rangeslider(visible=True),
            showticklabels=True
        ),
        yaxis=go.layout.YAxis(
            side="left",
            title="Value",
            #range=[low, high],
            showticklabels=True
        ),
        xaxis2=go.layout.XAxis(
            side="bottom",
            title="Profile",
            rangeslider=go.layout.xaxis.Rangeslider(visible=False),
            overlaying="x"
        ),
        yaxis2=go.layout.YAxis(
            side="right",
            title="Price",
            #range=[low, high],
            overlaying="y"
        )
    )
fig.update_layout(layout)
fig.show()
