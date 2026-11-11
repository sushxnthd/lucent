import test from 'node:test';
import assert from 'node:assert/strict';
import {syntheticDetections,inferThresholdedShutter,runFrozen} from './e002_466_thresholded_phase_scan.mjs';
const cal={known_linear_uniform_shutter:true,zero_noise:true,pulse_timing_authenticated:true,
  finite_pulse_support:true,global_shutter_row:true,no_unbounded_sensor_memory:true,
  threshold_authenticated:true,gain_lower_bound_authenticated:true,
  exposure_width_upper_bound_authenticated:true,no_clipping:true,
  threshold:0.15,minimum_gain:1,max_exposure_width_ms:0.4};
const samples=()=>syntheticDetections({start:0,end:0.4,pulseWidth:0.1,threshold:0.15});
const run=(s=samples(),c=cal)=>inferThresholdedShutter(s,0.1,0.05,c);
test('frozen false shutter support and repaired bounded support',()=>{
  const r=runFrozen();assert.equal(r.naive_false_start_bracket,true);
  assert.equal(r.naive_false_end_bracket,true);
  assert.equal(r.corrected.physical_release_authorized,false);
});
test('known threshold zero restores ideal zero/nonzero bracket',()=>{
  const s=syntheticDetections({start:0,end:0.4,pulseWidth:0.1,threshold:0});
  const r=run(s,{...cal,threshold:0});
  assert.equal(r.decision,'SHUTTER_SUPPORT_BOUNDED_SYNTHETIC');
  assert.equal(r.detector_dead_zone_ms,0);
  assert.ok(r.start_interval_ms[0]<=0 && r.start_interval_ms[1]>=0);
  assert.ok(r.end_interval_ms[0]<=0.4 && r.end_interval_ms[1]>=0.4);
});
for(const [name,patch] of [
  ['unverified floor',{threshold_authenticated:false}],
  ['unverified gain',{gain_lower_bound_authenticated:false}],
  ['unverified exposure width',{exposure_width_upper_bound_authenticated:false}],
  ['noise',{zero_noise:false}],
  ['clipping',{no_clipping:false}],
  ['rolling row',{global_shutter_row:false}],
  ['pulse tail',{finite_pulse_support:false}],
  ['sensor lag',{no_unbounded_sensor_memory:false}],
  ['clock error',{pulse_timing_authenticated:false}],
  ['nonlinear response',{known_linear_uniform_shutter:false}]
]) test('fail closed: '+name,()=>assert.equal(run(samples(),{...cal,...patch}).decision,'ABSTAIN_SHUTTER_UNCALIBRATED'));
test('missing phase fails closed',()=>{const s=samples();s.splice(3,1);assert.equal(run(s).decision,'ABSTAIN_SHUTTER_UNCALIBRATED');});
test('unknown detection state fails closed',()=>{const s=samples();s[3].detected=null;assert.equal(run(s).decision,'ABSTAIN_SHUTTER_UNCALIBRATED');});
test('no detections fail closed',()=>assert.equal(run(samples().map(x=>({...x,detected:false}))).decision,'ABSTAIN_SHUTTER_UNCALIBRATED'));
test('inconsistent detections fail closed',()=>{const s=samples();s[s.findIndex(x=>x.detected)+2].detected=false;assert.equal(run(s).decision,'ABSTAIN_SHUTTER_UNCALIBRATED');});
test('held-out nuisance sweep: accepted bounds enclose true shutter endpoints',()=>{
  let seed=0x466,accepted=0,abstained=0;
  const random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
  for(let i=0;i<10000;i++){
    const start=-0.12+random()*0.42,width=0.25+random()*0.30,
      gain=0.8+random()*0.6,threshold=random()*0.20,
      minPhase=-0.50+random()*0.02;
    const s=syntheticDetections({start,end:start+width,pulseWidth:0.08,
      threshold,gain,minPhase,maxPhase:1.1,step:0.025});
    const c={...cal,threshold,minimum_gain:0.75,max_exposure_width_ms:0.6};
    const r=inferThresholdedShutter(s,0.08,0.025,c);
    if(r.decision==='ABSTAIN_SHUTTER_UNCALIBRATED'){abstained++;continue;}
    accepted++;
    assert.ok(r.start_interval_ms[0]<=start+1e-9 && start<=r.start_interval_ms[1]+1e-9,'start '+i);
    assert.ok(r.end_interval_ms[0]<=start+width+1e-9 && start+width<=r.end_interval_ms[1]+1e-9,'end '+i);
    assert.equal(r.physical_release_authorized,false);
  }
  assert.ok(accepted>1000);
  console.log(JSON.stringify({heldout_synthetic_cases:10000,accepted,abstained,failures:0}));
});
