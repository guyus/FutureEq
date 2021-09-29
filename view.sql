BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "CheckSymbol" (
	"Symbol"	TEXT,
	"StatusAnalysis"	TEXT
);
INSERT INTO "CheckSymbol" ("Symbol","StatusAnalysis") VALUES ('WHA',NULL),
 ('SCB',NULL),
 ('AEONTS',NULL),
 ('CPF','D'),
 ('CPN','R'),
 ('LH','R'),
 ('PTTGC','N'),
 ('TU',NULL),
 ('TISCO',NULL),
 ('GULF',NULL),
 ('MTC',NULL),
 ('CPALL',NULL),
 ('AOT',NULL),
 ('SCC',NULL),
 ('BTS',NULL),
 ('TOP',NULL),
 ('HMPRO',NULL),
 ('DELTA',NULL),
 ('PTTEP',NULL),
 ('PTT',NULL),
 ('TCAP',NULL),
 ('SPALI',NULL),
 ('BEM',NULL),
 ('CHG',NULL),
 ('ADVANC',NULL),
 ('STA',NULL),
 ('SAWAD',NULL),
 ('INTUCH',NULL),
 ('STGT',NULL),
 ('IRPC',NULL);
CREATE VIEW "TrendOI-vol" as
SELECT * FROM TrendOI
WHERE 
pOI>=0 AND
PriceR>=0 AND pFnet>=0 AND pVal>=0 AND
fnet1>0 AND V1>1.5
ORDER by pFTrate DESC;
CREATE VIEW "TrendOI-up" AS SELECT * FROM "main"."TrendOI" WHERE "Fnet1" >= 0  AND "pFnet" >= 0  ORDER BY "pFnet" DESC;
CREATE VIEW "TrendOI-short" AS 
SELECT * FROM "main"."TrendOI" WHERE  "pFTratenet" >= 0 AND"pFnet" <= 0  ORDER BY "ssR1" DESC;
CREATE VIEW "TrendOI-Sell" AS SELECT * FROM "main"."TrendOI" WHERE "Pchange" < 0  AND "pOI" >= 0  AND "pVol" >= -7  AND "pFnet" <= 0 AND "Fnet1" <= 0 ORDER BY "pFnet" ASC;
CREATE VIEW "TrendOI-Retreat" as
SELECT * FROM TrendOI
WHERE 
pOI>=-10 AND 
--V2>=V1 AND
--VF2<=VF1) AND 
PriceR<=0 AND 
pFnet>=0 AND pVal<=0 AND Fnet1>0
ORDER by pFnet DESC;
CREATE VIEW "TrendOI-Result" as
SELECT sPriceTemp.Pchange,(sPriceTemp.Pchange-TrendOI.Pchange) as DP, Round(Round(sPriceTemp.ValueTemp*1/100000)-TrendOI.V1,1) as DVx2, 
Round((ssfOITemp.VolTemp - TrendOI.VF1)*10/TrendOI.VF1) as DVF,
TrendOI.*  

FROM TrendOI 
 JOIN sPriceTemp ON TrendOI.Series=sPriceTemp.Series
 JOIN ssfOITemp ON TrendOI.Series=ssfOITemp.Series
 WHERE sPriceTemp.TrdDate = (SELECT DISTINCT TrdDate FROM sPriceTemp ORDER by TrdDate DESC  LIMIT 1 OFFSET 0) 
 AND ssfOITemp.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOITemp ORDER by TrdDate DESC  LIMIT 1 OFFSET 0) 
 ORDER by DVx2,sPriceTemp.Pchange DESC;
CREATE VIEW "NVDRsum" as
SELECT Symbol, round(sum(net)/1000000,1) as sumN, count(Symbol) as counts FROM "sNVDR" 
WHERE TrdDate >='2020-11-01'
GROUP BY Symbol
ORDER by sum(net) DESC;
CREATE VIEW OI1 AS 

SELECT ssfOI.Series,Close,Pchange,round((Close-Open)*100/Open,2) as PriceR, 

