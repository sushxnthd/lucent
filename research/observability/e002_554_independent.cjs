'use strict';
// Independent BigInt rational integration of shutter segments and quadratic witness.
// Does not load Python or its JSON aggregate.
const assert = require('node:assert/strict');
const gcd = (a,b) => b === 0n ? (a < 0n ? -a : a) : gcd(b,a%b);
class Q {
  constructor(n,d=1n) { n=BigInt(n); d=BigInt(d); if(d===0n) throw Error('zero denominator');
    const g=gcd(n,d); this.n=(d<0n?-n:n)/g; this.d=(d<0n?-d:d)/g; }
  add(x){return new Q(this.n*x.d+x.n*this.d,this.d*x.d)}
  neg(){return new Q(-this.n,this.d)}
  sub(x){return this.add(x.neg())}
  mul(x){return new Q(this.n*x.n,this.d*x.d)}
  div(x){return new Q(this.n*x.d,this.d*x.n)}
  pow(k){return new Q(this.n**BigInt(k),this.d**BigInt(k))}
  eq(x){return this.n===x.n&&this.d===x.d}
  toString(){return this.d===1n?String(this.n):`${this.n}/${this.d}`}
}
const q=(n,d=1)=>new Q(n,d);
const z=q(0),one=q(1),half=q(1,2);
const cuts=[z,q(1,10),q(1,5),q(4,5),q(9,10),one];
const pattern=[1,-1,0,-1,1];
const kernel=(sign)=>pattern.map((v,i)=>({a:cuts[i],b:cuts[i+1],w:one.add(q(sign*v,2))}));
const integ=(k,p)=>k.reduce((acc,s)=>acc.add(s.w.mul(s.b.pow(p+1).sub(s.a.pow(p+1))).div(q(p+1))),z);
const moments=(k)=>{
  const mass=integ(k,0),center=integ(k,1).div(mass);
  return {mass,center,variance:integ(k,2).div(mass).sub(center.pow(2))};
};
const hi=kernel(1),lo=kernel(-1),H=moments(hi),L=moments(lo);
assert(H.mass.eq(one)&&L.mass.eq(one));
assert(H.center.eq(half)&&L.center.eq(half));
assert(H.variance.sub(L.variance).eq(q(2,125)));
// Independent quadratic integration: E[(a+h*x-1/2)^2].
const measured=(k,a,h)=>{
  const offset=a.sub(half);
  return offset.pow(2).mul(integ(k,0)).add(q(2).mul(offset).mul(h).mul(integ(k,1))).add(h.pow(2).mul(integ(k,2)));
};
const m0=measured(hi,q(-1,2),half),m1=measured(hi,one,half);
assert(m0.eq(m1)&&m0.eq(q(439,750)));
const d=q(3,2);
const bound=(k)=>m0.sub(half.pow(2).mul(moments(k).variance)).sub(d.pow(2).div(q(4)));
assert(bound(lo).eq(q(1,250)));
assert(bound(hi).eq(z));
assert(hi[2].w.eq(lo[2].w));
assert(!hi[0].w.eq(lo[0].w));
console.log('E002-554 independent BigInt rational oracle PASS; m='+m0+', bad='+bound(lo)+', good='+bound(hi));
