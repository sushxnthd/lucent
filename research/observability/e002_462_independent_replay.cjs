'use strict';
// Independent analytical shutter-support check, no Python imports.
const C=567.103928/1000,O=274.616337/1000,c=2.0;
function reference(fps,b,tau,width){
  const dt=1000/fps,left=tau-(b-c)/C,right=tau+(b-c)/O;
  const intervals=Array.from({length:12},(_,i)=>{
    const t=(i-4)*dt;return [t-width/2,t+width/2];
  });
  const disjoint=intervals.every(([a,z])=>z<=left||a>=right);
  return {fps,b,tau,width,disjoint,darkGap:dt-width,
          critical:(b-c)*(1/C+1/O),physical_certification:false};
}
const a=reference(400,2.3,1.0,.3),b=reference(1000,2.1,.4,.3);
if(!a.disjoint||!b.disjoint)throw Error('Frozen counterexample failed');
if(!(a.critical<a.darkGap&&b.critical<b.darkGap))
  throw Error('Critical gap sanity failed');
const c2000=reference(2000,2.1,.25,.3);
if(c2000.disjoint)throw Error('2000-fps reference unexpectedly missed excursion');
console.log(JSON.stringify({experiment:'E002-462',primary:[a,b],
  negative_2000:c2000,verification:'PASS',evidence_tier:'SYNTHETIC_ONLY'}));
