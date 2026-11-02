'use strict';
// Independent finite-grid integer-sum verifier; does not import Python code.
const assert=require('node:assert/strict');
const bits='000100000010111001001001100001000101111111100111100010111001010111011100100111111111010111010010100111101011010000011001';
const code=[...bits].map(Number);
assert.equal(code.length,120);
const starts=[0,20,40,60,80];
function measure(f,r,o,e,d,arr=code){
  let total=0, start=f+o+r*d;
  for(let t=start;t<start+e;t++)total+=arr[t];
  return total/e;
}
const obs=[];
for(const f of starts)for(const r of [0,1,2])obs.push({f,r,v:measure(f,r,3,4,2)});
function find(samples,tol,arr=code){
  const matches=[];
  for(let o=0;o<=8;o++)for(let e=2;e<=8;e++)for(let d=0;d<=4;d++){
    if(samples.every(({f,r,v})=>Math.abs(measure(f,r,o,e,d,arr)-v)<=tol+1e-12))matches.push([o,e,d]);
  }
  return matches;
}
const fit=obs.filter(s=>s.f<=40),hold=obs.filter(s=>s.f>=60);
const strict=find(fit,.01),loose=find(fit,.1);
assert.deepEqual(strict,[[3,4,2]]);
assert.ok(loose.length>=strict.length);
assert.ok(strict.every(([o,e,d])=>hold.every(s=>Math.abs(measure(s.f,s.r,o,e,d)-s.v)<=.01)));
const flat=Array(120).fill(1),flatObs=[];
for(const f of starts.slice(0,3))for(const r of [0,1,2])flatObs.push({f,r,v:1});
assert.equal(find(flatObs,.01,flat).length,315);
const dropped=find(fit.slice(0,-1),.01);
assert.ok(dropped.length>=strict.length);
const clockShift=find(fit.map(s=>({...s,f:s.f+1})),.01);
assert.deepEqual(clockShift,[[2,4,2]]);
const reversed=find(fit.map(s=>({...s,r:2-s.r})),.01);
assert.equal(reversed.length,0);
console.log(JSON.stringify({experiment:'E002-607',independent:'PASS',strict_candidates:strict.length,loose_candidates:loose.length,constant_candidates:315,dropped_candidates:dropped.length,release:'BLOCKED'}));
