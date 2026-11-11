'use strict';
// Independent BigInt arithmetic; no Python implementation or precomputed fractions imported.
const assert = require('node:assert/strict');
function gcd(a,b){a=a<0n?-a:a; b=b<0n?-b:b; while(b){const r=a%b;a=b;b=r;}return a;}
function R(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g];}
function add(a,b){return R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);}
function sub(a,b){return R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);}
function mul(a,b){return R(a[0]*b[0],a[1]*b[1]);}
function div(a,b){return R(a[0]*b[1],a[1]*b[0]);}
function cmp(a,b){const x=a[0]*b[1]-b[0]*a[1];return x>0n?1:x<0n?-1:0;}
const floor=div(R(243n),R(983n,100n));
const theta=R(1n,5n);
const critical=div(mul(R(2n),sub(R(1n),theta)),floor);
assert.deepEqual(floor,R(24300n,983n));
assert.deepEqual(critical,R(1966n,30375n));
const f=R(1n,30n), w=R(1n,100n);
const expected=[R(7n,300n),R(17n,300n),R(9n,100n),R(37n,300n)];
for(let k=0;k<4;k++){
 const gap=sub(mul(R(BigInt(k+1)),f),w);
 assert.deepEqual(gap,expected[k]);
 assert.equal(cmp(gap,critical)>0,k>=2);
}
const exact=add(critical,w);
assert.equal(cmp(sub(exact,w),critical),0);
const twoMiss=sub(mul(R(3n),f),w);
const lower=sub(twoMiss,R(30n,1000n));
const upper=add(twoMiss,R(30n,1000n));
assert.equal(cmp(lower,critical)<0,true);
assert.equal(cmp(upper,critical)>0,true);
console.log('E002-568 independent BigInt: 13 exact assertions passed; structural no-go k>=2; product remains BLOCKED');
