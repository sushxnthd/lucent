// E002-286 analysis specification (frozen before outcomes)
const fs=require('fs');
function phaseCoverage(start,end,f,phases=128){const P=1e6/f;let hit=0;for(let i=0;i<phases;i++){let phi=i*P/phases;let rem=((start-phi)%P+P)%P;let wait=(P-rem)%P;if(wait<end-start)hit++;}return hit/phases}
function quantile(x,q){x.sort((a,b)=>a-b);let p=(x.length-1)*q,k=Math.floor(p);return x[k]+(x[Math.min(k+1,x.length-1)]-x[k])*(p-k)}
function analyze(id,raw){let lines=raw.trimEnd().split(/\r?\n/),h=lines[0].split('\t'),at=n=>h.indexOf(n);
let a=[];for(let line of lines.slice(1)){let c=line.split('\t'),t=+c[at('device_time_stamp_y')],x=+c[at('left_eye_openness_value')];if(Number.isFinite(t))a.push({t,x,v:c[at('left_eye_openness_validity')]==='1'&&x>0&&Number.isFinite(x),p:c[at('left_pupil_validity')]==='1'})}
let base=quantile(a.filter(z=>z.v).map(z=>z.x),.9),b=Array(a.length).fill(false),v=Array(a.length).fill(false);
for(let i=3;i<a.length-3;i++){let w=a.slice(i-3,i+4);if(w.every(z=>z.v)&&w.every((z,k)=>k===0||z.t-w[k-1].t<=5000)){v[i]=true;b[i]=quantile(w.map(z=>z.x),.5)<.55*base}}
let e=[];for(let i=4;i<a.length-4;){if(!b[i]){i++;continue}let j=i;while(b[j+1]&&a[j+1].t-a[j].t<=5000)j++;let s=(a[i-1].t+a[i].t)/2,z=(a[j].t+a[j+1].t)/2,d=(z-s)/1000;if(v[i-1]&&v[j+1]&&d>=30&&d<=600&&s-a[0].t>=500000&&a[a.length-1].t-z>=500000){let q={d};for(let f of [10,24,30,60]){q['p'+f]=phaseCoverage(s,z,f);q['theory'+f]=Math.min(1,d*f/1000)}q.missing=a.slice(i,j+1).filter(x=>!x.p).length/(j-i+1);e.push(q)}i=j+1}
let out={id,rows:a.length,baseline:base,n:e.length,median_d:e.length?quantile(e.map(x=>x.d),.5):null,lt33:e.filter(x=>x.d<1000/30).length,lt100:e.filter(x=>x.d<100).length,mean_pupil_missing:e.reduce((s,x)=>s+x.missing,0)/Math.max(1,e.length),freq:{}};
for(let f of [10,24,30,60])out.freq[f]={coverage:e.reduce((s,x)=>s+x['p'+f],0)/Math.max(1,e.length),theory:e.reduce((s,x)=>s+x['theory'+f],0)/Math.max(1,e.length),maxerr:Math.max(0,...e.map(x=>Math.abs(x['p'+f]-x['theory'+f])))};
return out}
if(require.main===module){console.log(JSON.stringify(process.argv.slice(2).map(a=>{let i=a.indexOf('=');return analyze(a.slice(0,i),fs.readFileSync(a.slice(i+1),'utf8'))}),null,2))}
module.exports={analyze,phaseCoverage};
