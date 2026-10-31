'use strict';
// Independent quarter-millisecond integer integration. No Python imports.
const assert = require('node:assert/strict');
const offsets = [1,1,3,0,1,2,2,2,1,3,2,2,0,0,2,0,0,2,2,1,0,0,2,3,2,3,3,0,3,2,1,1,1,0,3,0,2,2,3,2];
const widths = [6,2,4,2,5,3,6,3,4,3,6,6,2,2,3,6,6,3,3,5,6,4,6,2,6,6,2,2,4,6,2,4,5,2,2,5,5,4,2,6];
const pulses = offsets.map((v,k) => [BigInt(20*k+v), BigInt(20*k+v+widths[k])]);
const min=(a,b)=>a<b?a:b, max=(a,b)=>a>b?a:b;
function duty(tq, row, deltaq, exposureq, delayq, led=pulses) {
  const start=tq+deltaq+row*delayq, end=start+exposureq;
  let sum=0n;
  for (const [a,b] of led) sum+=max(0n,min(end,b)-max(start,a));
  return [sum,exposureq];
}
function matches(x,y) {
  const n=x[0]*y[1]-y[0]*x[1], den=x[1]*y[1];
  return (n<0n?-n:n)*50n<=den;
}
const truth=(i,row,led=pulses)=>duty(BigInt(i*40),BigInt(row),4n,8n,2n,led);
const ds=[-4n,0n,4n,8n], es=[4n,8n,12n], rs=[0n,2n,4n];
function feasible(led=pulses,truthFn=truth,onlyR=null) {
  const out=[];
  for(const d of ds) for(const e of es) for(const r of rs) {
    if(onlyR!==null && r!==onlyR) continue;
    let good=true;
    for(let i=0;i<10 && good;i++) for(const row of [0,2,4]) {
      if(!matches(duty(BigInt(i*40),BigInt(row),d,e,r,led),truthFn(i,row,led))) {good=false;break;}
    }
    if(good) out.push([d,e,r]);
  }
  return out;
}
const fit=feasible();
assert.equal(fit.length,1);
assert.deepEqual(fit[0],[4n,8n,2n]);
for(let i=10;i<20;i++) for(const row of [0,2,4]) {
  assert(matches(duty(BigInt(i*40),BigInt(row),...fit[0]),truth(i,row)));
}
assert.equal(feasible(pulses,truth,0n).length,0);
const steady=[[-20n,820n]];
const steadyTruth=(_i,_row)=>[1n,1n];
assert.equal(feasible(steady,steadyTruth).length,36);
const altered=[1n,10n];
assert(!matches(duty(400n,0n,...fit[0]),altered));
console.log(JSON.stringify({evidence:'synthetic_only',candidates:36,train_feasible:1,heldout_rows:30,steady_feasible:36,wrong_rolling_feasible:0,heldout_corruption_rejected:true,release:'BLOCKED'}));
