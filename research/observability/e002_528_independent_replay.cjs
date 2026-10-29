'use strict';
// Independent exact BigInt replay of E002-528; no Python imports.
const assert = require('node:assert/strict');
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b===0n)throw Error('zero denominator');if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>Q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const lt=(a,b)=>a[0]*b[1]<b[0]*a[1];
const clamp=x=>lt(x,Q(0))?Q(0):lt(Q(1),x)?Q(1):x;
const fmt=x=>x[0]+'/'+x[1];
function pFull(P,e,d,u){return clamp(div(sub(sub(d,e),mul(Q(2),u)),P));}
function overlap(P,e,d){return lt(Q(0),d)?clamp(div(add(d,e),P)):Q(0);}
const P=Q(25,6),e=Q(1),u=Q(1,10);
const cases=[['240_3',P,e,Q(3),u,Q(54,125)],['240_4',P,e,Q(4),u,Q(84,125)],['240_5_heldout',P,e,Q(5),u,Q(114,125)],['1000_1p2_heldout',Q(1),Q(1,2),Q(6,5),Q(0),Q(7,10)]];
for(const [name,p,ex,d,unc,want] of cases){assert.equal(fmt(pFull(p,ex,d,unc)),fmt(want),name);}
assert.equal(fmt(overlap(P,e,Q(4))),fmt(Q(1)));
const prob=pFull(P,e,Q(4),u),q=sub(Q(1),prob);
const three=sub(Q(1),mul(mul(q,q),q));
assert.equal(fmt(three),fmt(Q(1884204,1953125)));
assert.equal(fmt(clamp(sub(prob,Q(1,10)))),fmt(Q(143,250)));
assert.equal(fmt(clamp(add(prob,Q(1,10)))),fmt(Q(193,250)));
// Independent numeric lattice enumeration, with strict endpoints.
function brute(P,e,d,u,phi){
 for(let k=-2;k<=Math.floor(d/P)+2;k++){
  const a=phi+k*P;
  if(a-u>0 && a+e+u<d)return true;
 }
 return false;
}
for(const [name,p,ex,d,unc,want] of cases){
 const N=10000, pv=Number(p[0])/Number(p[1]),ev=Number(ex[0])/Number(ex[1]),dv=Number(d[0])/Number(d[1]),uv=Number(unc[0])/Number(unc[1]);
 let n=0;for(let j=0;j<N;j++)if(brute(pv,ev,dv,uv,pv*j/N))n++;
 const pred=Number(want[0])/Number(want[1]);
 assert.ok(Math.abs(n/N-pred)<=1/N+1e-12,name+': '+n+'/'+N+' != '+pred);
 console.log(name+' predicted='+fmt(want)+' grid='+n+'/'+N);
}
assert.equal(brute(25/6,1,4,0.1,3.5),false);
// Floating point cannot decide strict equality at this exact boundary.
// Recheck the adversarial phase using exact BigInt rationals.
function bruteExact(P,e,d,u,phi){
 for(let k=-2;k<=3;k++){
  const a=add(phi,mul(Q(k),P));
  if(lt(u,a) && lt(add(add(a,e),u),d))return true;
 }
 return false;
}
assert.equal(bruteExact(P,e,add(add(P,e),mul(Q(2),u)),u,u),false);
console.log('E002-528 independent BigInt exact + phase grid replay: PASS');
