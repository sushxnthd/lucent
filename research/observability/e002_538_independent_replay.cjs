'use strict';
// Independently constructed integer threshold oracle for equal-endpoint cases.
// Does not import Python or implement its quadratic vertex algorithm.
const assert = require('node:assert/strict');
function gcd(a,b){while(b!==0n){[a,b]=[b,a%b];}return a;}
function q(A, fps, bNumer=9n,bDenom=10n,cNumer=1n,cDenom=5n){
  const deltaNumer=bNumer*cDenom-cNumer*bDenom;
  const deltaDenom=bDenom*cDenom;
  let n=BigInt(A)*deltaDenom, d=8n*BigInt(fps)**2n*deltaNumer;
  const g=gcd(n,d);return [n/g,d/g];
}
const fixtures=[[3000,30,'25/42','NO_HIDDEN_CROSSING'],
                [5040,30,'1','HIDDEN_CROSSING_FEASIBLE'],
                [6000,30,'25/21','HIDDEN_CROSSING_FEASIBLE'],
                [6000,240,'25/1344','NO_HIDDEN_CROSSING']];
for(const [A,fps,expected,decision] of fixtures){
  const [n,d]=q(A,fps);
  assert.equal(d===1n?String(n):`${n}/${d}`,expected);
  assert.equal(n<d?'NO_HIDDEN_CROSSING':'HIDDEN_CROSSING_FEASIBLE',decision);
}
console.log('E002-538 independent BigInt threshold replay: 4/4 exact cases passed; no human calibration claimed');
