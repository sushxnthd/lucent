// E002-612 independent exact rational replay; no Python imports.
'use strict';
const assert=require('node:assert/strict');
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n}
class Q{constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d}let g=gcd(n,d);this.n=n/g;this.d=d/g}
add(o){return new Q(this.n*o.d+o.n*this.d,this.d*o.d)}
sub(o){return new Q(this.n*o.d-o.n*this.d,this.d*o.d)}
mul(o){return new Q(this.n*o.n,this.d*o.d)}
div(o){return new Q(this.n*o.d,this.d*o.n)}
abs(){return new Q(this.n<0n?-this.n:this.n,this.d)}
eq(o){return this.n===o.n&&this.d===o.d}
toString(){return `${this.n}/${this.d}`}}
const q=n=>new Q(n), half=new Q(1n,2n);
function upper(z0,z1,e0,e1,lo,hi,m){if(lo.n<=0n||hi.n<=0n||e0.n<0n||e1.n<0n||m.n<0n)throw Error('invalid');return z1.sub(z0).abs().add(e0).add(e1).div(lo).add(m.mul(hi).mul(half))}
const expected=[[30,new Q(268,3)],[120,new Q(269,6)],[240,new Q(701,12)],[1000,new Q(405,2)]];
for(let [fps,ans] of expected){let dt=new Q(1,fps), e=new Q(1,10), actual=upper(q(0),q(0),e,e,dt,dt,q(5000));assert(actual.eq(ans),`${fps}: ${actual.toString()} != ${ans.toString()}`)}
let dt=new Q(1,120),e=new Q(1,10),trueSecant=e.add(e).div(dt), terminal=trueSecant.add(q(5000).mul(dt).mul(half));
assert(terminal.eq(upper(q(4),q(4),e,e,dt,dt,q(5000))));
console.log('E002-612 independent exact arithmetic: 4 rates + sharpness PASS');
