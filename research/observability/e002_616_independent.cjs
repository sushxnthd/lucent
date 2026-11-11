'use strict';
// Independent exact floor-index phase oracle and bilateral run test for E002-616.
// No source archive or human rows in this verifier.
const assert = require('node:assert/strict');
function runs(rows) {
  const out=[]; let abstained=0;
  for(let i=0;i<rows.length;i++){
    if(!(rows[i].left && rows[i].right))continue;
    const a=i;
    while(i+1<rows.length && rows[i+1].id===rows[i].id+1 &&
          rows[i+1].left && rows[i+1].right)i++;
    const b=i;
    if(a===0 || b===rows.length-1){abstained++;continue;}
    const flank=rows.slice(a-1,b+2);
    if(flank.some((r,j)=>r.bad || (j && r.id!==flank[j-1].id+1))){
      abstained++;continue;
    }
    out.push([rows[a].id,rows[b].id]);
  }
  return {out,abstained};
}
function kept(first,last,p){
  const out=new Set();
  for(let k=0;;k++){
    const i=first+p+Math.floor(10*k/3);
    if(i>last)break;
    out.add(i);
  }
  return out;
}
function misses(first,last,a,b){
  return Array.from({length:10},(_,p)=>{
    const k=kept(first,last,p);
    for(let x=a;x<=b;x++)if(k.has(x))return false;
    return true;
  });
}
let checks=0;
for(let n=1;n<=8;n++){
  const v=misses(0,400,100,100+n-1).filter(Boolean).length;
  assert.equal(v,n===1?7:n===2?4:n===3?1:0);checks++;
}
const rows=Array.from({length:40},(_,i)=>({id:i,left:false,right:false,bad:false}));
for(let i=12;i<=14;i++){rows[i].left=true;rows[i].right=true;}
assert.deepEqual(runs(rows).out,[[12,14]]);checks++;
rows[13].right=false;
assert.deepEqual(runs(rows).out,[[12,12],[14,14]]);checks++;
rows[13].right=true;rows[13].bad=true;
assert.equal(runs(rows).abstained,1);checks++;
rows[13].bad=false;rows.splice(13,1);
assert.equal(runs(rows).abstained,2);checks++;
console.log(JSON.stringify({experiment:'E002-616',independent_js:'PASS',checks}));
