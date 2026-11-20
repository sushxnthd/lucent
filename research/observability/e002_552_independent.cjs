// E002-552 independent BigInt rational check via polynomial exposure integration.
// No imports from Python or the decision module.
const assert = require('node:assert/strict');
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
class Q{
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
  add(o){return new Q(this.n*o.d+o.n*this.d,this.d*o.d)}
  sub(o){return new Q(this.n*o.d-o.n*this.d,this.d*o.d)}
  mul(o){return new Q(this.n*o.n,this.d*o.d)}
  div(o){return new Q(this.n*o.d,this.d*o.n)}
  toString(){return this.d===1n?String(this.n):`${this.n}/${this.d}`}
}
const q=(n,d=1)=>new Q(n,d);
const ZERO=q(0), ONE=q(1), TWO=q(2), SIX=q(6), TWELVE=q(12);
function polyMean(a,b,acc,lo,hi){
  // Direct integration: integral (a + b*t + acc*t²/2) / (hi-lo).
  const area=a.mul(hi.sub(lo))
    .add(b.mul(hi.mul(hi).sub(lo.mul(lo))).div(TWO))
    .add(acc.mul(hi.mul(hi).mul(hi).sub(lo.mul(lo).mul(lo))).div(SIX));
  return area.div(hi.sub(lo));
}
function lower(m0,m1,d,h0,h1,A,t){
  const c0=ZERO.sub(h0.div(TWO)),c1=d.add(h1.div(TWO));
  const s=t.sub(c0).div(c1.sub(c0));
  const varTerm=ONE.sub(s).mul(h0.mul(h0).div(TWELVE)).add(s.mul(h1.mul(h1).div(TWELVE)));
  return ONE.sub(s).mul(m0).add(s.mul(m1))
    .sub(A.div(TWO).mul(t.sub(c0).mul(c1.sub(t)).add(varTerm)));
}
// Exact 0 <= f <= 49/100, f(t)=(t-1/2)^2; threshold 1/10.
const d=ONE,h=q(1,5),A=TWO,a=q(1,4),b=q(-1),theta=q(1,10);
const m0=polyMean(a,b,A,ZERO.sub(h),ZERO);
const m1=polyMean(a,b,A,d,d.add(h));
assert.equal(m0.toString(),'109/300');assert.equal(m1.toString(),'109/300');
const naive=m0.sub(A.mul(d.mul(d)).div(q(8)));
assert.equal(naive.toString(),'17/150');
assert(naive.n*theta.d>theta.n*naive.d);
assert.equal(lower(m0,m1,d,h,h,A,q(1,2)).toString(),'0');
// Unequal exposures: the exact lower envelope is attained by the same parabola.
const h0=q(1,10),h1=q(3,10);
const u0=polyMean(a,b,A,ZERO.sub(h0),ZERO);
const u1=polyMean(a,b,A,d,d.add(h1));
for(const t of [ZERO,q(1,4),q(1,2),q(3,4),ONE]){
  const f=a.add(b.mul(t)).add(A.mul(t.mul(t)).div(TWO));
  assert.equal(lower(u0,u1,d,h0,h1,A,t).toString(),f.toString());
}
console.log(JSON.stringify({oracle:'independent BigInt polynomial integration',m0:m0.toString(),
  naive_lower:naive.toString(),corrected_midpoint:lower(m0,m1,d,h,h,A,q(1,2)).toString(),
  unequal_exposure_equality_checks:5,passed:true}));
