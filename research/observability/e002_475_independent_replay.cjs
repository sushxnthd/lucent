// E002-475 independent arithmetic and exhaustive rank replay. No Python imports.
'use strict';
const assert = require('node:assert/strict');
function factorial(n) { let v = 1; for (let i = 2; i <= n; ++i) v *= i; return v; }
function countPermutations(values, n, cb, used = [], remaining = values) {
  if (!remaining.length) { cb(used); return; }
  for (let i = 0; i < remaining.length; i++)
    countPermutations(values, n, cb, [...used, remaining[i]], [...remaining.slice(0, i), ...remaining.slice(i+1)]);
}
let success = 0, total = 0;
countPermutations([1,2,3,4,5], 3, ranks => {
  total++;
  if (Math.max(...ranks.slice(0,3)) > Math.max(...ranks.slice(3))) success++;
});
assert.equal(total, factorial(5));
assert.equal(success, 72);
assert.equal(success/total, 3/5);
assert.equal(12/(12+1), 12/13);
assert.equal(12/(12+8), 0.6);
const tol = n => 1 - Math.pow(0.95, n);
assert(tol(58) < 0.95 && tol(59) >= 0.95);
assert(151/159 < 0.95 && 152/160 >= 0.95);
assert(Math.abs(tol(12) - 0.459639912337363) < 1e-14);
console.log(JSON.stringify({independent_replay:'PASS',permutations:total,success,
  one_person:12/13,eight_people:12/20,tolerance_confidence_n12:tol(12),
  minimum_95_95:59,minimum_95_joint_eight:152}));
