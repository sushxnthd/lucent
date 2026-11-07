'use strict';
// Independent Node.js LCG, exposure integrator and affine least-squares fit.
// Research-only synthetic replay, never a physical camera or human certification.
const assert = require('node:assert/strict');
function code(seed){
 let x=seed>>>0, out=[];
 for(let i=0;i<800;i++){x=(Math.imul(1664525,x)+1013904223)>>>0;out.push(x>>>31)}
 return out;
}
function mean(a){return a.reduce((p,c)=>p+c,0)/a.length}
function average(s,t,e){return mean(s.slice(t,t+e))}
function observations(s){let z=[];for(let f=0;f<20;f++)for(let r=0;r<2;r++)z.push([f,r,0.2+0.65*average(s,33*f+7+5*r,8)]);return z}
function fit(s,z){let candidates=[];
 for(let phase=0;phase<=20;phase++)for(let e of [4,8,12])for(let d of [0,5,10]){
  let xs=z.map(([f,r])=>average(s,33*f+phase+r*d,e)), ys=z.map(v=>v[2]);
  let mx=mean(xs),my=mean(ys),varx=xs.reduce((a,v)=>a+(v-mx)**2,0);
  if(varx<1e-12)continue;
  let gain=xs.reduce((a,v,i)=>a+(v-mx)*(ys[i]-my),0)/varx;
  if(gain<=0)continue;
  let offset=my-gain*mx;
  let rmse=Math.sqrt(mean(xs.map((v,i)=>(ys[i]-offset-gain*v)**2)));
  candidates.push({phase,e,d,rmse});
 }
 candidates.sort((a,b)=>a.rmse-b.rmse||a.phase-b.phase||a.e-b.e||a.d-b.d);
 return candidates;
}
const s=code(20261030), a=fit(s,observations(s));
assert.deepEqual([a[0].phase,a[0].e,a[0].d],[7,8,5]);
assert.ok(a[0].rmse<1e-12 && a[1].rmse-a[0].rmse>0.004);
const p=Array.from({length:800},(_,i)=>Number(i%4>=2));
for(let f=0;f<20;f++)for(let r=0;r<2;r++)assert.equal(average(p,33*f+7+5*r,8),average(p,33*f+11+5*r,8));
let correct=0;for(let seed=0;seed<40;seed++){
 let q=code(seed),fitq=fit(q,observations(q));
 if(fitq[0].phase===7 && fitq[0].e===8 && fitq[0].d===5 && fitq[1].rmse-fitq[0].rmse>=.004)correct++;
}
assert.equal(correct,40);
console.log(JSON.stringify({independent:'PASS',truth:[7,8,5],clean_rmse:a[0].rmse,margin:a[1].rmse-a[0].rmse,heldout_correct:correct,periodic_alias:true}));
