--# Update SSFOI
--update ssfoi n set vol=(select vol from ssfoi s where s.series = n.series and s.trddate='2023-05-23') where n.trddate ='2023-05-25';
--delete from ssfoi where trddate = '2023-04-04';
--update ssfoi set trddate = '2023-05-25' where trddate = '2023-05-26';

--# Update SPRICE
--select l.series as sym ,(l.close - p.close) as close from sprice l, sprice p where l.trddate = '2023-05-24' and p.trddate = '2023-05-25' and l.series = p.series 
--update sprice m set change = (select (l.close - p.close) as close from sprice l, sprice p where l.trddate = '2023-05-24' and p.trddate = '2023-05-25' and l.series = p.series and l.series = m.series)
--where m.trddate = '2023-05-25' ;
--update sprice set ppricer = case when sprice.pricer=0 or sprice.pricer is null then 0 else round(1 / sprice.pricer , 2) end
--select series, pricer, round(pricer*10000000/(vol-lead(vol ,1) over (PARTITION BY series ORDER BY trddate desc)+1)::numeric ,1) as lagVal, trddate  
--from sprice where series ='MBK'
--select series, trddate, pricer,lagval,lagvaldif 
--, sum(round(lagval , 1)) OVER (PARTITION BY rm.series  ORDER BY rm.trddate) AS cum_net
--, sum(round(lagvaldif , 1)) OVER (PARTITION BY rm.series  ORDER BY rm.trddate) AS cumdif_net
--, sum(round(perv  , 1)) OVER (PARTITION BY rm.series  ORDER BY rm.trddate) AS cumPerv_net
--from ratio_momentum rm where series = 'CKP' and trddate >'2022-08-01' order by trddate desc 
--select series, trddate, pricer , ratio_pv
--, sum(round(ratio_pv  , 2)) OVER (PARTITION BY rm.series  ORDER BY rm.trddate) AS cum_net
--from ratio_momentum rm where trddate >'2022-08-01' order by trddate desc 
--delete from sprice  where trddate = '2023-12-05';
update sprice set trddate = '2023-12-15' where trddate = '2023-12-16'
--select symbol, sum(calvol) as tvol, sum(net) as tnet, round(sum(net)/sum(calvol),1) as tcost from snvdr s where  calvol <>0 and trddate >= '2021-01-01' group by symbol  --where symbol = 'AOT' symbol = 'BGRIM' and

--select symbol,net,calvol,round(net/(calvol+1)), round((s."open"+s."close")/2),nv.trddate  from snvdr nv left join sprice s on nv.symbol = s.series and nv.TrdDate=s.trddate where symbol = 'BGRIM' and calvol <>0
--select f.*,s."close",round((s."close"-f.tcost)*100/s."close",1) as profit,s.value  from fcost f inner join sprice s on f.symbol = s.series where s.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 0)
--and tcost < s."close"  
--UPDATE snvdr SET  
--ft=(SELECT round(abs(n1.net) / (s.value + 1::numeric) / 10::numeric, 1) as tf  
--FROM snvdr n1 inner join sprice s on n1.symbol = s.series and n1.TrdDate=s.trddate where n1.Symbol = snvdr.symbol AND n1.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 10)), 
--calvol=(SELECT round((n1.net) / ((s.open+s.close)/2::numeric), 1) as calvol   
--FROM snvdr n1 inner join sprice s on n1.symbol = s.series and n1.TrdDate=s.trddate where n1.Symbol = snvdr.symbol AND n1.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 10))  
--where snvdr.TrdDate = (SELECT DISTINCT TrdDate FROM ssfOI ORDER by TrdDate DESC  LIMIT 1 OFFSET 10)
--UPDATE snvdr nv SET 
--calvol = 0

--# Update sshortsell --
--UPDATE sshortsell SET trddate ='2023-08-02' where trddate = '2023-08-02';

--# Update SNVDR--
--UPDATE snvdr nv SET trddate ='2023-08-02' where trddate = '2023-08-02';
--UPDATE snvdr nv SET 
--calvol = round((nv.net) / ((s.open+s.close)/2::numeric), 1)
--FROM sprice s where nv.symbol = s.series and nv.TrdDate=s.trddate 
--and  nv.TrdDate = '2022-06-06' --and nv.TrdDate <= '2022-05-01'
--delete from snvdr n where n.trddate < '2021-10-01'
--select * from snvdr n where n.trddate < '2021-10-01'
--select * 
--FROM snvdr nv left join sprice s on nv.symbol = s.series and nv.TrdDate=s.trddate where  nv.TrdDate = '2022-06-08'

--select mc.series, mc.pricer,mc.ratio_pv, mc.cum_ratio , ma.avg_cum, oi.*  from ratio_momentum_cum mc join ratio_momentum_cum_avg ma on mc.series = ma.series and mc.trddate = current_date-1 
--join trendp_oi oi on oi.series  = ma.series 
--where mc.cum_ratio > ma.avg_cum and pval>oi.volavg5 and v1>0.5 and oi.pricer >=0

select ratio_pv ,ratio_pv1, toi.* from( 
select *,
	lead(ratio_pv) over (partition BY rm.series ORDER BY rm.trddate desc) as ratio_pv1  
from ratio_momentum rm 
where trddate > current_date -5
order by series) as tb join trendp_oi toi on toi.series = tb.series
where tb.ratio_pv > tb.ratio_pv1  and toi.volavg5 >=0.5 and (((toi.pval>0 or toi.v1>toi.volavg5) and toi.pricer>=0))-- or ((toi.pval<0 or toi.v1<toi.volavg5) and toi.pricer<0))
--and tb.ratio_pv>abs(ratio_pv1) --and tb.ratio_pv>=0 and ratio_pv1<=0
order by ratio_pv1,toi.poi desc 

