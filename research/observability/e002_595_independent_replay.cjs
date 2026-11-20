#!/usr/bin/env node
"use strict";
// E002-595 independent integer-only phase oracle; no imports from Python.
// Discrete point-sampling grid only, NOT human closure or physical exposure.
const assert = require("node:assert/strict");
function grid(p) {
  if (!Number.isInteger(p) || p < 0 || p >= 3) throw Error("INVALID_PHASE");
  const out = [];
  for (let k = 0; k < 19; k++) {
    const numerator = 30n * BigInt(p) + 95n * BigInt(k);
    const index = Number((2n * numerator + 30n) / 60n);
    if (index >= 19) break;
    out.push(index);
  }
  return out;
}
function missed(xs, width) {
  if (!Number.isInteger(width) || width < 1 || width > 19)
    throw Error("INVALID_WIDTH");
  let count = 0;
  for (let start = 0; start <= 19 - width; start++) {
    if (!xs.some(i => start <= i && i < start + width)) count++;
  }
  return count;
}
const grids = [0,1,2].map(grid);
assert.deepEqual(grids, [
  [0,3,6,10,13,16], [1,4,7,11,14,17], [2,5,8,12,15,18]
]);
const union = new Set(grids.flat());
assert.equal(union.size, 18);
assert.deepEqual([...Array(19).keys()].filter(i=>!union.has(i)), [9]);
const misses = [1,2,3,4].map(w => grids.map(xs=>missed(xs,w)));
assert.deepEqual(misses, [[13,13,13],[7,6,7],[1,1,1],[0,0,0]]);
for (const bad of [-1,3,0.5,null,"1",true]) assert.throws(()=>grid(bad));
for (const bad of [-1,0,20,0.5,true]) assert.throws(()=>missed(grids[0],bad));
process.stdout.write(JSON.stringify({
  experiment:"E002-595", independent_replay:"PASS",
  exact_integer_grid:grids, missed_pulses_by_width:misses,
  all_phase_unobserved_native_indices:[9],
  physical_human_validation:false, product:"ABSTAIN_UNCALIBRATED"
})+"\n");