sPrice.Value,ssfOI.Vol,ssfOI.OI, Net as Fnet, 
ssfOI.Avg5,ssfOI.Avg10,
round(abs(sNVDR.Net)/sNVDR.Total*100,1) as FNrate, -- Ratio Net Per Total NVDR
round(abs(sNVDR.Net)/sPrice.Value/10,1) as FTrate, -- Ratio Net Per Total Vol
(round(round((ssfOI.OI),2)/((ssfOI.Vol)),2)) as OIratio, sShortSell.Per, sShortSellR.Per as PerR

FROM ssfOI 
JOIN sPrice On (replace(sPrice.Series,' <XD>','') = ssfOI.Series AND ssfOI.TrdDate = sPrice.TrdDate)
JOIN sNVDR On (ssfOI.Series = sNVDR.Symbol AND ssfOI.TrdDate = sNVDR.TrdDate)
LEFT JOIN sShortSell ON (sShortSell.Series = ssfOI.Series and sShortSell.TrdDate = ssfOI.TrdDate)
LEFT JOIN sShortSell as sShortSellR ON (sShortSellR.Series = (ssfOI.Series||'-R') and sShortSellR.TrdDate = ssfOI.TrdDate)
WHERE ssfOI.TrdDate =  
(SELECT DISTINCT replace(TrdDate,' 00:00:00','') FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0);
CREATE VIEW OI1pre AS 
SELECT ssfOI.Series,Close,Pchange,round((Close-Open)*100/Open,2) as PriceR,
--1 as FVratio,
Value,Vol,OI , 1 as FVratio, 1 as Fnet,
1 as FNrate, -- Ratio Net Per Total NVDR
1 as FTrate, -- Ratio Net Per Total Vol
--SELECT ssfOI.Series,Close,Pchange,round((Close-Open)*100/Open,2) as PriceR, round((Close-Open)*100/(sPrice.Open),2) as pChgP, round(Net/Vol/1000,1) as FVratio,
--Value,Vol,OI, Net as Fnet 
(round(round((ssfOI.OI),2)/((ssfOI.Vol)),2)) as OIratio
FROM ssfOI 
JOIN sPrice On (replace(sPrice.Series,' <XD>','') = ssfOI.Series AND ssfOI.TrdDate = sPrice.TrdDate)
--JOIN sNVDR On ssfOI.Series = sNVDR.Symbol
WHERE ssfOI.TrdDate =  
(SELECT DISTINCT replace(TrdDate,' 00:00:00','') FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0);
CREATE VIEW OI2 AS 

SELECT ssfOI.Series,Close,Pchange,round((Close-Open)*100/Open,2) as PriceR, 

sPrice.Value,ssfOI.Vol,ssfOI.OI, Net as Fnet,
ssfOI.Avg5,ssfOI.Avg10, 
round(abs(sNVDR.Net)/sNVDR.Total*100,1) as FNrate, -- Ratio Net Per Total NVDR
round(abs(sNVDR.Net)/sPrice.Value/10,1) as FTrate, -- Ratio Net Per Total Vol
(round(round((ssfOI.OI),2)/((ssfOI.Vol)),2)) as OIratio, sShortSell.Per, sShortSellR.Per as PerR
FROM ssfOI 
JOIN sPrice On (replace(sPrice.Series,' <XD>','') = ssfOI.Series AND ssfOI.TrdDate = sPrice.TrdDate)
JOIN sNVDR On (ssfOI.Series = sNVDR.Symbol AND ssfOI.TrdDate = sNVDR.TrdDate)
LEFT JOIN sShortSell ON (sShortSell.Series = ssfOI.Series and sShortSell.TrdDate = ssfOI.TrdDate)
LEFT JOIN sShortSell as sShortSellR ON (sShortSellR.Series = (ssfOI.Series||'-R') and sShortSellR.TrdDate = ssfOI.TrdDate)
WHERE ssfOI.TrdDate =  
(SELECT DISTINCT replace(TrdDate,' 00:00:00','') FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 1);
CREATE VIEW OI3 AS 

SELECT ssfOI.Series,Close,Pchange,round((Close-Open)*100/Open,2) as PriceR, 

