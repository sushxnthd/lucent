// Independent exact-rational algebraic replay of E002-523 frozen worlds.
// No Python import, no real hardware or human evidence.
const assert = require('node:assert/strict');
function gcd(a,b){while(b){[a,b]=[b,a%b];}return a<0n?-a:a;}
class Q {
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
  add(b){return new Q(this.n*b.d+b.n*this.d,this.d*b.d);}
  sub(b){return new Q(this.n*b.d-b.n*this.d,this.d*b.d);}
  mul(b){return new Q(this.n*b.n,this.d*b.d);}
  div(b){return new Q(this.n*b.d,this.d*b.n);}
  eq(b){return this.n===b.n&&this.d===b.d;}
  gt(b){return this.n*b.d>b.n*this.d;}
  lte(b){return this.n*b.d<=b.n*this.d;}
  toString(){return this.d===1n?String(this.n):`${this.n}/${this.d}`;}
}
const q=(n,d=1)=>new Q(n,d);
const T=q(10), alpha=q(1,50), theta=q(1,5), open=q(201,1000), one=q(1), baseline=one.div(T);
for(const w of [q(1,100),q(1,10000)]){
  const mean=open.mul(one.sub(alpha).sub(w.div(T)));
  const trueR=one.add(q(2).mul(alpha).mul(T).div(w));
  const naive=T.mul(one.sub(mean.div(theta)));
  const valid=naive.div(trueR);
  assert(naive.gt(w),'naive cap must be falsified');
  assert(valid.lte(w),'true cap must remain valid');
  assert(mean.gt(q(0))&&!mean.gt(theta));
  assert(baseline.sub(q(2).mul(alpha).div(q(4,5))).eq(q(1,20)));
  for(let i=0;i<=10;i++){
    const t=q(i);
    const insideA=t.gt(q(3,2).sub(w.div(q(2)))) && q(3,2).add(w.div(q(2))).gt(t);
    const insideB=t.gt(q(11,2).sub(q(2,5))) && q(11,2).add(q(2,5)).gt(t);
    assert(!insideA&&!insideB);
  }
  process.stdout.write(JSON.stringify({width_ms:w.toString(),mean:mean.toString(),actual_R:trueR.toString(),naive_lower_ms:naive.toString(),valid_lower_ms:valid.toString()})+'\n');
}
