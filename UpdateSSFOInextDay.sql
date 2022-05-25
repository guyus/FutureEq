--update ssfoi n set vol=(select vol from ssfoi s where s.series = n.series and s.trddate='2022-02-28') where n.trddate ='2022-03-01';
delete from ssfoi where trddate = '2022-05-20';
--update ssfoi set trddate = '2022-02-28' where trddate = '2022-03-01';