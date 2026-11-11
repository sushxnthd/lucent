#!/usr/bin/env node
// E002-550 independent arithmetic replay. No private human data.
const assert = require("node:assert/strict");
function bound(y0, y1, dt, e, u, A) {
  if (!(dt > 2*u) || [y0,y1,dt,e,u,A].some(x => !Number.isFinite(x)) || [e,u,A].some(x=>x<0))
    return null;
  return (Math.abs(y1-y0)+2*e)/(dt-2*u)+A*(dt+2*u)/2;
}
const exact = bound(.4,.5,.0025,0,0,0);
const noisy = bound(.4,.5,.0025,.01,0,1000);
const clock = bound(.4,.5,.0025,.01,.0001,1000);
assert.ok(Math.abs(exact-40)<1e-10);
assert.ok(Math.abs(noisy-49.25)<1e-10);
assert.ok(clock>noisy);
assert.equal(bound(.4,.5,.0025,.01,.00125,1000),null);
assert.equal(bound(.5,.5,.0025,0,0,Infinity),null);
// A finite-difference zero is compatible with arbitrarily large hidden slopes
// when there is no hard acceleration ceiling: triangular amplitude .5.
for (const width of [1e-4,1e-5,1e-6]) assert.ok(1/width>=1e4);
console.log(JSON.stringify({experiment:"E002-550",independent_replay:"PASS",
  exact_linear:exact, conditional_error_accel:noisy,
  clock_widened:clock, human_measurements:0, product:"ABSTAIN_UNCALIBRATED"}));
