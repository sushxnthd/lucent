'use strict';
// Independent BigInt rational replay of E002-540 idealized shutter model.
// No imports from the Python evaluator. No human or camera measurement claim.
const assert = require('node:assert/strict');
const gcd = (a,b) => b === 0n ? (a < 0n ? -a : a) : gcd(b,a%b);
class Q {
  constructor(n,d=1n) {
    n=BigInt(n); d=BigInt(d);
    assert.notEqual(d,0n);
    if(d<0n) {n=-n;d=-d;}
    const g=gcd(n,d);this.n=n/g;this.d=d/g;
  }
  add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
  sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
  mul(b){return new Q(this.n*b.n,this.d*b.d);}
  div(b){return new Q(this.n*b.d,this.d*b.n);}
  eq(b){return this.n===b.n && this.d===b.d;}
  lt(b){return this.n*b.d<b.n*this.d;}
  str(){return this.d===1n?String(this.n):String(this.n)+'/'+String(this.d);}
}
const q=(n,d=1)=>new Q(n,d);
const zero=q(0),one=q(1),two=q(2),V=q(45),E=q(1,100),T=q(1,30),b=q(9,10),c=q(1,5),x=q(7,10);
const ramp=one.sub(x).div(V);
const plateau=E.sub(ramp);
const mid=E.add(T).div(two);
const min=x.sub(V.mul(T.sub(E)).div(two));
const vertices=[[zero,one],[plateau,one],[E,x],[mid,min],[T,x],[T.add(ramp),one],[T.add(E),one]];
const integrate=(start,end)=>{
  let total=zero;
  for(let i=0;i<vertices.length-1;i++){
    const [t0,a0]=vertices[i], [t1,a1]=vertices[i+1];
    const lo=t0.lt(start)?start:t0, hi=end.lt(t1)?end:t1;
    if(!lo.lt(hi))continue;
    const slope=a1.sub(a0).div(t1.sub(t0));
    const yl=a0.add(slope.mul(lo.sub(t0)));
    const yh=a0.add(slope.mul(hi.sub(t0)));
    total=total.add(yl.add(yh).mul(hi.sub(lo)).div(two));
  }
  return total;
};
assert(integrate(zero,E).div(E).eq(b));
assert(integrate(T,T.add(E)).div(E).eq(b));
assert(min.eq(q(7,40)));
assert(min.lt(c));
assert(b.sub(V.mul(T.sub(E)).div(two)).eq(q(3,8)));
assert(c.sub(min).mul(two).div(V).eq(q(1,900)));
for(let i=0;i<vertices.length-1;i++){
  const [t0,a0]=vertices[i], [t1,a1]=vertices[i+1];
  assert(t0.lt(t1));
  const slope=a1.sub(a0).div(t1.sub(t0));
  assert(!slope.lt(q(-45)) && !q(45).lt(slope));
  assert(!a0.lt(zero) && !one.lt(a0));
}
console.log(JSON.stringify({verified:true,means:[b.str(),b.str()],minimum:min.str(),closed_dwell_seconds:q(1,900).str(),invalid_pointwise_floor:q(3,8).str(),synthetic_only:true}));
