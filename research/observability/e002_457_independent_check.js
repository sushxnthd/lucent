#!/usr/bin/env node
"use strict";
/* Independent E002-457 adversarial replay; no imports from Python implementation. */
let state = 2026457;
function random() {
  state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
  return state / 4294967296;
}
function invariant(condition, description) {
  if (!condition) throw new Error(description);
}
let falseExclusions = 0;
const crossingTrials = 30000;
for (let i = 0; i < crossingTrials; i++) {
  const C = 30 + 700 * random();
  const O = 30 + 700 * random();
  const c = 0.1 + 2 * random();
  const m0 = 0.1 + 1.8 * random();
  const m1 = 0.1 + 1.8 * random();
  const a0 = c + m0;
  const a1 = c + m1;
  const down = m0 / C;
  const up = m1 / O;
  const dt = down + up + random() * 0.01;
  const dwell = dt - down - up;
  const e = Math.min(dt * 0.16, 0.002) * random();
  const clock = dt * 0.03 * random();
  const u0 = 0.1 * random();
  const u1 = 0.1 * random();
  const path = t => t <= down ? a0 - C * t :
    t <= down + dwell ? c : c + O * (t - (down + dwell));
  const average = t => {
    let sum = 0;
    for (let j = 0; j < 24; j++) sum += path(t - e / 2 + e * (j + 0.5) / 24);
    return sum / 24;
  };
  const x0 = average(0);
  const x1 = average(dt);
  const shutterCorrection = (C + O) * e / 8;
  const b0 = x0 - u0 - shutterCorrection;
  const b1 = x1 - u1 - shutterCorrection;
  const critical = (b0 - c) / C + (b1 - c) / O;
  const excluded = b0 > c && b1 > c && dt + 2 * clock < critical - 1e-12;
  if (excluded) falseExclusions++;
}
const negativeTrials = 10000;
let excludedNegative = 0;
for (let i = 0; i < negativeTrials; i++) {
  const C = 100 + 500 * random();
  const O = 100 + 500 * random();
  const margin = 0.5 + 1.5 * random();
  const dt = (2 * margin / Math.max(C, O)) * 0.1;
  const critical = margin / C + margin / O;
  if (dt < critical) excludedNegative++;
}
invariant(falseExclusions === 0, "crossing was incorrectly excluded");
invariant(excludedNegative === negativeTrials, "short-gap negative control failed");

state = 457;
let witnessFailures = 0;
const exactTrials = 100000;
for (let i = 0; i < exactTrials; i++) {
  const C = 30 + 800 * random();
  const O = 30 + 800 * random();
  const c = 3 * random();
  const a0 = c + 0.01 + 2 * random();
  const a1 = c + 0.01 + 2 * random();
  const required = (a0 - c) / C + (a1 - c) / O;
  const dt = required + 0.03 * random();
  const tclose = (a0 - c) / C;
  const attained = a0 - C * tclose;
  const recovered = c + O * (required - tclose);
  if (dt < required - 1e-12 || Math.abs(attained - c) > 1e-9 ||
      Math.abs(recovered - a1) > 1e-9) witnessFailures++;
}
invariant(witnessFailures === 0, "exact directional witness failed");
const result = {
  experiment: "E002-457",
  evidence_tier: "INDEPENDENT_SYNTHETIC_NUMERICAL_ONLY",
  seed: 2026457,
  crossing_trials: crossingTrials,
  crossing_false_exclusions: falseExclusions,
  no_crossing_negative_controls: negativeTrials,
  negative_controls_excluded: excludedNegative,
  exact_piecewise_witness_trials: exactTrials,
  exact_witness_failures: witnessFailures,
  physical_release_authorized: false,
  product_claim: "ABSTAIN_UNCALIBRATED"
};
process.stdout.write(JSON.stringify(result, null, 2) + "\n");
