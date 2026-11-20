#!/usr/bin/env node
'use strict';
// Independent exact-rational BigInt reconstruction of E002-591 (no Python data).
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
class Q {
  constructor(n,d=1n){n=BigInt(n);d=BigInt(d);if(d===0n)throw Error('ZERO_DENOM');if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
  add(x){return new Q(this.n*x.d+x.n*this.d,this.d*x.d)}
  sub(x){return new Q(this.n*x.d-x.n*this.d,this.d*x.d)}
  mul(x){return new Q(this.n*x.n,this.d*x.d)}
  div(x){return new Q(this.n*x.d,this.d*x.n)}
  cmp(x){const z=this.n*x.d-x.n*this.d;return z<0n?-1:z>0n?1:0}
  toString(){return this.d===1n?String(this.n):String(this.n)+'/'+String(this.d)}
}
const q=(a,b=1)=>new Q(a,b), Z=q(0), O=q(1), TWO=q(2), FOUR=q(4);
const eq=(a,b)=>a.cmp(b)===0;
function cutoff(c,tau,d){
  if(!(tau.cmp(Z)>=0&&c.cmp(tau)>0&&c.cmp(O)<0&&d.cmp(Z)>=0&&d.cmp(O)<0))throw Error('BAD_DOMAIN');
  const s=O.sub(d),h=O.sub(tau),excess=c.sub(tau),cap=tau.add(h.mul(s));
  if(c.cmp(cap)>=0)return null;
  return excess.cmp(h.mul(s).div(TWO))<=0
    ? FOUR.mul(excess).div(s.mul(s))
    : h.mul(h).div(cap.sub(c));
}
function meanCeiling(c,tau,d,v){
  const s=O.sub(d),h=O.sub(tau);
  if(v.mul(s).cmp(TWO.mul(c.sub(tau)))<0)return null;
  return v.mul(s).cmp(TWO.mul(h))<=0
    ?tau.add(v.mul(s).mul(s).div(FOUR))
    :tau.add(h.mul(s)).sub(h.mul(h).div(v));
}
function path(c,tau,d){
  const v=cutoff(c,tau,d);if(v===null)throw Error('IMPOSSIBLE');
  const s=O.sub(d),h=O.sub(tau),base=c.sub(tau).div(h),k=v.mul(s).div(h);
  let nodes;
  if(k.cmp(TWO)<=0){
    nodes=[[Z,base],[base.div(k),Z],[base.div(k).add(O.div(TWO)),k.div(TWO)],[O,base]];
  }else{
    nodes=[[Z,base],[base.div(k),Z],[base.add(O).div(k),O],
      [O.sub(O.sub(base).div(k)),O],[O,base]];
  }
  const tzero=base.div(k), out=[];
  for(let i=0;i<nodes.length;i++){
    const [u,b]=nodes[i];
    if(i>0&&eq(u,nodes[i-1][0]))continue;
    if(i>0&&u.cmp(tzero)>0&&eq(nodes[i-1][0],tzero)&&d.cmp(Z)>0)
      out.push([s.mul(tzero).add(d),tau]);
    out.push([s.mul(u).add(u.cmp(tzero)>0?d:Z),tau.add(h.mul(b))]);
  }
  return {v,out};
}
function check(c,tau,d,expected){
  const v=cutoff(c,tau,d);
  if(expected===null){if(v!==null)throw Error('FINITE_FALSE');return;}
  if(!eq(v,expected))throw Error('THRESHOLD '+v+' vs '+expected);
  const {out}=path(c,tau,d);
  if(!eq(out[0][0],Z)||!eq(out[0][1],c)||!eq(out[out.length-1][0],O)||!eq(out[out.length-1][1],c))throw Error('ENDPOINTS');
  let area=Z, dwellOK=eq(d,Z)&&out.some(([t,a])=>eq(a,tau));
  for(let i=1;i<out.length;i++){
    const [t0,a0]=out[i-1],[t1,a1]=out[i],dt=t1.sub(t0);
    if(dt.cmp(Z)<=0||a0.cmp(Z)<0||a0.cmp(O)>0||a1.cmp(Z)<0||a1.cmp(O)>0)throw Error('PATH_DOMAIN');
    const da=a1.sub(a0),abs=da.cmp(Z)<0?Z.sub(da):da;
    if(abs.cmp(v.mul(dt))>0)throw Error('SPEED');
    if(eq(a0,tau)&&eq(a1,tau)&&dt.cmp(d)>=0)dwellOK=true;
    area=area.add(dt.mul(a0.add(a1)).div(TWO));
  }
  if(!dwellOK||!eq(area,c)||!eq(meanCeiling(c,tau,d,v),c))throw Error('MEAN_DWELL');
  const sub=v.mul(q(99,100)),max=meanCeiling(c,tau,d,sub);
  if(max!==null&&max.cmp(c)>=0)throw Error('SUBTHRESHOLD_NOT_EXCLUDED');
}
const cases=[
 [q(1,2),Z,Z,q(2)], [q(1,2),Z,q(1,10),q(5,2)],
 [q(1,2),Z,q(1,4),q(4)], [q(1,2),Z,q(1,2),null],
 [q(1,2),q(1,10),q(3,10),q(81,23)],
 [q(1,5),Z,q(1,10),q(80,81)],
 [q(1,2),q(1,10),q(3,5),null]];
for(const row of cases)check(...row);
let grid=0;
for(const c of [q(1,5),q(2,5),q(1,2),q(3,5),q(4,5)])
 for(const tau of [Z,q(1,10)])
  for(const d of [Z,q(1,20),q(1,10),q(1,4),q(2,5),q(3,5)]){
   if(c.cmp(tau)<=0)continue;
   const v=cutoff(c,tau,d);
   if(v!==null){check(c,tau,d,v);grid++;}
  }
function witnessInterval(t,upper,tau,speed,timeError){
  const r=tau.sub(upper).div(speed).sub(timeError);
  if(r.cmp(Z)<0)return null;
  return [t.sub(r),t.add(r)];
}
const w=witnessInterval(q(10),q(1,20),q(1,10),q(1,100),q(1));
if(!eq(w[0],q(6))||!eq(w[1],q(14)))throw Error('CLOCK_WITNESS');
if(witnessInterval(q(10),q(1,20),q(1,10),q(1,100),q(6))!==null)throw Error('CLOCK_OVERCLAIM');
console.log(JSON.stringify({experiment:'E002-591',independent_replay:'PASS',
  frozen_cases:cases.length,rational_grid_witnesses:grid,
  evidence_tier:'IDEALIZED_THEOREM_SYNTHETIC_ONLY',product:'ABSTAIN_UNCALIBRATED',release:'BLOCKED'}));
