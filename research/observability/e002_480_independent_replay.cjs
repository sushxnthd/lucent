'use strict';
// E002-480 independent arithmetic replay; constructed instrument model only.
const assert=require('node:assert/strict');
const T=25/6,w=.006,u=.004,c=2.01525,l=.0005;
function hit(t) {
  for(let k=-1;k<=4;k++) {
    const a=c-l/2+k*T,b=a+l;
    if(Math.min(t+w,b)-Math.max(t,a)>1e-12) return true;
  }
  return false;
}
const counts={};
for(const n of [1,2,4,8]) {
  const step=.05/n,phases=Math.ceil(2*T/step-1e-12)+1;
  let unavoidable=0;
  for(let i=0;i<phases;i++) {
    const t=i*step;
    if(hit(t-u)&&hit(t+u)) unavoidable++;
  }
  assert.equal(unavoidable,0);
  counts[n]={phases,unavoidable};
}
assert.deepEqual([counts[1].phases,counts[2].phases,counts[4].phases,counts[8].phases],[168,335,668,1335]);
const oldCore=Math.max(0,w-2*u),newCore=w-.002,n=Math.ceil(T/newCore);
assert.equal(oldCore,0);
assert.equal(n,1042);
assert.ok(T/n<=newCore);
assert.ok(T/(n-1)>newCore);
const maxContrast=.2*l/w,noise=.002,threshold=.04;
assert.ok(maxContrast+noise<threshold);
console.log(JSON.stringify({independent_replay:'PASS',grid_counts:counts,
  old_core_ms:oldCore,improved_core_ms:newCore,min_even_phases_per_period:n,
  narrow_island_max_contrast:maxContrast,threshold_with_noise:threshold+noise,
  physical_validation:'NOT_ESTABLISHED'},null,2));
