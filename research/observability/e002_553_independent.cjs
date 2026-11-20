'use strict';
// Independent BigInt rational oracle: pulse integration and two quadratic witnesses.
const assert=require('node:assert/strict');
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
class R{
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');
    if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
  add(x){return new R(this.n*x.d+x.n*this.d,this.d*x.d)}
  neg(){return new R(-this.n,this.d)}
  sub(x){return this.add(x.neg())}
  mul(x){return new R(this.n*x.n,this.d*x.d)}
  div(x){return new R(this.n*x.d,this.d*x.n)}
  eq(x){return this.n===x.n&&this.d===x.d}
  gt(x){return this.n*x.d>x.n*this.d}
  toString(){return this.d===1n?''+this.n:`${this.n}/${this.d}`}
}
const q=(n,d=1)=>new R(n,d),zero=q(0),one=q(1),half=q(1,2),third=q(1,3);
function moment1(a,b){return a.add(b).mul(half)}
function moment2(a,b){return a.mul(a).add(a.mul(b)).add(b.mul(b)).mul(third)}
function pulseMoments(start,end,width){
  const a=start,b=start.add(width),c=end.sub(width),d=end;
  const mu=moment1(a,b).add(moment1(c,d)).mul(half);
  const sec=moment2(a,b).add(moment2(c,d)).mul(half);
  return {mu,v:sec.sub(mu.mul(mu)),sec};
}
function fMean(m){return m.sec.sub(m.mu).add(q(1,4))}
function lowerAt(t,m0,m1,mu0,mu1,v0,v1){
  const D=mu1.sub(mu0),s=t.sub(mu0).div(D),om=one.sub(s),A=q(2);
  const B0=m0.sub(A.mul(v0).mul(half)),B1=m1.sub(A.mul(v1).mul(half));
  return om.mul(B0).add(s.mul(B1)).sub(A.mul(D.mul(D)).mul(s).mul(om).mul(half));
}
const left=pulseMoments(q(-1,2),zero,q(1,20));
const right=pulseMoments(one,q(3,2),q(1,20));
const m0=fMean(left),m1=fMean(right);
assert(m0.eq(q(46,75)));assert(m1.eq(q(46,75)));
assert(left.v.eq(q(61,1200)));assert(right.v.eq(q(61,1200)));
assert(left.mu.eq(q(-1,4)));assert(right.mu.eq(q(5,4)));
const boxvar=q(1,48);
const correct=lowerAt(half,m0,m1,left.mu,right.mu,left.v,right.v);
const wrong=lowerAt(half,m0,m1,left.mu,right.mu,boxvar,boxvar);
assert(correct.eq(zero));assert(wrong.eq(q(3,100)));assert(wrong.gt(q(1,50)));
function altMean(m){return m.sec.mul(half).add(m.mu.mul(q(1,7))).add(q(1,9))}
const alt0=altMean(left),alt1=altMean(right);
function lowerAlt(t){
  const D=right.mu.sub(left.mu),s=t.sub(left.mu).div(D),om=one.sub(s);
  return om.mul(alt0.sub(left.v.mul(half))).add(s.mul(alt1.sub(right.v.mul(half))))
    .sub(D.mul(D).mul(s).mul(om).mul(half));
}
for(const t of [zero,q(1,4),half,q(3,4),one]){
  const actual=t.mul(t).mul(half).add(t.mul(q(1,7))).add(q(1,9));
  assert(lowerAlt(t).eq(actual));
}
console.log(JSON.stringify({independent_oracle:'BigInt exact pulse integration',mean:m0.toString(),
  variance:left.v.toString(),boxcar_variance:boxvar.toString(),correct_lower:correct.toString(),
  wrong_lower:wrong.toString(),false_exclusion:true,additional_quadratic_equality_checks:5}));
