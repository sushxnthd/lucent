#!/usr/bin/env node
'use strict';
// Independent BigInt rational oracle for E002-596. No Python imports.
const assert=require('node:assert/strict');
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error('zero denominator');if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>Q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>a[0]*b[1]<b[0]*a[1]?-1:a[0]*b[1]>b[0]*a[1]?1:0;
const repr=a=>a[1]===1n?String(a[0]):String(a[0])+'/'+String(a[1]);
const zero=Q(0),half=Q(1,2),rate=Q(19,6),N=19;
function grid(phase){
  if(!Array.isArray(phase)||cmp(phase,zero)<0||cmp(phase,rate)>=0)throw Error('INVALID_PHASE');
  const out=[];
  for(let k=0;k<20;k++){
    const t=add(add(phase,mul(Q(k),rate)),half);
    const i=Number(t[0]/t[1]);
    if(i>=N)break;
    out.push(i);
  }
  return out;
}
function misses(indices,w){
  if(!Number.isInteger(w)||w<1||w>N)throw Error('INVALID_WIDTH');
  let count=0;
  for(let s=0;s<=N-w;s++)if(!indices.some(i=>i>=s&&i<s+w))count++;
  return count;
}
function audit(){
  const candidates=new Map();
  const insert=x=>{if(cmp(x,zero)>=0&&cmp(x,rate)<=0)candidates.set(repr(x),x);};
  insert(zero);insert(rate);
  for(let k=0;k<=N;k++)for(let i=0;i<=N;i++)insert(sub(Q(2*i+1,2),mul(Q(k),rate)));
  const b=[...candidates.values()].sort(cmp),seen=new Map();
  for(let j=0;j<b.length-1;j++)for(const p of [b[j],div(add(b[j],b[j+1]),Q(2))]){
    const g=grid(p);seen.set(g.join(','),g);
  }
  const sig=[...seen.values()].sort((a,b)=>a.join(',')<b.join(',')?-1:a.join(',')>b.join(',')?1:0);
  const integer=Object.fromEntries([0,1,2,3].map(i=>[String(i),grid(Q(i))]));
  const union=k=>[...new Set(Array.from({length:k},(_,i)=>integer[String(i)]).flat())].sort((a,b)=>a-b);
  const u3=union(3),u4=union(4);
  const missing=u=>Array.from({length:N},(_,i)=>i).filter(i=>!u.includes(i));
  const ext=(w,fn)=>fn(...sig.map(s=>misses(s,w)));
  return {
    experiment:'E002-596',evidence_tier:'EXACT_INDEX_ONLY',native_fps:95,nominal_fps:30,window_native_frames:N,
    integer_phases:integer,three_phase_union:u3,three_phase_unseen:missing(u3),
    four_phase_union:u4,four_phase_unseen:missing(u4),
    boundary_count:b.length,distinct_continuous_signatures:sig.length,
    signature_sample_count_range:[Math.min(...sig.map(x=>x.length)),Math.max(...sig.map(x=>x.length))],
    worst_missed_pulses_by_width:Object.fromEntries([1,2,3,4].map(w=>[String(w),ext(w,Math.max)])),
    best_missed_pulses_by_width:Object.fromEntries([1,2,3,4].map(w=>[String(w),ext(w,Math.min)])),
    critical_phases:b.map(repr),
    signatures:sig.map(s=>({indices:s,n:s.length,misses:Object.fromEntries([1,2,3,4].map(w=>[String(w),misses(s,w)]))})),
    human_anatomical_labels:0,physical_shutter_calibrations:0,product:'ABSTAIN_UNCALIBRATED',release:'BLOCKED'
  };
}
const r=audit();
assert.deepEqual(r.integer_phases['3'],[3,6,9,13,16]);
assert.deepEqual(r.four_phase_unseen,[]);
assert.equal(r.distinct_continuous_signatures,19);
assert.deepEqual(r.worst_missed_pulses_by_width,{'1':14,'2':8,'3':2,'4':0});
for(const p of [Q(-1),rate,Q(4)])assert.throws(()=>grid(p));
for(const w of [0,20,1.5,true])assert.throws(()=>misses([0,3],w));
console.log(JSON.stringify(r));
