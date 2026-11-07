// E002-466: synthetic-only threshold-aware shutter phase-scan falsification.
// This module never certifies a physical camera.
export const abstain = reason => ({decision:'ABSTAIN_SHUTTER_UNCALIBRATED',reason,physical_release_authorized:false,product_claim:'ABSTAIN_UNCALIBRATED'});
export function exactOverlap(a,b,t,p) {
  if (![a,b,t,p].every(Number.isFinite) || !(b>a) || !(p>0)) throw Error('INVALID_GEOMETRY');
  return Math.max(0,Math.min(b,t+p)-Math.max(a,t));
}
export function syntheticDetections({start,end,pulseWidth,threshold,gain=1,minPhase=-0.3,maxPhase=0.85,step=0.05}) {
  if (![start,end,pulseWidth,threshold,gain,minPhase,maxPhase,step].every(Number.isFinite) ||
      !(end>start) || pulseWidth<=0 || threshold<0 || gain<=0 || step<=0 || maxPhase<=minPhase)
    throw Error('INVALID_SYNTHETIC_SETTINGS');
  const n=Math.floor((maxPhase-minPhase)/step+1e-8);
  if(n<4 || n>100000) throw Error('INVALID_PHASE_COUNT');
  return Array.from({length:n+1},(_,i)=>{
    const phase_ms=minPhase+i*step;
    const response=gain*exactOverlap(start,end,phase_ms,pulseWidth)/(end-start);
    return {phase_ms,detected:response>threshold};
  });
}
export function inferThresholdedShutter(samples,pulseWidth,step,cal={}) {
  if (!cal.known_linear_uniform_shutter || !cal.zero_noise ||
      !cal.pulse_timing_authenticated || !cal.finite_pulse_support ||
      !cal.global_shutter_row || !cal.no_unbounded_sensor_memory ||
      !cal.threshold_authenticated || !cal.gain_lower_bound_authenticated ||
      !cal.exposure_width_upper_bound_authenticated || !cal.no_clipping)
    return abstain('UNVERIFIED_OPTICAL_MODEL');
  const {threshold,minimum_gain,max_exposure_width_ms}=cal;
  if (![pulseWidth,step,threshold,minimum_gain,max_exposure_width_ms].every(Number.isFinite) ||
      pulseWidth<=0 || step<=0 || threshold<0 || minimum_gain<=0 || max_exposure_width_ms<=0 ||
      !Array.isArray(samples) || samples.length<4 || samples.length>100001)
    return abstain('INVALID_CALIBRATION_OR_SCAN');
  for(let i=0;i<samples.length;i++) {
    const x=samples[i];
    if(!x || !Number.isFinite(x.phase_ms) || typeof x.detected!=='boolean')
      return abstain('INVALID_SAMPLE');
    if(i>0 && Math.abs(x.phase_ms-samples[i-1].phase_ms-step)>1e-8)
      return abstain('MISSING_OR_NONUNIFORM_PHASE');
  }
  const positives=samples.map((x,i)=>x.detected?i:-1).filter(i=>i>=0);
  if(!positives.length) return abstain('NO_DETECTIONS');
  const first=positives[0],last=positives[positives.length-1];
  if(first===0 || last===samples.length-1) return abstain('UNBRACKETED_TRANSITION');
  if(positives.length!==last-first+1) return abstain('NONUNIMODAL_DETECTIONS');
  const delta=threshold*max_exposure_width_ms/minimum_gain;
  const epsilon=1e-10; // Numerical outward slack, NOT physical uncertainty.
  const start=[samples[first-1].phase_ms+pulseWidth-delta-epsilon,
               samples[first].phase_ms+pulseWidth+epsilon];
  const end=[samples[last].phase_ms-epsilon,
             samples[last+1].phase_ms+delta+epsilon];
  if(start.some(x=>!Number.isFinite(x)) || end.some(x=>!Number.isFinite(x)) ||
     !(start[0]<=start[1] && end[0]<=end[1] && start[1]<end[0]))
    return abstain('UNRESOLVED_EXPOSURE');
  return {decision:'SHUTTER_SUPPORT_BOUNDED_SYNTHETIC',
    start_interval_ms:start,end_interval_ms:end,detector_dead_zone_ms:delta,
    physical_release_authorized:false,product_claim:'ABSTAIN_UNCALIBRATED',
    evidence_tier:'SYNTHETIC_IDEAL_NOISELESS_WITH_KNOWN_DETECTION_FLOOR'};
}
export function runFrozen() {
  const settings={start:0,end:0.4,pulseWidth:0.1,threshold:0.15,step:0.05};
  const samples=syntheticDetections(settings);
  const first=samples.findIndex(s=>s.detected);
  const last=samples.findLastIndex(s=>s.detected);
  const naiveStart=[samples[first-1].phase_ms+settings.pulseWidth,
                    samples[first].phase_ms+settings.pulseWidth];
  const naiveEnd=[samples[last].phase_ms,samples[last+1].phase_ms];
  const calibrated={known_linear_uniform_shutter:true,zero_noise:true,
    pulse_timing_authenticated:true,finite_pulse_support:true,global_shutter_row:true,
    no_unbounded_sensor_memory:true,threshold_authenticated:true,
    gain_lower_bound_authenticated:true,exposure_width_upper_bound_authenticated:true,
    no_clipping:true,threshold:0.15,minimum_gain:1,max_exposure_width_ms:0.4};
  const corrected=inferThresholdedShutter(samples,settings.pulseWidth,settings.step,calibrated);
  const contains=(v,r)=>r[0]<=v && v<=r[1];
  if(contains(settings.start,naiveStart) || contains(settings.end,naiveEnd) ||
     corrected.decision!=='SHUTTER_SUPPORT_BOUNDED_SYNTHETIC' ||
     !contains(settings.start,corrected.start_interval_ms) ||
     !contains(settings.end,corrected.end_interval_ms))
    throw Error('FROZEN_DETECTION_FLOOR_FALSIFICATION_FAILED');
  return {experiment:'E002-466',settings,naiveStart,naiveEnd,
    naive_false_start_bracket:true,naive_false_end_bracket:true,
    corrected,real_physical_acquisitions:0,new_human_anatomical_measurements:0};
}
if (process.argv[1]?.endsWith('e002_466_thresholded_phase_scan.mjs'))
  console.log(JSON.stringify(runFrozen(),null,2));
