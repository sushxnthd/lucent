/* E002-593 independent BigInt verifier; synthetic integer-only shutter-gap test. */
'use strict';
function rng(seed) {
  let x = seed >>> 0;
  return function(lo, hi) {
    x ^= (x << 13) >>> 0;
    x ^= x >>> 17;
    x ^= (x << 5) >>> 0;
    x >>>= 0;
    return lo + (x % (hi - lo + 1));
  };
}
function check(c, g, r, a, b, measuredGap, apertureError=20, timingError=1500) {
  const Vnumerator = 2n * BigInt(c - 100) * BigInt(r);
  const denominator = 1000n * BigInt(g);
  const possibleClosure = r >= 1000;
  const naive = Vnumerator * BigInt(measuredGap) < BigInt(a + b - 200) * denominator;
  const certified = Vnumerator * BigInt(measuredGap + timingError) <
    BigInt(a + b - 2*apertureError - 200) * denominator;
  return {possibleClosure, naive, certified};
}
function run() {
  const rand = rng(593);
  const counts = {total:12000,true_hidden_closure:0,true_no_closure:0,
    naive_exclusions:0,naive_false_exclusions:0,robust_exclusions:0,
    robust_false_exclusions:0,oracle_exclusions:0};
  for(let i=0;i<counts.total;i++) {
    const c=rand(300,800),g=rand(12000,30000),r=rand(850,1150);
    const a=c+rand(-20,20),b=c+rand(-20,20),m=g+rand(-1500,1500);
    const v=check(c,g,r,a,b,m);
    counts[v.possibleClosure?'true_hidden_closure':'true_no_closure']++;
    if(v.naive) {counts.naive_exclusions++;if(v.possibleClosure)counts.naive_false_exclusions++;}
    if(v.certified) {counts.robust_exclusions++;if(v.possibleClosure)counts.robust_false_exclusions++;}
    if(!v.possibleClosure)counts.oracle_exclusions++;
  }
  if(counts.robust_false_exclusions!==0 || counts.naive_false_exclusions<=0) throw Error('adversarial test failed');
  if(check(500,20000,1000,520,520,18500).certified) throw Error('touching boundary not abstained');
  if(!check(500,20000,1000,530,530,18500).certified) throw Error('out-of-bound error attack missed');
  return counts;
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={check,run};
