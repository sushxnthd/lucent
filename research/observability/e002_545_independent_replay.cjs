'use strict';
// Independent whole-vector sign enumerator; never imports Python source.
const assert = require('node:assert/strict');
function replay(rows) {
  const n = rows.length, k = rows[0].length;
  const statistic = a => Math.max(...Array.from({length:k}, (_,j) => a.reduce((s,row)=>s+row[j],0)));
  const target = statistic(rows);
  let tail = 0;
  for(let mask=0;mask<2**n;mask++) {
    const flipped=rows.map((r,i)=>r.map(v=>(mask&(1<<i))?-v:v));
    if(statistic(flipped)>=target-1e-10*Math.max(1,Math.abs(target))) tail++;
  }
  return {tail,total:2**n};
}
const pos=Array.from({length:8},()=>Array(200).fill(1));
assert.deepEqual(replay(pos),{tail:1,total:256});
assert.deepEqual(replay(pos.map(r=>r.map(()=>0))),{tail:256,total:256});
const drift=Array.from({length:8},(_,i)=>Array.from({length:5},(_,j)=>(i+1)*(j%2?1:-0.3)+j*.01));
let rejected=0;
for(let mask=0;mask<256;mask++) {
 const rows=drift.map((r,i)=>r.map(v=>(mask&(1<<i))?-v:v));
 const {tail,total}=replay(rows);
 if(tail/total<=.05) rejected++;
}
assert.ok(rejected<=12);
console.log(JSON.stringify({positive_tail:1,zero_tail:256,null_rejected_of_256:rejected,independent_replay:'PASS'}));
