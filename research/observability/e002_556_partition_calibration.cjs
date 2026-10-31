#!/usr/bin/env node
// E002-556: complete-support shutter calibration with conservative variance and blinded holdouts.
// Usage: node e002_556_partition_calibration.cjs <capture.json> OR --self-test
"use strict";
const fs=require("node:fs");
function calibrate(input) {
  const fail=m=>{throw Error(m)};
  const num=(v,name,min=-Infinity)=>{if(typeof v!=="number"||!Number.isFinite(v)||v<min)fail("invalid "+name);return v};
  if(!input||!Array.isArray(input.bins)||input.bins.length<8)fail(">=8 complete-support bins required");
  const clock=num(input.timing_abs_error_us,"clock uncertainty",0);
  const supportStart=num(input.support_start_us,"support start");
  const supportEnd=num(input.support_end_us,"support end");
  if(!(supportEnd>supportStart))fail("invalid support");
  const bins=input.bins.map((b,i)=>{
    const a=num(b.start_us,"bin start"),z=num(b.end_us,"bin end");
    if(!(z>a))fail("nonpositive bin");
    if(i===0&&Math.abs(a-supportStart)>1e-9)fail("unmeasured shutter leading edge");
    if(i>0&&Math.abs(a-input.bins[i-1].end_us)>1e-9)fail("partition gap or overlap");
    if(i===input.bins.length-1&&Math.abs(z-supportEnd)>1e-9)fail("unmeasured shutter trailing edge");
    if(!Array.isArray(b.reps)||b.reps.length<3)fail(">=3 replicates per bin required");
    let qlo=0,qhi=Infinity;
    for(const r of b.reps){
      const c=num(r.camera,"camera",0),ce=num(r.camera_error,"camera error",0);
      const p=num(r.photo,"photo",0),pe=num(r.photo_error,"photo error",0);
      if(!(p>pe))fail("photodiode amplitude unbounded");
      qlo=Math.max(qlo,Math.max(0,c-ce)/(p+pe));
      qhi=Math.min(qhi,(c+ce)/(p-pe));
    }
    if(qlo>qhi+1e-12)fail("replicate response intervals inconsistent");
    return {a:a-clock,z:z+clock,qlo,qhi};
  });
  const L=bins.reduce((s,b)=>s+b.qlo,0),U=bins.reduce((s,b)=>s+b.qhi,0);
  if(!(L>0&&U>0))fail("zero or unbounded gain");
  let vlo=0,vhi=0;
  for(let i=0;i<bins.length;i++){
    const a=bins[i],width=a.z-a.a;
    vhi+=0.5*a.qhi*a.qhi*width*width/(L*L);
    for(let j=i+1;j<bins.length;j++){
      const b=bins[j],dlo=Math.max(0,b.a-a.z),dhi=b.z-a.a;
      vlo+=a.qlo*b.qlo*dlo*dlo/(U*U);
      vhi+=a.qhi*b.qhi*dhi*dhi/(L*L);
    }
  }
  if(!Array.isArray(input.holdouts)||input.holdouts.length<4)fail(">=4 independent composite holdouts required");
  let failures=0;
  const holdouts=input.holdouts.map((h,k)=>{
    if(!Array.isArray(h.pattern)||h.pattern.length!==bins.length)fail("holdout length mismatch");
    const pat=h.pattern.map(v=>num(v,"pattern",0));
    if(pat.every(v=>v===pat[0]))fail("uninformative holdout");
    const observed=num(h.observed,"observed",0),error=num(h.abs_error,"holdout error",0);
    const low=pat.reduce((s,v,i)=>s+v*bins[i].qlo,0)/U;
    const high=pat.reduce((s,v,i)=>s+v*bins[i].qhi,0)/L;
    const rejected=observed+error<low-1e-12||observed-error>high+1e-12;
    if(rejected)failures++;
    return {index:k,predicted:[low,high],observed:[Math.max(0,observed-error),observed+error],falsified:rejected};
  });
  return {evidence_tier:"model_or_unauthenticated_capture_only",status:failures?"CALIBRATION_FALSIFIED":"MODEL_CONSISTENT_UNAUTHENTICATED",variance_us2:[Math.max(0,vlo),vhi],bins:bins.length,holdouts:holdouts.length,failed_holdouts:failures,holdout_details:holdouts,product:"ABSTAIN_UNCALIBRATED",release:"BLOCKED",limitations:"Requires independently verified full support, physical clock, raw linear camera response, photodiode calibration, shutter row, and optical geometry. No anatomical certification."};
}
const FIXTURE={"demo":{"support_start_us":0,"support_end_us":8000,"timing_abs_error_us":2,"bins":[{"start_us":0,"end_us":1000,"reps":[{"camera":1,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":1,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":1,"camera_error":0.02,"photo":1,"photo_error":0.001}]},{"start_us":1000,"end_us":2000,"reps":[{"camera":2,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":2,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":2,"camera_error":0.02,"photo":1,"photo_error":0.001}]},{"start_us":2000,"end_us":3000,"reps":[{"camera":3,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":3,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":3,"camera_error":0.02,"photo":1,"photo_error":0.001}]},{"start_us":3000,"end_us":4000,"reps":[{"camera":4,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":4,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":4,"camera_error":0.02,"photo":1,"photo_error":0.001}]},{"start_us":4000,"end_us":5000,"reps":[{"camera":4,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":4,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":4,"camera_error":0.02,"photo":1,"photo_error":0.001}]},{"start_us":5000,"end_us":6000,"reps":[{"camera":3,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":3,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":3,"camera_error":0.02,"photo":1,"photo_error":0.001}]},{"start_us":6000,"end_us":7000,"reps":[{"camera":2,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":2,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":2,"camera_error":0.02,"photo":1,"photo_error":0.001}]},{"start_us":7000,"end_us":8000,"reps":[{"camera":1,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":1,"camera_error":0.02,"photo":1,"photo_error":0.001},{"camera":1,"camera_error":0.02,"photo":1,"photo_error":0.001}]}],"holdouts":[{"pattern":[1,0,1,0,1,0,1,0],"observed":0.5,"abs_error":0.002},{"pattern":[1,1,1,1,0,0,0,0],"observed":0.5,"abs_error":0.002},{"pattern":[0,0,0,1,1,0,0,0],"observed":0.4,"abs_error":0.002},{"pattern":[1,0,0,0,0,0,0,1],"observed":0.1,"abs_error":0.002}]},"actual":3333333.3333333335};
if(require.main===module){
 if(process.argv[2]==="--self-test"){
  const r=calibrate(FIXTURE.demo);
  if(r.status!=="MODEL_CONSISTENT_UNAUTHENTICATED"||r.variance_us2[0]>FIXTURE.actual||r.variance_us2[1]<FIXTURE.actual)process.exit(1);
  const bad=JSON.parse(JSON.stringify(FIXTURE.demo));bad.holdouts[0].observed=.99;
  if(calibrate(bad).status!=="CALIBRATION_FALSIFIED")process.exit(1);
  console.log("E002-556 PASS: synthetic variance containment and holdout falsification");
 }else{
  if(!process.argv[2]){console.error("Usage: node e002_556_partition_calibration.cjs capture.json");process.exit(2)}
  try{console.log(JSON.stringify(calibrate(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2))}
  catch(e){console.error("ABSTAIN: "+e.message);process.exit(2)}
 }
}
module.exports={calibrate};
