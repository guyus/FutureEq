import pandas as pd

# Create your connection.

df=pd.read_html('http://siamchart.com/stock/')

#df[0].rename(columns = {'Securities':'Series','Volume (Shares)':'Volume','Turnover (Baht)':'Value','%Short Sale Volume Comparing with Auto Matching':'Per'},inplace = True)
#df[0]['TrdDate'] = pd.to_datetime('today').date()
#df=df[0]
df