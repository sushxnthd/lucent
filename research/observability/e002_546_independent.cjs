#!/usr/bin/env node
// E002-546 independent arithmetic oracle; does not import Python implementation.
// Hypothetical reference sampling only. Not a human measurement.
const assert = require("node:assert/strict");
const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
const reduced = (n, d) => { const g = gcd(n, d); return [n / g, d / g]; };
const expected = new Map([
  [30, [1, 15]], [100, [2, 9]], [200, [4, 9]],
  [240, [8, 15]], [500, [1, 1]],
]);
for (const [fps, pair] of expected) {
  // Threshold interval length: T*c/b = (1/100)*(1/5)/(9/10) = 1/450.
  const actual = reduced(Math.min(fps, 450), 450);
  assert.deepEqual(actual, pair, "uniform-phase detection probability");
}
// Independently evaluate the triangle at two sampled instants.
// 100Hz phase=0: 0 and 10ms, both open at 0.9.
// 200Hz phase=2.5ms: 2.5 and 7.5ms, both aperture 0.45.
const triangle = t => t < 0 || t > 0.010 ? 0.9
  : t <= 0.005 ? 0.9 * (1 - t / 0.005)
  : 0.9 * (t / 0.005 - 1);
assert(Math.abs(triangle(0) - 0.9) < 1e-12);
assert(Math.abs(triangle(0.010) - 0.9) < 1e-12);
assert(Math.abs(triangle(0.0025) - 0.45) < 1e-12);
assert(Math.abs(triangle(0.0075) - 0.45) < 1e-12);
assert(0.45 > 0.2);
console.log("E002-546 independent JS oracle: 5 exact phase probabilities and 5 geometric checks passed");