sPrice.Value,ssfOI.Vol,ssfOI.OI, Net as Fnet, 
ssfOI.Avg5,ssfOI.Avg10,
round(abs(sNVDR.Net)/sNVDR.Total*100,1) as FNrate, -- Ratio Net Per Total NVDR
round(abs(sNVDR.Net)/sPrice.Value/10,1) as FTrate, -- Ratio Net Per Total Vol
(round(round((ssfOI.OI),2)/((ssfOI.Vol)),2)) as OIratio, sShortSell.Perc, sShortSellR.Perc as PercR
FROM ssfOI 
JOIN sPrice On (replace(sPrice.Series,' <XD>','') = ssfOI.Series AND ssfOI.TrdDate = sPrice.TrdDate)
JOIN sNVDR On (ssfOI.Series = sNVDR.Symbol AND ssfOI.TrdDate = sNVDR.TrdDate)
LEFT JOIN sShortSell ON (sShortSell.Series = ssfOI.Series and sShortSell.TrdDate = ssfOI.TrdDate)
LEFT JOIN sShortSell as sShortSellR ON (sShortSellR.Series = (ssfOI.Series||'-R') and sShortSellR.TrdDate = ssfOI.TrdDate)
WHERE ssfOI.TrdDate =  
(SELECT DISTINCT replace(TrdDate,' 00:00:00','') FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 2);
CREATE VIEW OI4 AS 

SELECT ssfOI.Series,Close,Pchange,round((Close-Open)*100/Open,2) as PriceR, 

sPrice.Value,ssfOI.Vol,ssfOI.OI, Net as Fnet, 
round(abs(sNVDR.Net)/sNVDR.Total*100,1) as FNrate, -- Ratio Net Per Total NVDR
round(abs(sNVDR.Net)/sPrice.Value/10,1) as FTrate, -- Ratio Net Per Total Vol
(round(round((ssfOI.OI),2)/((ssfOI.Vol)),2)) as OIratio, sShortSell.Perc, sShortSellR.Perc as PercR
FROM ssfOI 
JOIN sPrice On (replace(sPrice.Series,' <XD>','') = ssfOI.Series AND ssfOI.TrdDate = sPrice.TrdDate)
JOIN sNVDR On (ssfOI.Series = sNVDR.Symbol AND ssfOI.TrdDate = sNVDR.TrdDate)
LEFT JOIN sShortSell ON (sShortSell.Series = ssfOI.Series and sShortSell.TrdDate = ssfOI.TrdDate)
LEFT JOIN sShortSell as sShortSellR ON (sShortSellR.Series = (ssfOI.Series||'-R') and sShortSellR.TrdDate = ssfOI.TrdDate)
WHERE ssfOI.TrdDate =  
(SELECT DISTINCT replace(TrdDate,' 00:00:00','') FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 3);
CREATE VIEW SumOI as
SELECT * FROM ssfOI WHERE Series Like 'Single%' ORDER by TrdDate DESC;
CREATE VIEW "TrendOI" as
SELECT OI1.Series, Round((OI1.FTrate-OI2.FTrate)*100/abs(OI2.FTrate),1) as pFTrate ,
Round((OI1.Fnet - OI2.Fnet)*100/abs(OI2.Fnet),1) as pFnet,
Round((Round((OI1.OI-OI2.OI),2)*10/OI1.Vol)-(Round((OI2.OI-OI3.OI),2)*10/OI2.Vol),1) as pOIC,
(OI1.OI - OI2.OI)*100/OI2.OI as pOI, 
Round((OI1.Value - OI2.Value)*100/OI2.Value,1) as pVal, 
Round((OI1.PerR - OI2.PerR)*100/OI2.PerR,1) as pSR, 
OI1.PriceR,OI1.Pchange, sumN,
-- FOREIGN Multiple Factor
Round(OI4.FTrate*(OI4.Fnet/1000000)) as MF4, Round(OI3.FTrate*(OI3.Fnet/1000000)) as MF3,Round(OI2.FTrate*OI2.Fnet/1000000) as MF2, Round(OI1.FTrate*OI1.Fnet/1000000) as MF1,

-- FOREIGN Ratio Investment of Total Volumn
OI4.FTrate as FT4, OI3.FTrate as FT3,OI2.FTrate as FT2, OI1.FTrate as FT1,

