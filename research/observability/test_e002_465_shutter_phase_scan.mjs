import test from "node:test";
import assert from "node:assert/strict";
import {overlap,response,scan,inferIdealShutter,runFrozen} from "./e002_465_shutter_phase_scan.mjs";
const assumptions={known_linear_uniform_shutter:true,zero_noise:true,
  pulse_timing_authenticated:true,finite_pulse_support:true,
  global_shutter_row:true,no_unbounded_sensor_memory:true};
const evaluate=(s,opts=assumptions)=>inferIdealShutter(s,0.1,0.05,opts);
test("frozen A/B counterexample and zero physical claims",()=>{
  const r=runFrozen();
  assert.equal(r.event_in_A_dark_gap,true);
  assert.equal(r.event_in_B_exposure,true);
  assert.equal(r.real_physical_acquisitions,0);
  assert.equal(r.physical_release_authorized,false);
});
test("independent analytic overlap check",()=>{
  assert.equal(overlap(0,0.4,0.1,0.2),0.1);
  assert.equal(overlap(0,0.4,0.5,0.6),0);
  assert.ok(Math.abs(response([0,0.4],0.1,0.1)-0.25)<1e-12);
});
test("both shutter worlds have different optical pulse response",()=>{
  assert.equal(response([0,0.4],-0.05,0.1)>0,true);
  assert.equal(response([0.2,0.6],-0.05,0.1),0);
});
test("ideal brackets enclose actual start/end for unseen offset",()=>{
  const shutter=[0.137,0.573],s=scan(shutter,{minPhase:-0.4,maxPhase:0.9});
  const r=evaluate(s);
  assert.equal(r.decision,"SHUTTER_SUPPORT_BOUNDED_SYNTHETIC");
  assert.ok(r.start_interval_ms[0]<=shutter[0] && shutter[0]<=r.start_interval_ms[1]);
  assert.ok(r.end_interval_ms[0]<=shutter[1] && shutter[1]<=r.end_interval_ms[1]);
});
test("zero-noise assumption missing forces abstention",()=>{
  const r=evaluate(scan([0,0.4]),{...assumptions,zero_noise:false});
  assert.equal(r.decision,"ABSTAIN_SHUTTER_UNCALIBRATED");
});
test("unverified optical pulse timing forces abstention",()=>{
  assert.equal(evaluate(scan([0,0.4]),{...assumptions,pulse_timing_authenticated:false}).decision,
    "ABSTAIN_SHUTTER_UNCALIBRATED");
});
test("rolling shutter row not certified forces abstention",()=>{
  assert.equal(evaluate(scan([0,0.4]),{...assumptions,global_shutter_row:false}).decision,
    "ABSTAIN_SHUTTER_UNCALIBRATED");
});
test("sensor memory unknown forces abstention",()=>{
  assert.equal(evaluate(scan([0,0.4]),{...assumptions,no_unbounded_sensor_memory:false}).decision,
    "ABSTAIN_SHUTTER_UNCALIBRATED");
});
test("missing transition bracket forces abstention",()=>{
  assert.equal(evaluate(scan([0,0.4],{minPhase:0.05,maxPhase:0.25})).decision,
    "ABSTAIN_SHUTTER_UNCALIBRATED");
});
test("nonuniform or missing phase forces abstention",()=>{
  const s=scan([0,0.4]);s[4].phase_ms+=0.01;
  assert.equal(evaluate(s).decision,"ABSTAIN_SHUTTER_UNCALIBRATED");
});
test("discontinuous positive responses force abstention",()=>{
  const s=scan([0,0.4]);const i=s.findIndex(x=>x.response>0)+2;
  s[i].response=0;
  assert.equal(evaluate(s).decision,"ABSTAIN_SHUTTER_UNCALIBRATED");
});
test("unknown or nonfinite radiometry forces abstention",()=>{
  const s=scan([0,0.4]);s[5].response=NaN;
  assert.equal(evaluate(s).decision,"ABSTAIN_SHUTTER_UNCALIBRATED");
});
