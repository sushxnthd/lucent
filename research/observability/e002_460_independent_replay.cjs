"use strict";
/* E002-460 independent JavaScript reproduction. Pure math; no human data. */
const assert=require("node:assert/strict");
const C=567.103928, O=274.616337, c=2, m=3;
const delta=1000/240;
const critical=1000*(m-c)*(1/C+1/O);
const oldConservativeCritical=(e)=>1000*(1-(C+O)*e/8000)*(1/C+1/O);
function darkGapReachable({left,right,mu0,mu1,m0,m1,c,C,O}) {
  const lo=Math.max(left,mu0+1000*(m0-c)/C);
  const hi=Math.min(right,mu1-1000*(m1-c)/O);
  return {lo,hi,possible:lo<hi && hi>left && lo<right};
}
assert.ok(delta<critical);
assert.ok(oldConservativeCritical(2.3)<delta);
let x=darkGapReachable({left:1.15,right:delta-1.15,mu0:0,mu1:delta,m0:m,m1:m,c,C,O});
assert.equal(x.possible,false);
let yes=darkGapReachable({left:1,right:5,mu0:0,mu1:6,m0:m,m1:m,c,C,O});
assert.equal(yes.possible,true);
let noSupport=darkGapReachable({left:2.5,right:3.5,mu0:0,mu1:6,m0:m,m1:m,c,C,O});
assert.equal(noSupport.possible,false);
let seed=460;
const rand=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296};
let witnessed=0,excluded=0;
for(let i=0;i<10000;i++){
  const d=4+8*rand(), width=.1+.9*rand(),tau=width/2+.1+(d-width-.2)*rand();
  const Cx=50+750*rand(),Ox=50+750*rand(),a=.1+.89*rand(),b=.1+.89*rand();
  const threshold=.1+3*rand();
  const mm0=threshold+a*(Cx/1000)*tau;
  const mm1=threshold+b*(Ox/1000)*(d-tau);
  const r=darkGapReachable({left:width/2,right:d-width/2,mu0:0,mu1:d,
                            m0:mm0,m1:mm1,c:threshold,C:Cx,O:Ox});
  assert.ok(r.possible,"Constructed feasible trajectory excluded");
  // Independent trapezoidal integration of piecewise-linear true witness.
  const f=(t)=>t<=tau?threshold+a*(Cx/1000)*(tau-t):threshold+b*(Ox/1000)*(t-tau);
  assert.ok(Math.abs((f(-width/2)+f(width/2))/2-mm0)<1e-10);
  assert.ok(Math.abs((f(d-width/2)+f(d+width/2))/2-mm1)<1e-10);
  witnessed++;
}
for(let i=0;i<10000;i++){
  const Cx=50+750*rand(),Ox=50+750*rand(),margin=.1+3*rand();
  const crit=1000*margin*(1/Cx+1/Ox);
  const d=crit*(.1+.8*rand()),width=.1*d;
  const r=darkGapReachable({left:width/2,right:d-width/2,mu0:0,mu1:d,
                            m0:margin+2,m1:margin+2,c:2,C:Cx,O:Ox});
  assert.equal(r.possible,false,"Impossible short-gap crossing accepted");
  excluded++;
}
const result={evidence:"SYNTHETIC_ONLY",sample_caps_are_hypothetical:true,
  delta_240_ms:delta,critical_ms:critical,
  old_conservative_2p3ms:oldConservativeCritical(2.3),
  sharp_dark_gap_240:"EXCLUDED_CONDITIONALLY",
  old_surrogate_240_2p3ms:"NOT_EXCLUDED",
  six_ms_2ms_shutter:"POSSIBLE_CONDITIONALLY",
  six_ms_5ms_shutter:"EXCLUDED_CONDITIONALLY",
  constructed_witnesses:witnessed,short_gap_negative_controls:excluded,
  false_exclusions:0,physical_validation:"NOT_ESTABLISHED"};
console.log(JSON.stringify(result,null,2));
