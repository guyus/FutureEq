var slist="";const stock= ["AAV","ADVANC","AEONTS","AMATA","AOT","AP","AWC","BA","BAM","BANPU","BAY","BBL","BCH","BCP","BCPG","BDMS","BEC","BEM","BGRIM","BH","BJC","BLA","BLAND","BPP","BTS","CBG","CENTEL","CHG","CK","CKP","COM7","CPALL","CPF","CPN","CRC","DELTA","DTAC","EA","EGCO","EPG","ERW","ESSO","GLOBAL","GPSC","GULF","GUNKUL","HANA","HMPRO","ICHI","INTUCH","IRPC","ITD","IVL","JAS","JMT","KBANK","KCE","KEX","KKP","KTB","KTC","LH","M","MAJOR","MBK","MEGA","MINT","MTC","OR","ORI","OSP","PLANB","PRM","PSH","PSL","PTG","PTT","PTTEP","PTTGC","QH","RATCH","RS","SAWAD","SCC","SCGP","SGP","SIRI","SPALI","SPRC","STEC","STGT","SUPER","TASCO","TCAP","THANI","THCOM","THG","TISCO","TKN","TOA","TOP","TPIPL","TPIPP","TQM","TRUE","TTA","TTB","TTCL","TTW","TU","TVO","VGI","VNG","WHA","WHAUP"];

async function callData(){
	var slist0="";
	for(let x in stock){
	await $.post("/webrealtime/data/fastquote.jsp", {
			symbol : stock[x],
			key : aj
		}, function(data) {
			//console.log(data);
			if(slist0=="") 
				slist0 = data;
			else
				slist0 = slist0 +","+ data;
			//const obj = JSON.parse(data);console.log(obj.symbol);
			//Object.assign(slist,{obj.symbol:data});
		});
	var sleept = Math.floor(Math.random(1000, 2000));
	setTimeout(function(){
    		console.log("Executed after %f second",sleept);
	}, sleept);

	}//console.log(slist0);

	return slist0;
}
callData().then(
	function(slist) {
		console.log("["+slist+"]");slist="["+slist+"]";
		var a = document.createElement("a");
		document.body.appendChild(a);
		var blob = new Blob([slist], {type: 'text/json'});
		url = window.URL.createObjectURL(blob);
		a.href = url;
        		a.download = "fileName.json";
        		a.click();
        		window.URL.revokeObjectURL(url);
	});