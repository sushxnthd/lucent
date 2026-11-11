'use strict';
// Independent integer rank verifier. No Python imports or generated fixtures.
const assert = require('node:assert/strict');
function numerator(nullMaxima, heldoutMax) {
  return 1 + nullMaxima.filter(x => x >= heldoutMax).length;
}
const calibration = Array.from({length: 39}, (_, i) => i / 1000);
assert.equal(numerator(calibration, 0.5), 1);
assert.equal(numerator(calibration, 0.038), 2);
assert.equal(numerator(calibration, 0.037), 3);
assert.equal(numerator(calibration, 0), 40);
const ranks = Array.from({length: 40}, (_, i) => {
  const vals = Array.from({length: 40}, (_, j) => j);
  const heldout = vals.splice(i, 1)[0];
  return numerator(vals, heldout);
});
assert.equal(ranks.filter(k => k / 40 <= 0.05).length, 2);
assert.equal(numerator(Array(39).fill(0.5), 0.5), 40);
const naive = 1 - Math.pow(0.95, 200);
assert.ok(naive > 0.9999 && naive < 1);
console.log(JSON.stringify({independent_rank_checks: 6,
  exact_exchangeable_false_candidate_fraction: 2 / 40,
  naive_any_hit_probability: naive,
  evidence: 'MATHEMATICAL_AND_SYNTHETIC_ONLY', release: 'BLOCKED'}));
