#!/usr/bin/env node
'use strict';
// E002-615 independent BigInt virtual point-selector oracle.
// Synthetic controls only; not independent human annotation or camera evidence.
const assert = require('node:assert/strict');

function nearest(times, step, phase) {
  if (step <= 0n) throw Error('INVALID_STEP');
  if (!times.length) throw Error('EMPTY_TIMES');
  for (let i=1;i<times.length;i++)
    if (times[i] <= times[i-1]) throw Error('NONMONOTONIC_TIME');
  const t0=times[0], selected=new Set();
  for (let k=0n;;k++) {
    const target3=3n*t0+(3n*BigInt(phase)+10n*k)*step;
    if (target3 > 3n*times[times.length-1]) break;
    let low=0,high=times.length;
    while(low<high) {
      const mid=(low+high)>>1;
      if (3n*times[mid]<target3) low=mid+1;
      else high=mid;
    }
    let idx;
    if(low===0) idx=0;
    else if(low===times.length) idx=times.length-1;
    else idx=(target3-3n*times[low-1] <= 3n*times[low]-target3)?low-1:low;
    selected.add(idx);
  }
  return [...selected].sort((a,b)=>a-b);
}
const base=Array.from({length:40},(_,i)=>BigInt(i)*10n);
for(let p=0;p<10;p++) {
  assert.deepEqual(nearest(base,10n,p),
    nearest(base.map(t=>t*3n+71n),30n,p));
}
assert.deepEqual(nearest([0n,10n,20n],5n,1),[0]);
assert.deepEqual(nearest(base,10n,0),
  [0,3,7,10,13,17,20,23,27,30,33,37]);
assert.throws(()=>nearest([0n,0n,20n],10n,0),/NONMONOTONIC/);
const jitter=base.slice(); jitter[20]+=4n;
const intervals=jitter.slice(1).map((v,i)=>Number(v-jitter[i]));
assert.equal(intervals.filter(v=>Math.abs(v/10-1)>0.1).length,2);
console.log(JSON.stringify({experiment:'E002-615',independent_oracle:'PASS',
  exact_bigint_tests:5,source_human_validation:false}));