-- FOREIGN Buy part
Round(OI4.Fnet/1000000,1) as Fnet4,Round(OI3.Fnet/1000000,1) as Fnet3,Round(OI2.Fnet/1000000,1) as Fnet2,Round(OI1.Fnet/1000000,1) as Fnet1, 

-- Avg FOREIGN Buy part
Round(OI1.Avg5/1000000,1) as FA5, Round(OI2.Avg10/1000000,1) as FA10,

-- Total Value
Round(OI3.Value/100000,1) as V3,Round(OI2.Value/100000,1) as V2,Round(OI1.Value/100000,1) as V1, 
-- sShortSell Part
OI2.Per as ss2,OI1.Per as ss1, OI2.PerR as ssR2, OI1.PerR as ssR1,

Round(Round((OI2.OI-OI3.OI),2)*10/OI2.Vol,2) as cOI2,Round(Round((OI1.OI-OI2.OI),2)*10/OI1.Vol,2) as cOI1,
OI3.Vol as VF3,OI2.Vol as VF2,OI1.Vol as VF1, OI3.OI as o3,OI2.OI as o2,OI1.OI as o1, 

--sPrice.Change, ROUND(sPrice.Close-sPrice.Open,2) as rPrice, sPrice.Close
Round(OI1.Pchange/abs(OI1.Fnet)*10000000,1) as PricepFNet, Round(OI1.Pchange/(ROUND((OI1.Fnet - OI2.Fnet)/abs(OI2.Fnet),1)),1) as ratio2
FROM OI1 
Join OI2 ON OI1.Series = OI2.Series
Join OI3 ON OI3.Series = OI1.Series
Join OI4 ON OI4.Series = OI1.Series
Join sNVDRsum ON sNVDRsum.Symbol = OI1.Series
--WHERE v1>1.5
--sPrice.TrdDate=(SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)

ORDER by	
pFTrate DESC, pOIC DESC;
CREATE VIEW "TrendOI-All" as
SELECT * FROM TrendOI
WHERE 
pOI>=0 AND pFnet>=0 AND pVal>=0 AND
fnet1>0 AND V1>1.5 AND FT1>10 AND ssR1<10 AND ss1<10
ORDER by pFTrate DESC;
CREATE VIEW "TrendOI-Avg-Buy" as
SELECT * FROM TrendOI
WHERE --pVal>=0 AND
FA5>FA10 AND Fnet1>FA5 AND V1>1 AND FT1>10 --AND ssR1<10 AND ss1<10
ORDER by pFTrate DESC;
CREATE VIEW "TrendOI-Avg-Sell" as
SELECT * FROM TrendOI
WHERE --pVal>=0 AND
FA5<FA10 AND Fnet1<FA5 AND V1>1 AND FT1>10 --AND ssR1<10 AND ss1<10
ORDER by pFTrate DESC;
CREATE VIEW "TrendOI-C-List" as
SELECT * FROM TrendOI
WHERE 
Series IN (SELECT Symbol FROM CheckSymbol);
CREATE VIEW "TrendOI-C-TopMCap" as
SELECT * FROM TrendOI
WHERE 
Series IN (SELECT Symbol FROM CheckTopMCAP);
CREATE VIEW "TrendOI-Cont-Buy" as
SELECT * FROM TrendOI
WHERE --pVal>=0 AND
Fnet1>0 AND Fnet2>0 AND V1>1 AND FT1>10 --AND ssR1<10 AND ss1<10
ORDER by pFTrate DESC;
CREATE VIEW "TrendOI-Cont-Sell" as
SELECT * FROM TrendOI
WHERE --pVal>=0 AND
Fnet1<0 AND Fnet2<0 AND V1>1 AND FT1>10 --AND ssR1<10 AND ss1<10
ORDER by pFTrate DESC;
CREATE VIEW "TrendOI-Rebound" as
SELECT * FROM TrendOI
WHERE 
pOI<=-5 AND 
--V2>=V1 AND
--VF2<=VF1) AND 
PriceR>=0 AND 
pVal<=0 AND Fnet1<0
ORDER by pFnet DESC;
COMMIT;
