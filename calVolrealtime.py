import json
import os

# JSON file
sFile = 'D:\\Downloads\\fileName.json'
sBakFile = 'D:\\Downloads\\fileNameBak.json'
file_exists = os.path.exists(sFile)
if file_exists:
    f = open (sFile, "r")
else:
    f = open (sBakFile, "r")

# Reading from file
data = json.loads(f.read())
#print(data)  
# Iterating through the json
# list
for i in data:
    bShow1 = 0
    bShow2 = 0
    print("------------------------------")
    if(i['val']>5):
        #print("off:{}".format(i['bov'][1]+i['bov'][3]+i['bov'][5]+i['bov'][7]+i['bov'][9]))
        #print(i['bo'])
        if ((float(i['percentBuyVolumn'])-float(i['percentSellVolumn']))>10) :
            print("Perc Buy Stock    [{:0} --- {:0}]".format(i['percentBuyVolumn'],i['percentSellVolumn'])) 
            bShow1 = 1
            if i['sectorbarBuy']>i['sectorbarSell']:   
                print("--Perc Buy Sector [{:0.02f} --- {:0.02f}]".format(i['sectorbarBuy'],i['sectorbarSell'])) 
                if i['marketbarBuy']>i['marketbarSell']: 
                    print("----Perc Buy Mkt  [{:0.02f} --- {:0.02f}]".format(i['marketbarBuy'],i['marketbarSell']))          
        if i['bov'][0]>i['bov'][1] and i['pchg']>=0:
            sStart = ""
            if (i['bov'][0]-i['bov'][1])/i['bov'][0]>=0.15:
                sStart = "*"
            if (i['bov'][0]-i['bov'][1])/i['bov'][0]>=0.30:
                sStart = "**"
            if (i['bov'][0]-i['bov'][1])/i['bov'][0]>=0.50:
                sStart = "***"                        
            print(" {} UP {:0,.0f} {:0,.0f}".format(sStart,i['bov'][0],i['bov'][1])) 

            bShow2 = 1
            if i['bov'][0]>i['bov'][3]:
                print(" --UP 2 {:0,.0f} {:0,.0f}".format(i['bov'][0],i['bov'][3])) 
                if i['bov'][0]+i['bov'][2]+i['bov'][4]+i['bov'][6]+i['bov'][8]>i['bov'][1]+i['bov'][3]+i['bov'][5]+i['bov'][7]+i['bov'][9]:
                    print(" ----UP 3 {:0,.0f} {:0,.0f}".format(i['bov'][0],i['bov'][2]))                     
        if bShow1==1 or bShow2==1:
            print("{} [{:0,.1f}] last: {:0,.2f}    pchg: {:0,.2f} %".format(i['symbol'],i['val'],i['last'],i['pchg']))
            volBid = i['bov'][0]+i['bov'][2]+i['bov'][4]+i['bov'][6]+i['bov'][8]
            volOff = i['bov'][1]+i['bov'][3]+i['bov'][5]+i['bov'][7]+i['bov'][9]
            sStart = ""
            if (volBid-volOff)/volBid>=0.10:
                sStart = "*"
            if (volBid-volOff)/volBid>=0.25:
                sStart = "**"
            if (volBid-volOff)/volBid>=0.40:
                sStart = "***"          
            print("    {} SUM bid: {:0,.0f} SUM off:{:0,.0f}".format(sStart, volBid, volOff))
            print("        {:d} b: {:0,.0f}  o: {:0,.0f}".format((i['bov'][0]>i['bov'][1]),i['bov'][0],i['bov'][1]))
            print("        {:d} b: {:0,.0f}  o: {:0,.0f}".format((i['bov'][2]>i['bov'][3]),i['bov'][2],i['bov'][3]))
            if bShow1==1 and bShow2==1:
                print("        {:d} b: {:0,.0f}  o: {:0,.0f}".format(i['bov'][4]>i['bov'][5],i['bov'][4],i['bov'][5]))
                print("        {:d} b: {:0,.0f}  o: {:0,.0f}".format(i['bov'][6]>i['bov'][7],i['bov'][6],i['bov'][7]))
                print("        {:d} b: {:0,.0f}  o: {:0,.0f}".format(i['bov'][8]>i['bov'][9],i['bov'][8],i['bov'][9]))        

# Closing file
f.close()
if os.path.exists(sFile):
    os.remove(sBakFile)
    os.rename(sFile,sBakFile)
os.system("pause")