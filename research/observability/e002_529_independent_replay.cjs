// E002-529 independent exact BigInt arithmetic. No import from Python implementation.
// Synthetic scalar falsification only; no human or camera calibration.
const assert = require('node:assert/strict');

function gcd(a,b) { a=a<0n?-a:a; b=b<0n?-b:b; while(b){[a,b]=[b,a%b];} return a; }
function r(n,d=1n) {
  n=BigInt(n); d=BigInt(d);
  if(d===0n) throw Error('ZERO_DENOMINATOR');
  if(d<0n){n=-n;d=-d;}
  const g=gcd(n,d);
  return {n:n/g,d:d/g};
}
function add(a,b){return r(a.n*b.d+b.n*a.d,a.d*b.d);}
function neg(a){return r(-a.n,a.d);}
function sub(a,b){return add(a,neg(b));}
function mul(a,b){return r(a.n*b.n,a.d*b.d);}
function div(a,b){return r(a.n*b.d,a.d*b.n);}
function cmp(a,b){const v=a.n*b.d-b.n*a.d;return v<0n?-1:v>0n?1:0;}
function eq(a,b){return cmp(a,b)===0;}
function min(a,b){return cmp(a,b)<=0?a:b;}
function max(a,b){return cmp(a,b)>=0?a:b;}
const zero=r(0), one=r(1), two=r(2), four=r(4);
function clamp(x){return max(zero,min(one,x));}
function opportunity(P,e,d,u=zero){
  return {full:clamp(div(sub(sub(d,e),mul(two,u)),P)),
          overlap:cmp(d,zero)>0?clamp(div(add(d,e),P)):zero};
}
function fullAtPhase(P,e,d,u,phi){
  for(let k=-2;k<=3;k++){
    const a=add(phi,mul(r(k),P));
    if(cmp(sub(a,u),zero)>0 && cmp(add(add(a,e),u),d)<0) return true;
  }
  return false;
}

const b=one,c=r(1,5),V=r(60),H=r(1,30),eps=r(1,10000);
const h=div(mul(V,eps),four);
const critical=div(mul(two,sub(b,c)),V);
const descend=div(add(sub(b,c),h),V);
const whole=add(mul(two,descend),div(eps,two));
const crossingDwell=add(div(eps,two),div(mul(two,h),V));
assert(eq(critical,r(2,75)));
assert(eq(whole,r(803,30000)));
assert(cmp(whole,H)<0);
assert(eq(crossingDwell,eps));
assert(cmp(h,c)<0);

const p240=opportunity(r(1,240),r(1,1000),eps,r(1,10000));
assert(eq(p240.full,zero));
assert(eq(p240.overlap,r(33,125)));
const p1000=opportunity(r(1,1000),r(1,2000),eps);
assert(eq(p1000.full,zero));
assert(eq(p1000.overlap,r(3,5)));
const falseSubstitution=opportunity(r(1,240),r(1,1000),critical,r(1,10000));
assert(eq(falseSubstitution.full,one));
const holdout=r(1,100000);
const p10000=opportunity(r(1,10000),r(1,100000),holdout);
assert(eq(p10000.full,zero));
assert(eq(p10000.overlap,r(1,5)));
let witnesses=0;
for(let j=0;j<10000;j++){
  const phi=mul(r(j,10000),r(1,240));
  if(fullAtPhase(r(1,240),r(1,1000),eps,r(1,10000),phi)) witnesses++;
}
assert.equal(witnesses,0);
console.log(JSON.stringify({
  experiment:'E002-529', exact_arithmetic:'independent_node_bigint',
  minimum_excursion_s:'2/75', total_excursion_s:'803/30000',
  strict_closed_dwell_s:'1/10000', full_240hz:'0',
  ideal_overlap_240hz:'33/125', full_1000hz:'0',
  ideal_overlap_1000hz:'3/5', invalid_substitution_full_240hz:'1',
  heldout_10000hz_full:'0', heldout_10000hz_overlap:'1/5',
  exact_phase_grid_witnesses:witnesses, product:'ABSTAIN_UNCALIBRATED'
}));
