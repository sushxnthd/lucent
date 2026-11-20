'use strict';
// Independent exact BigInt rational replay. No Python imports or shared code.
const assert = require('node:assert/strict');
function gcd(a,b) { while (b !== 0n) [a,b] = [b,a%b]; return a < 0n ? -a : a; }
function rat(s) {
  if (!/^-?(0|[1-9]\d*)(\.\d+)?$/.test(String(s))) throw Error('decimal');
  let [a,b=''] = String(s).split('.');
  let d=10n**BigInt(b.length), n=BigInt(a.replace('-','')+b)*(String(s).startsWith('-')?-1n:1n);
  return reduce(n,d);
}
function reduce(n,d) { if(d===0n)throw Error('zero');if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g]; }
function mul([a,b],[c,d]) {return reduce(a*c,b*d);}
function sub([a,b],[c,d]) {return reduce(a*d-c*b,b*d);}
function div([a,b],[c,d]) {return reduce(a*d,b*c);}
function cmp([a,b],[c,d]) {return a*d < c*b ? -1 : a*d > c*b ? 1 : 0;}
function upper(y,b,g,L) {
  let z=div(sub(rat(y),rat(b)),mul(rat(g),rat(L)));
  return cmp(z,rat('0'))<0?rat('0'):cmp(z,rat('1'))>0?rat('1'):z;
}
function equal(a,b) {assert.equal(cmp(a,b),0);}
const tight=upper('0.15','0','0.98','0.9');
const loose=upper('0.15','0','0.98','0.5');
equal(tight,reduce(25n,147n));
equal(loose,reduce(15n,49n));
assert.ok(cmp(tight,rat('0.2'))<=0);
assert.ok(cmp(loose,rat('0.2'))>0);
equal(mul(rat('0.2'),rat('1')),mul(rat('0.5'),rat('0.4')));
equal(upper('0.2','0','1','0.4'),rat('0.5'));
console.log(JSON.stringify({experiment:'E002-610',independent:'PASS',tight_upper:'25/147',loose_upper:'15/49',two_worlds_same_signal:true}));
