'use strict';
// Independent exact decimal comparison; no Python import and no camera evidence.
const assert = require('node:assert/strict');
function q(s) {
  s=String(s);
  if(!/^-?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(s)) throw Error('decimal');
  const neg=s.startsWith('-'); if(neg)s=s.slice(1);
  const [i,f='']=s.split('.'); const den=10n**BigInt(f.length);
  return {n:(neg?-1n:1n)*BigInt(i+f),d:den};
}
function cmp(a,b) {const x=q(a),y=q(b);const diff=x.n*y.d-y.n*x.d;return diff<0n?-1:diff>0n?1:0;}
function assess(gap,ref,tau,prediction) {
  if(!(cmp(gap.l,gap.r)<0 && cmp(ref.a,ref.b)<0))return 'INVALID';
  if(!(cmp(gap.l,ref.a)<0 && cmp(ref.b,gap.r)<0))return 'ABSTAIN';
  if(cmp(ref.upper,tau)>0)return 'NO_REFERENCE_WITNESS';
  return prediction==='EXCLUDE'?'WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION':'HIDDEN_CLOSURE_WITNESS_CONDITIONAL';
}
const gap={l:'0',r:'10'},ref={a:'3',b:'5',upper:'0.15'};
assert.equal(assess(gap,ref,'0.20','EXCLUDE'),'WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION');
assert.equal(assess(gap,ref,'0.20','ABSTAIN'),'HIDDEN_CLOSURE_WITNESS_CONDITIONAL');
for(const [a,b] of [['9','11'],['0','2'],['8','10'],['-1','5'],['3','11']]) {
 assert.equal(assess(gap,{...ref,a,b},'0.20','EXCLUDE'),'ABSTAIN');
}
assert.equal(assess(gap,{...ref,upper:'0.21'},'0.20','EXCLUDE'),'NO_REFERENCE_WITNESS');
assert.equal(assess(gap,{...ref,upper:'0.20'},'0.20','EXCLUDE'),'WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION');
assert.equal(cmp('0.20000000000000000000001','0.20'),1);
console.log('E002-609 independent exact-decimal replay: PASS (9 controls + precision)');
