// E002-625 independent verification of E002-624's sampling-design law.
// Standalone Node.js, no dependencies. Synthetic arithmetic only.
"use strict";
const assert=require("node:assert/strict");
function penalty(h,e,a){if(!(h>0&&e>0&&a>0))throw Error("positive inputs required");return 2*e/h+a*h/2;}
function optimum(e,a){return 2*Math.sqrt(e/a);}
function roots(e,a,b){const d=b*b-4*a*e;if(d<=0)return null;return [(b-Math.sqrt(d))/a,(b+Math.sqrt(d))/a];}
let trials=0;
let state=0x6252026;
function rand(){state=(Math.imul(state,1664525)+1013904223)>>>0;return (state+0.5)/4294967296;}
for(let i=0;i<100000;i++){
 const e=10**(-5+5*rand()),a=10**(1+6*rand());
 const h0=optimum(e,a),floor=2*Math.sqrt(a*e);
 const z=10**(-3+6*rand()),h=z*h0;
 const p=penalty(h,e,a);
 assert.ok(p+1e-9*Math.max(1,floor)>=floor);
 assert.ok(Math.abs(p/floor-(z+1/z)/2)<1e-7*Math.max(1,z,1/z));
 const b=floor*(1.01+4*rand()),rr=roots(e,a,b);
 assert.ok(rr!==null&&rr[0]>0&&rr[0]<h0&&h0<rr[1]);
 const mid=(rr[0]+rr[1])/2;
 assert.ok(penalty(mid,e,a)<b*(1+1e-12));
 assert.ok(penalty(rr[0]/2,e,a)>b);
 assert.ok(penalty(rr[1]*2,e,a)>b);
 assert.equal(roots(e,a,floor*0.99),null);
 trials++;
}
const e=.05,a=10000,h0=optimum(e,a);
assert.ok(Math.abs(h0-.00447213595499958)<1e-12);
assert.ok(Math.abs(penalty(.005,e,a)-45)<1e-10);
console.log(JSON.stringify({experiment:"E002-625",independent_of:"e002_624_sampling_design.py",synthetic_trials:trials,violations:0,example_optimum_seconds:h0,example_penalty_mm_per_second:45,evidence:"independent numeric algebra check only; no physical or human validation"}));
