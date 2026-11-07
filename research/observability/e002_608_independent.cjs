'use strict';
// Independent exact rational replay of a triangular physical counterexample.
// Does not import the Python model or its output.
const assert = require('node:assert/strict');
function rat(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<=0n)throw Error('denominator');return [n,d]}
function add(a,b){return rat(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
function mul(a,b){return rat(a[0]*b[0],a[1]*b[1])}
function eq(a,b){return a[0]*b[1]===b[0]*a[1]}
function integralLinear(lo,hi,peak){
  // a(t) = 1/5 + |t-5|/50 on [-20,30]; integrate with trapezoids
  const f=t=>add(rat(1,5),rat(Math.abs(t-peak),50));
  let pts=[lo,...([peak].filter(x=>x>lo&&x<hi)),hi];
  let acc=rat(0);
  for(let i=1;i<pts.length;i++){
    const width=rat(pts[i]-pts[i-1]);
    const mean=mul(add(f(pts[i-1]),f(pts[i])),rat(1,2));
    acc=add(acc,mul(width,mean));
  }
  return mul(acc,rat(1,hi-lo));
}
const mL=integralLinear(-20,0,5),mR=integralLinear(10,30,5);
assert(eq(mL,rat(1,2))&&eq(mR,rat(1,2)));
const tau=rat(1,5), v=rat(1,50), gap=rat(10), exposure=rat(20);
const lhs=add(add(mL,mR),rat(-2,5));
const naive=mul(v,gap);
const correct=mul(v,add(gap,exposure));
assert(lhs[0]*naive[1]>naive[0]*lhs[1]); // wrong point test excludes
assert(eq(lhs,correct)); // correct shutter-aware test does not exclude
assert(eq(add(add(rat(3,5),rat(3,5)),rat(-2,5)),rat(4,5)));
console.log(JSON.stringify({experiment:'E002-608',independent:'PASS',
  measured_averages:['1/2','1/2'],naive_false_exclusion:true,
  shutter_aware_boundary_equality:true,physical_camera_measurements:0,
  human_closure_measurements:0,release:'BLOCKED'}));
