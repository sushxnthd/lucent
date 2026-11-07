'use strict';
// Independently reconstructed exact arithmetic; no Python imports or JSON fixtures.
const assert=require('node:assert/strict');
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
function r(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
const add=(x,y)=>r(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const neg=x=>r(-x[0],x[1]);
const sub=(x,y)=>add(x,neg(y));
const mul=(x,y)=>r(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>r(x[0]*y[1],x[1]*y[0]);
const eq=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const lt=(x,y)=>x[0]*y[1]<y[0]*x[1];
const V=r(25),F=r(1,30),W=r(1,100),H=sub(F,W),theta=r(1,5);
const a0=r(37,50),a1=r(49,100),amin=r(119,600);
const avg=div(add(a0,a1),r(2));
const naive=div(sub(mul(r(2),avg),mul(V,H)),r(2));
const exposurePenalty=div(mul(V,add(W,W)),r(2));
const correct=div(sub(sub(mul(r(2),avg),mul(V,H)),exposurePenalty),r(2));
const actualMin=sub(a1,div(mul(V,H),r(2)));
assert.ok(eq(avg,r(123,200)));
assert.ok(eq(naive,r(97,300)));
assert.ok(eq(correct,r(119,600)));
assert.ok(eq(actualMin,amin));
assert.ok(lt(amin,theta));
assert.ok(lt(theta,naive));
assert.ok(eq(sub(a0,a1),mul(V,W)));
assert.ok(eq(sub(a1,amin),div(mul(V,H),r(2))));
console.log(JSON.stringify({experiment:'E002-570',independent_exact_assertions:8,status:'PASS',product:'ABSTAIN_UNCALIBRATED'}));
