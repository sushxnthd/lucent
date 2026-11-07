#!/usr/bin/env node
// E002-587: independently regenerate constraints and verify primal/dual certificates.
// Does not call Python, SciPy, or the finite-grid optimizer.
'use strict';
const fs = require('fs');
const payload = JSON.parse(fs.readFileSync(0, 'utf8'));
const clip = x => Math.max(0, Math.min(1, x));
function observations(start) {
  const out = [];
  for (const r of [0,20,40]) for(let i=0;i<25;i++) {
    const p=i/2, y=clip((start+r*0.1+4-p)/4);
    out.push({r,p,y});
  }
  return out;
}
function constraints(obs,delta,epsilon) {
  const A=[],b=[];
  for(const {r,p,y} of obs) {
    const lo=Math.max(0,y-epsilon),hi=Math.min(1,y+epsilon);
    if(lo>0) {A.push([-1,-(1-lo),-r]);b.push(-p+delta);}
    if(hi<1) {A.push([1,1-hi,r]);b.push(p+delta);}
  }
  for(const [j,lo,hi] of [[0,0,4],[1,2,6],[2,0,0.2]]) {
    let a=[0,0,0];a[j]=1;A.push(a);b.push(hi);
    a=[0,0,0];a[j]=-1;A.push(a);b.push(-lo);
  }
  return {A,b};
}
function dot(a,b) {return a.reduce((s,x,i)=>s+x*b[i],0);}
let certificates=0;
for(const [name,start,delta,epsilon] of [['exact',2,0,0],['relaxed',2,.5,.1],['off_grid',2.17,0,0]]) {
  const data=payload[name], {A,b}=constraints(observations(start),delta,epsilon);
  if(data.constraint_count!==A.length) throw Error(name+':constraint count mismatch');
  for(let i=0;i<A.length;i++) {
    if(Math.max(...A[i].map((x,j)=>Math.abs(x-data.A[i][j])),Math.abs(b[i]-data.b[i]))>1e-10)
      throw Error(name+':constraint reconstruction mismatch '+i);
  }
  for(const r of [0,20,40]) {
    for(const [key,c] of [['min_start',[1,0,r]],['max_end_negated',[-1,-1,-r]]]) {
      const cert=data.certificates[String(r)][key];
      const x=cert.primal,lambda=cert.dual;
      if(x.length!==3 || lambda.length!==A.length) throw Error('bad dimensions');
      const primalMax=Math.max(...A.map((a,i)=>dot(a,x)-b[i]));
      const dualMax=Math.max(...lambda);
      const stationarity=Math.max(...c.map((v,j)=>Math.abs(v-A.reduce((s,a,i)=>s+a[j]*lambda[i],0))));
      const gap=Math.abs(dot(c,x)-dot(b,lambda));
      if(primalMax>1e-7 || dualMax>1e-7 || stationarity>1e-7 || gap>1e-7)
        throw Error(`${name} row ${r} ${key} primal=${primalMax} dual=${dualMax} stationarity=${stationarity} gap=${gap}`);
      certificates++;
    }
  }
}
const result={experiment:'E002-587', independent_replay:'PRIMAL_DUAL_CERTIFICATES_VERIFIED',
  certificates_verified:certificates, cases:['exact','relaxed','off_grid'],
  evidence_tier:'SYNTHETIC_CONTINUOUS_LP_ONLY',physical_certificate:false,
  product:'ABSTAIN_UNCALIBRATED',release:'BLOCKED'};
console.log(JSON.stringify(result));
