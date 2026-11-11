'use strict';
// Independent finite subthreshold support calculation; no Python imports.
const C=567.103928/1000,O=274.616337/1000,c=2;
const cases=[{fps:400,b:2.3,m:1.95,d:.1,tau:.9},
             {fps:1000,b:2.1,m:1.98,d:.03,tau:.38}];
const out=cases.map(({fps,b,m,d,tau})=>{
  const left=tau-(b-m)/C,right=tau+d+(b-m)/O;
  const sub=d+(c-m)*(1/C+1/O),dark=[.15,1000/fps-.15];
  const identical=left>dark[0]&&right<dark[1];
  if(!identical||sub<=0)throw Error('Frozen finite-duration prediction falsified');
  return {fps,baseline_mm:b,minimum_mm:m,excursion_support_ms:[left,right],
    subthreshold_duration_ms:sub,identical_to_constant_open:identical,
    physical_certification:false};
});
console.log(JSON.stringify({experiment:'E002-462 finite-dwell supplement',
  verification:'PASS',cases:out}));
