'use strict';
const assert=require('node:assert/strict');
// Integer-only check: A10=10*A, m10=10*m; 2*A10*f*(m10-tau10)>100*v.
function pass(v,A10,f,m10,tau10=2){return 2*A10*f*(m10-tau10)>100*v;}
assert.equal(pass(400,74,30,10),false);
assert.equal(pass(400,74,60,10),true);
assert.equal(pass(243,98,30,5),false);
assert.equal(pass(93,98,30,5),true);
assert.equal(pass(243,98,30,10),true);
// Strict equality at v=470.4 mm/s (tenths), A=9.8 mm, f=30 Hz.
assert.equal(2*98*30*(10-2)>10*4704,false);
console.log('E002-611 independent integer verifier PASS (6 checks)');
