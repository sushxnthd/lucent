#!/usr/bin/env node
// E002-522 independent BigInt arithmetic and held-out finite-grid response replay.
// Does not import or call the Python evaluator. Synthetic instrument models only.
'use strict';
const assert = require('node:assert/strict');
const gcd = (a,b) => { while (b) [a,b]=[b,a%b]; return a; };
function f(n,d=1n) {
  if (d === 0n) throw Error('zero denominator');
  const g = gcd(n<0n?-n:n,d<0n?-d:d);
  if (d<0n) return [-n/g,-d/g];
  return [n/g,d/g];
}
const mul = (a,b) => f(a[0]*b[0],a[1]*b[1]);
const sub = (a,b) => f(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const div = (a,b) => f(a[0]*b[1],a[1]*b[0]);
const eq = (a,b) => assert.deepEqual(a,b);
const one=f(1n), theta=f(1n,5n), M=f(19n,100n);
const fraction=div(sub(one,div(M,theta)),f(2n));
eq(fraction,f(1n,40n));
eq(mul(fraction,f(8n)),f(1n,5n));
eq(div(sub(one,div(M,theta)),one),f(1n,20n));
eq(mul(div(sub(one,div(M,theta)),f(100n)),f(8n)),f(1n,250n));
// Independent exact sharpness: a=0 on p, theta+eps elsewhere;
// q=R on p, q_out on complement.
const eps=f(1n,1000000n);
const plus=f(theta[0]*eps[1]+eps[0]*theta[1],theta[1]*eps[1]);
const p=div(sub(one,div(M,plus)),f(2n));
const qOut=div(sub(one,mul(f(2n),p)),sub(one,p));
const mean=mul(mul(qOut,sub(one,p)),plus);
eq(mean,M);
assert(p[0]*fraction[1]>fraction[0]*p[1]);
assert((p[0]*fraction[1]-fraction[0]*p[1])*10000n < p[1]*fraction[1]);
// Held-out integer-weight response experiment; independent of Python PRNG.
let state=0x5222026 >>> 0;
const rand=() => {state ^= state << 13;state ^= state >>> 17;state ^= state << 5;return state>>>0;};
let qualified=0, tested=0;
for(let trial=0;trial<5000;trial++){
  const n=[8,16,32][rand()%3], weights=[], aperture=[];
  for(let i=0;i<n;i++){weights.push(BigInt(rand()%101));aperture.push(BigInt(rand()%31));}
  if(weights.every(w=>w===0n)) weights[0]=1n;
  const sumw=weights.reduce((x,y)=>x+y,0n);
  const maxw=weights.reduce((x,y)=>x>y?x:y,0n);
  let numerator=0n, closed=0n;
  for(let i=0;i<n;i++){
    numerator+=weights[i]*aperture[i];
    if(aperture[i]<=20n) closed++;
  }
  tested++;
  if(numerator>=20n*sumw) continue;
  // Direct algebra from p=count/n, M=sum(w_i*a_i)/(100 sumw),
  // theta=20/100, R=n*max(w_i)/sumw.
  assert(20n*closed*maxw >= 20n*sumw-numerator,
    'weighted shutter bound violated in held-out case '+trial);
  qualified++;
}
assert(qualified>1000);
console.log(JSON.stringify({status:'PASS',type:'synthetic_integer_instrument_replay',
  tested,qualified,uniform_ms:'2/5',R2_ms:'1/5',R100_ms:'1/250',
  external_human_evidence:false,physical_instrument_evidence:false}));
