'use strict';
// Independent exact BigInt arithmetic of frozen representative-parameter stress.
// Literature cohort means are NOT a continuous-time physiological hard ceiling.
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;};
const q=(a,b=1n)=>{if(b===0n)throw Error('zero denominator');if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];};
const mul=(x,y)=>q(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>q(x[0]*y[1],x[1]*y[0]);
const sub=(x,y)=>q(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const str=x=>x[1]===1n?String(x[0]):String(x[0])+'/'+String(x[1]);
const speed=div(q(243n),q(49n,5n));
const gap=fps=>sub(q(1n,BigInt(fps)),q(1n,1000n));
const ratio=fps=>div(mul(speed,gap(fps)),q(8n,5n));
const a=ratio(30),b=ratio(15);
if(str(speed)!=='1215/49'||str(a)!=='7857/15680'||str(b)!=='15957/15680')throw Error('independent rational disagreement');
if(!(a[0]<a[1]&&b[0]>b[1]))throw Error('crossing prediction failed');
console.log(JSON.stringify({experiment:'E002-536',method:'independent_node_bigint',normalized_speed_s_inverse:str(speed),ratio_30fps:str(a),ratio_15fps:str(b),physical_validated:false,product:'ABSTAIN_UNCALIBRATED',release:'BLOCKED'}));
