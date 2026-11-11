'use strict';
// Independent exact BigInt rational replay of E002-524 phase boundaries.
// No physiological labels, no actual camera timing.
const assert = require('node:assert/strict');
function gcd(a,b) {a=a<0n?-a:a; b=b<0n?-b:b; while(b){const t=a%b;a=b;b=t;} return a;}
function r(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<=0n)throw Error('denominator');const g=gcd(n,d);return [n/g,d/g];}
const add=(a,b)=>r(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>r(-a[0],a[1]);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>r(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>r(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>a[0]*b[1]<b[0]*a[1]?-1:a[0]*b[1]>b[0]*a[1]?1:0;
const eq=(a,b)=>cmp(a,b)===0;
const z=r(0),one=r(1),two=r(2),P=r(25,6),e=one,u=r(1,10),eps=r(1,100000);
const kP=k=>mul(r(k),P);
function overlap(d,phi){for(let k=-2;k<=6;k++){const start=add(phi,kP(k)),end=add(start,e);if(cmp(start,d)<0&&cmp(end,z)>0)return true;}return false;}
function full(d,phi,U=z){for(let k=-2;k<=6;k++){const start=add(phi,kP(k)),end=add(start,e);if(cmp(sub(start,U),z)>0&&cmp(add(end,U),d)<0)return true;}return false;}
const gap=sub(P,e),witness=add(P,e),robust=add(witness,mul(two,u));
assert(eq(gap,r(19,6))&&eq(witness,r(31,6))&&eq(robust,r(161,30)));
assert(!overlap(gap,gap));
assert(!full(witness,z));
assert(!full(robust,u,u));
const dMid=P,phiMid=div(add(sub(dMid,e),P),two);
assert(overlap(dMid,phiMid)&&!full(dMid,phiMid));
for(let i=0;i<257;i++){
 const phi=div(mul(P,r(i)),r(257));
 assert(overlap(add(gap,eps),phi));
 assert(full(add(witness,eps),phi));
 assert(full(add(robust,eps),phi,u));
}
const missing=add(mul(two,P),add(e,mul(two,u)));
assert(eq(missing,r(143,15)));
process.stdout.write(JSON.stringify({experiment:'E002-524',independent:'Node BigInt',phase_cases:257,
  exact_overlap_boundary:'19/6 ms',exact_full_boundary:'31/6 ms',
  exact_robust_full_boundary:'161/30 ms',
  exact_one_missing_frame_robust_boundary:'143/15 ms',
  result:'PASS',human_data:false})+'\n');
