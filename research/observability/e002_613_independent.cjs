// E002-613 independent finite-unit arithmetic (no import from Python code).
// Millimetres -> integer micrometres; seconds -> integer microseconds.
const assert = require('node:assert/strict');
function scaled(s, factor) {
  assert.match(s, /^(?:0|[1-9]\d*)(?:\.\d+)?$/);
  const [whole, fraction = ''] = s.split('.');
  const digits = factor.toString().length - 1;
  assert.ok(fraction.length <= digits, 'precision exceeds fixed units');
  return BigInt(whole) * factor + BigInt((fraction + '0'.repeat(digits)).slice(0, digits));
}
function gcd(a,b) { while(b) [a,b] = [b,a%b]; return a; }
function lower(z0,z1,e0,e1,dt) {
  const x0 = scaled(z0,1000n), x1 = scaled(z1,1000n);
  const err = scaled(e0,1000n) + scaled(e1,1000n);
  const time = scaled(dt,1000000n);
  assert.ok(time>0n);
  const gap = (x1>x0?x1-x0:x0-x1)-err;
  const num = (gap>0n?gap:0n)*1000n;
  const g = gcd(num,time);
  return [num/g,time/g];
}
function rejected(l, cap) { return l[0]*1000n > scaled(cap,1000n)*l[1]; }
const base=['8.0','7.5','0.05','0.05','0.0025'];
assert.deepEqual(lower(...base),[160n,1n]);
assert.equal(rejected(lower(...base),'150'),true);
assert.equal(rejected(lower(...base),'160'),false);
assert.deepEqual(lower('8.0','7.5','0.05','0.05','0.003'),[400n,3n]);
assert.equal(rejected(lower('8.0','7.5','0.05','0.05','0.003'),'150'),false);
assert.deepEqual(lower('8.0','7.5','0.25','0.25','0.0025'),[0n,1n]);
assert.deepEqual(lower('8.0','8.0','0.05','0.05','0.0025'),[0n,1n]);
assert.throws(()=>lower('8','7','0','0','0'));
assert.throws(()=>lower('8','7','NaN','0','0.0025'));
console.log('E002-613 independent integer-unit verifier: 8 checks passed (synthetic only)');
