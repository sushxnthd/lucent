#!/usr/bin/env node
// E002-539 independent exact-rational replay. No Python imports or floating point.
"use strict";
const assert = require("node:assert/strict");
function gcd(a,b) { a=a<0n?-a:a; b=b<0n?-b:b; while(b){const t=a%b;a=b;b=t;} return a||1n; }
function r(n,d=1n) { n=BigInt(n);d=BigInt(d);assert(d!==0n);if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g]; }
const add=(a,b)=>r(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>r(-a[0],a[1]);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>r(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>r(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
const fmt=a=>a[1]===1n?a[0].toString():a[0]+"/"+a[1];
const zero=r(0),two=r(2),eight=r(8);
function dip(D,V,A){
  const h=div(D,two);
  if(cmp(V,zero)===0||cmp(A,zero)===0)return zero;
  return cmp(V,mul(A,h))>=0 ? div(mul(A,mul(h,h)),two)
    : sub(mul(V,h),div(mul(V,V),mul(two,A)));
}
function check(fps,v,expected,ratio,exclusion){
  const d=r(1,fps),b=r(9,10),c=r(1,5),f=dip(d,r(v),r(6000));
  assert.equal(fmt(f),expected);
  const q=div(f,sub(b,c));
  assert.equal(fmt(q),ratio);
  assert.equal(cmp(q,r(1))<0,exclusion);
  return {fps,v,drop:fmt(f),ratio:fmt(q),conditional_exclusion:exclusion};
}
const results=[
  check(30,45,"93/160","93/112",true),
  check(30,60,"7/10","1",false),
  check(30,65,"117/160","117/112",false),
  check(240,45,"5/384","25/1344",true),
  check(15,45,"213/160","213/112",false),
];
assert(cmp(dip(r(1,30),r(45),r(6000)),r(3,4))<0);
assert(cmp(dip(r(1,30),r(45),r(6000)),r(5,6))<0);
console.log(JSON.stringify({experiment:"E002-539",independent:"Node.js BigInt",cases:results,product:"ABSTAIN_UNCALIBRATED",release:"BLOCKED"},null,2));
