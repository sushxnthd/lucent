'use strict';
// Independent arithmetic, no Python imports. Synthetic model only.
const T=1000/240,w=.006,u=.004,A=.20,eps=.002,theta=.04;
const overlap=(L,n)=>Math.max(0,Math.min(w,L,(w+L)/2-u-T/(2*n)));
const contrast=(L,n)=>A*overlap(L,n)/w-eps;
const thresholdWidth=2*(u+(theta+eps)*w/A)-w;
const assert=(ok,msg)=>{if(!ok)throw new Error(msg)};
assert(Math.abs(thresholdWidth-.00452)<1e-12,'width threshold');
assert(overlap(.0005,1000000)===0,'narrow island');
assert(Math.abs(Math.max(0,Math.min(w,.003,(w+.003)/2-u))-.0005)<1e-12,'positive geometric overlap');
assert(contrast(.003,100000000)<theta,'geometry without detector');
assert(contrast(.006,668)<=theta,'668 insufficient');
assert(contrast(.006,2815)<=theta,'2815 insufficient');
assert(contrast(.006,2816)>theta,'2816 succeeds');
console.log(JSON.stringify({experiment:'E002-481',width_threshold_ms:thresholdWidth,critical_n:2816,
    checks:[668,2815,2816].map(n=>({n,overlap_ms:overlap(.006,n),worst_contrast:contrast(.006,n),detectable:contrast(.006,n)>theta})),
    physical_claim:'ABSTAIN_UNCALIBRATED'},null,2));
