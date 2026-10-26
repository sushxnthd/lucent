"use strict";
/* E002-461 independent JS replay. No import of Python or E002-460 code.
 * Every generated trajectory has a genuine synthetic dark-gap closure.
 * This does NOT validate physical human measurements or velocity caps.
 */
const assert = require("node:assert/strict");
const C0 = 567.103928 / 1000, O0 = 274.616337 / 1000;
const D0 = 1000 / 240, W0 = 2.3, threshold = 2.0;

function exactQ(m, s, w) { return m*m + (s*w)**2 / 12; }
function caseFrom(C, O, D, w, tau, c, a, b) {
  assert(w / 2 < tau && tau < D - w / 2);
  const m0 = c + a*C*tau, m1 = c + b*O*(D-tau);
  return {C,O,D,w,tau,c,q0:exactQ(m0,a*C,w),q1:exactQ(m1,b*O,w),m0,m1};
}
function excluded(x, m0, m1) {
  const earliest = Math.max(x.w/2, (m0-x.c)/x.C);
  const latest = Math.min(x.D-x.w/2, x.D-(m1-x.c)/x.O);
  return earliest > latest + 1e-10*Math.max(1,Math.abs(earliest),Math.abs(latest));
}
function naive(x) {return excluded(x,Math.sqrt(x.q0),Math.sqrt(x.q1));}
function corrected(x) {
  const L = Math.max(x.C,x.O);
  const varianceMax = (L*x.w)**2/12;
  return excluded(x, Math.sqrt(Math.max(0,x.q0-varianceMax)),
                     Math.sqrt(Math.max(0,x.q1-varianceMax)));
}
const primary = caseFrom(C0,O0,D0,W0,D0/2,threshold,.99,.99);
const negative = caseFrom(C0,O0,D0,W0,D0/2,threshold,.95,.95);
assert.equal(naive(primary),true,"primary invalid static-inverse rule must falsely exclude");
assert.equal(corrected(primary),false,"corrected rule must not exclude witnessed closure");
assert.equal(naive(negative),false,"frozen negative control must not falsely exclude");
assert.equal(corrected(negative),false);
let seed=461>>>0;
function random() {seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/4294967296;}
function uniform(lo,hi) {return lo+(hi-lo)*random();}
let naiveErrors=0, correctedErrors=0;
for(let i=0;i<10000;i++){
  const D=uniform(3.5,10),w=uniform(.2,Math.min(3,.7*D));
  const tau=uniform(w/2+.01,D-w/2-.01);
  const x=caseFrom(uniform(.15,.8),uniform(.1,.5),D,w,tau,uniform(.5,3),
                   uniform(.65,1),uniform(.65,1));
  if(naive(x)) naiveErrors++;
  if(corrected(x)) correctedErrors++;
}
assert(naiveErrors>0,"nonlinear sensor must cause false exclusions in randomized sample");
assert.equal(correctedErrors,0,"conservative interval may never exclude a witness");
const apparentCritical = (Math.sqrt(primary.q0)-threshold)/C0+
                         (Math.sqrt(primary.q1)-threshold)/O0;
const correctedCritical = (Math.sqrt(Math.max(0,primary.q0-(C0*W0)**2/12))-threshold)/C0+
                          (Math.sqrt(Math.max(0,primary.q1-(C0*W0)**2/12))-threshold)/O0;
console.log(JSON.stringify({experiment:"E002-461",evidence:"SYNTHETIC_ONLY",
 primary:{gap_ms:D0,shutter_ms:W0,alpha:.99,q0_mm2:primary.q0,q1_mm2:primary.q1,
  true_closure_ms:primary.tau,naive_false_exclusion:naive(primary),
  corrected_exclusion:corrected(primary),naive_critical_ms:apparentCritical,
  corrected_critical_lower_ms:correctedCritical},
 negative_control:{alpha:.95,naive_false_exclusion:naive(negative)},
 randomized:{seed:461,n:10000,naive_false_exclusions:naiveErrors,
             corrected_false_exclusions:correctedErrors},
 physical_certification:false},null,2));
