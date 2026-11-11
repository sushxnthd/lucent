'use strict';
// Independent floating-point replay; no import from Python exact-rational implementation.
const assert = require('node:assert/strict');
const T = 1000/150, e = 1, baseline = .35, threshold = .10, speed = .10;
const ratio = speed*(T-e)/(2*(baseline-threshold));
const critical = 2*(baseline-threshold)/(T-e);
const meanAtHalfPhase = threshold + speed*e/4;
const maxJitterMean = threshold + speed*(e/4 + (.25*.25)/e);
const contaminatedMax = maxJitterMean*1.10+.01;
const calibratedMax = maxJitterMean*1.05+.005;
const lowerSpeedRatio = .08*(T-e)/(2*(baseline-threshold));
function approx(a,b,tol=1e-12) {assert.ok(Math.abs(a-b)<tol,`${a} != ${b}`);}
approx(ratio,17/15);
approx(critical,3/34);
approx(meanAtHalfPhase,.125);
approx(maxJitterMean,.13125);
approx(contaminatedMax,.154375);
approx(calibratedMax,.1428125);
assert.ok(contaminatedMax>.15);
assert.ok(calibratedMax<.15);
assert.ok(lowerSpeedRatio<1);
function aperture(t, dip=.1) {
  const center=T/2;
  const nearest=Math.min(...Array.from({length:7},(_,i)=>Math.abs(t-(i-3)*T-center)));
  return baseline-Math.max(0,baseline-dip-speed*nearest);
}
function integrate(center,dip=.1,n=200000) {
  let s=0;
  for(let i=0;i<n;i++) s+=aperture(center-e/2+(i+.5)*e/n,dip);
  return s/n;
}
approx(integrate(0),baseline,1e-9);
approx(integrate(T),baseline,1e-9);
approx(integrate(T/2),meanAtHalfPhase,1e-8);
approx(integrate(T/2+.25),maxJitterMean,1e-8);
approx(integrate(0,.08),baseline,1e-9);
console.log(JSON.stringify({independent_replay:'PASS',ratio,critical,meanAtHalfPhase,maxJitterMean,contaminatedMax,calibratedMax,strict_closure_hidden:true,quadrature_steps:200000},null,2));
