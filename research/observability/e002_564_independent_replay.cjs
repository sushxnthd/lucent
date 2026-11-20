'use strict';
// Independent exact rational implementation, deliberately no Python imports.
const assert = require('node:assert/strict');
function gcd(a,b) { while(b!==0n){[a,b]=[b,a%b]} return a<0n?-a:a }
function dec(s) { const [w,f='']=String(s).split('.'); return [BigInt(w+f),10n**BigInt(f.length)] }
function ratio(v,a) {const [vn,vd]=dec(v),[an,ad]=dec(a); const n=vn*ad,d=vd*an; assert(d>0n);const g=gcd(n,d);return `${n/g}/${d/g}`}
assert.equal(ratio('243','9.83'),'24300/983');
assert.equal(ratio('427','11.7'),'4270/117');
assert.equal(ratio('329','10.2'),'1645/51');
assert.equal(ratio('349','10.6'),'1745/53');
assert.equal(ratio('243','12.8'),'1215/64');
console.log('E002-564 independent BigInt exact ratios: 5/5 passed');
