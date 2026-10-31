#!/usr/bin/env node
"use strict";
// E002-464 independent arithmetic, not a copy of the Python gate.
// Synthetic counterexamples only; no physical sensor or human evidence.
const assert = require("node:assert/strict");
const left = 0.15, right = 2.35, nominal = 1.0, delta = 0.02;
const threshold = 2.0, observed = 1.95, error = 0.01;
const inside = (past, future, width=0) =>
  nominal - delta - width/2 - past > left + 1e-12 &&
  nominal + delta + width/2 + future < right - 1e-12;
assert.equal(observed + error <= threshold, true);
assert.equal(inside(1.4, 0), false);
assert.equal(inside(0.1, 0), true);
assert.equal(inside(0.83, 0), false);
assert.equal(inside(0.82, 0), true);
assert.equal(inside(0, 1.33), false);
assert.equal(inside(0, 1.32), true);
assert.equal(inside(0.82, 0, 0.1), false);
const physicalClosureTime = -0.4, causalDelay = 1.4;
assert.ok(Math.abs(physicalClosureTime + causalDelay - nominal) < 1e-12);
assert.ok(physicalClosureTime < left); // true dark gap remains open
const signedOutput = 2*2.2 - 2.45;
assert.ok(2.2 > threshold && 2.45 > threshold);
assert.ok(Math.abs(signedOutput - 1.95) < 1e-12);
let admitted = 0;
for (let i=0; i<=200; i++) {
  for (let j=0; j<=200; j++) {
    if (inside(i/100, j/100)) admitted++;
  }
}
assert.equal(admitted, 11039);
const result = {
  experiment: "E002-464",
  evidence_tier: "SYNTHETIC_ONLY_INDEPENDENT_ARITHMETIC",
  delayed_report_time_ms: nominal,
  true_closure_time_ms: physicalClosureTime,
  true_dark_gap_open: true,
  legacy_positive_is_unsound_without_lag_bound: true,
  dynamic_gate_delayed_witness_allowed: inside(1.4, 0),
  dynamic_gate_calibrated_witness_allowed: inside(0.1, 0),
  signed_kernel_falsifies_positive_average_implication: true,
  sweep_cases: 40401,
  sweep_interior: admitted,
  physical_release_authorized: false,
  product_claim: "ABSTAIN_UNCALIBRATED"
};
process.stdout.write(JSON.stringify(result, null, 2) + "\n");
