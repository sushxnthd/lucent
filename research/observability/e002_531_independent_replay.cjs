// E002-531 independent Node.js replay, no Python imports or external dependencies.
'use strict';
const assert = require('node:assert/strict');
const n = 80, threshold = 0.25;
const A5 = Array(n).fill(5), B5 = A5.slice();
for (let k=0;k<9;k++) B5[30+k] = Math.abs(k-4);
const A=A5.map(x=>x/5), B=B5.map(x=>x/5);
const mask = s => s.map((v,i)=> i>=30 && i<=38 ? null : v);
const obsA = mask(A), obsB = mask(B);
assert.deepEqual(obsA, obsB);
const fill = s => {
  const out=s.slice();
  for(let i=30;i<=38;i++) out[i] = out[29] + (out[39]-out[29])*(i-29)/10;
  return out;
};
assert.deepEqual(fill(obsA), fill(obsB));
assert.equal(B.filter(v=>v<=threshold).length, 3);
const crossings = [];
for(let i=0;i<n-1;i++) {
  const x=B[i], y=B[i+1];
  if((x-threshold)*(y-threshold)<0) crossings.push(i+(threshold-x)/(y-x));
}
assert.equal(crossings.length, 2);
assert.equal(crossings[0], 32.75);
assert.equal(crossings[1], 35.25);
assert.equal((crossings[1]-crossings[0])/400, 1/160);
const count = (s,phase) => s.filter((v,i)=>i%16===phase && v<=threshold).length;
assert.equal(count(B,0),0);
assert.equal(count(B,1),1);
assert.equal(count(fill(obsB),1),0);
assert.equal(Math.max(...B5.slice(1).map((v,i)=>Math.abs(v-B5[i])))*80,80);
console.log('E002-531 independent Node replay PASS: same observed/imputed, 3 native witnesses, 6.25 ms, phase reversal, abstention');
