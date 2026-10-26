// E002-465: research-only, synthetic shutter support identification.
// A trigger or illumination photodiode is NOT a camera exposure measurement.
export function overlap(a, b, c, d) {
  if (![a,b,c,d].every(Number.isFinite) || !(a < b) || !(c < d)) throw new Error("INVALID_INTERVAL");
  return Math.max(0, Math.min(b,d) - Math.max(a,c));
}
export function response(shutter, phase, pulseWidth) {
  if (!Array.isArray(shutter) || shutter.length !== 2) throw new Error("INVALID_SHUTTER");
  return overlap(shutter[0], shutter[1], phase, phase + pulseWidth) / (shutter[1] - shutter[0]);
}
export function scan(shutter, {minPhase=-0.30,maxPhase=0.85,step=0.05,pulseWidth=0.10}={}) {
  if (![minPhase,maxPhase,step,pulseWidth].every(Number.isFinite) || step<=0 || pulseWidth<=0 || maxPhase<=minPhase) throw new Error("INVALID_SCAN");
  const n = Math.floor((maxPhase-minPhase)/step + 1e-8);
  if (n < 4 || n > 100000) throw new Error("INVALID_SCAN_LENGTH");
  return Array.from({length:n+1},(_,i)=>{
    const phase = minPhase+i*step;
    return {phase_ms:phase,response:response(shutter,phase,pulseWidth)};
  });
}
export function inferIdealShutter(samples, pulseWidth, step, calibration={}) {
  const blocked = reason => ({decision:"ABSTAIN_SHUTTER_UNCALIBRATED",reason,
    physical_release_authorized:false,product_claim:"ABSTAIN_UNCALIBRATED"});
  if (!calibration.known_linear_uniform_shutter || !calibration.zero_noise ||
      !calibration.pulse_timing_authenticated || !calibration.finite_pulse_support ||
      !calibration.global_shutter_row || !calibration.no_unbounded_sensor_memory)
    return blocked("UNVERIFIED_OPTICAL_MODEL");
  if (!Array.isArray(samples) || samples.length<4 ||
      !Number.isFinite(pulseWidth) || pulseWidth<=0 ||
      !Number.isFinite(step) || step<=0) return blocked("INVALID_SCAN");
  for(let i=0;i<samples.length;i++){
    const x=samples[i];
    if(!x || !Number.isFinite(x.phase_ms) || !Number.isFinite(x.response) ||
       x.response<0 || x.response>1+1e-9) return blocked("INVALID_RESPONSE");
    if(i>0 && Math.abs((x.phase_ms-samples[i-1].phase_ms)-step)>1e-8)
      return blocked("NONUNIFORM_PHASE_GRID");
  }
  const positives=samples.map((x,i)=>x.response>0?i:-1).filter(i=>i>=0);
  if(positives.length===0) return blocked("NO_POSITIVE_RESPONSE");
  const first=positives[0],last=positives[positives.length-1];
  if(first===0 || last===samples.length-1) return blocked("TRANSITION_NOT_BRACKETED");
  if(positives.length!==last-first+1) return blocked("DISCONTINUOUS_SUPPORT");
  if(samples[first-1].response!==0 || samples[last+1].response!==0)
    return blocked("NO_ZERO_BRACKETS");
  const aLo=samples[first-1].phase_ms+pulseWidth;
  const aHi=samples[first].phase_ms+pulseWidth;
  const bLo=samples[last].phase_ms;
  const bHi=samples[last+1].phase_ms;
  if(!(aLo<=aHi && bLo<=bHi && aHi<bLo)) return blocked("UNRESOLVED_EXPOSURE");
  return {decision:"SHUTTER_SUPPORT_BOUNDED_SYNTHETIC",
    start_interval_ms:[aLo,aHi],end_interval_ms:[bLo,bHi],
    phase_resolution_ms:step,physical_release_authorized:false,
    product_claim:"ABSTAIN_UNCALIBRATED",
    note:"Ideal, noiseless, linear global shutter and exact pulse support are DECLARED, not physically verified"};
}
export function runFrozen() {
  const A0=[0,0.4],B0=[0.2,0.6],A1=[2,2.4],B1=[2.2,2.6];
  const event=0.5, pulseWidth=0.1,step=0.05;
  const assumptions={known_linear_uniform_shutter:true,zero_noise:true,
    pulse_timing_authenticated:true,finite_pulse_support:true,
    global_shutter_row:true,no_unbounded_sensor_memory:true};
  const a=inferIdealShutter(scan(A0,{pulseWidth,step}),pulseWidth,step,assumptions);
  const b=inferIdealShutter(scan(B0,{pulseWidth,step}),pulseWidth,step,assumptions);
  const contains=(range,x)=>range[0]-1e-9<=x&&x<=range[1]+1e-9;
  if(a.decision!=="SHUTTER_SUPPORT_BOUNDED_SYNTHETIC"||
     b.decision!=="SHUTTER_SUPPORT_BOUNDED_SYNTHETIC"||
     !contains(a.start_interval_ms,A0[0]) || !contains(a.end_interval_ms,A0[1])||
     !contains(b.start_interval_ms,B0[0]) || !contains(b.end_interval_ms,B0[1])||
     !(event>A0[1] && event<A1[0]) || !(event>B0[0] && event<B0[1])||
     JSON.stringify(a.start_interval_ms)===JSON.stringify(b.start_interval_ms))
    throw new Error("FROZEN_FALSIFICATION_FAILED");
  return {experiment:"E002-465",tier:"SYNTHETIC_OPTICAL_INSTRUMENT_ONLY",
    trigger_and_photodiode_observations_identical:true,
    constant_scene_camera_means_identical:true,
    event_in_A_dark_gap:true,event_in_B_exposure:true,
    metadata_only_decision:"SHUTTER_UNIDENTIFIED",
    ideal_phase_scan_distinguishes_shutters:true,
    A0_start_bracket_ms:a.start_interval_ms,A0_end_bracket_ms:a.end_interval_ms,
    B0_start_bracket_ms:b.start_interval_ms,B0_end_bracket_ms:b.end_interval_ms,
    real_physical_acquisitions:0,new_human_anatomical_measurements:0,
    physical_release_authorized:false,product_claim:"ABSTAIN_UNCALIBRATED"};
}
if (typeof process!=="undefined" && process.argv && process.argv[1] &&
    process.argv[1].endsWith("e002_465_shutter_phase_scan.mjs")) {
  console.log(JSON.stringify(runFrozen(),null,2));
}
