'use strict';
// E002-484: adversarial closure/nonclosure observational alias.
// SYNTHETIC ONLY. Never use to authorize anatomical or fatigue claims.
const KNOTS=[[0,0],[5,1],[15,-1],[20,0]];
const ABSTAIN='ABSTAIN_UNCALIBRATED';
function valid(x,label){if(typeof x!=='number'||!Number.isFinite(x))throw new RangeError(label);}
function deviation(t){
  valid(t,'time');
  if(t<0||t>20)return 0;
  for(let i=0;i<KNOTS.length-1;i++){
    const [a,fa]=KNOTS[i],[b,fb]=KNOTS[i+1];
    if(t>=a&&t<=b)return fa+(fb-fa)*(t-a)/(b-a);
  }
  return 0;
}
function aperture(t,epsilon=0){
  valid(epsilon,'epsilon');if(epsilon<0||epsilon>1)throw new RangeError('epsilon');
  return 1+(1-epsilon)*deviation(t);
}
function integral(a,b,epsilon=0){
  valid(a,'a');valid(b,'b');if(b<a)throw new RangeError('interval');
  const xs=[a,b,...KNOTS.map(p=>p[0]).filter(x=>x>a&&x<b)].sort((x,y)=>x-y);
  let sum=0;
  for(let i=1;i<xs.length;i++)sum+=(xs[i]-xs[i-1])*(aperture(xs[i-1],epsilon)+aperture(xs[i],epsilon))/2;
  return sum;
}
function gates(epsilon=0){return [integral(0,10,epsilon)/10,integral(10,20,epsilon)/10];}
function cosine(t){
  valid(t,'time');if(t<0||t>20)throw new RangeError('time');
  return 1+Math.PI/4*Math.cos(Math.PI*t/20);
}
function cosineGates(){
  // Analytic integration: average cos on [0,10] is 2/pi; on [10,20] is -2/pi.
  return [1.5,.5];
}
function sensorInterval(mean,delta=.1,q=.03){
  valid(mean,'mean');valid(delta,'delta');valid(q,'q');
  if(!(mean>0)||delta<0||delta>=1||q<0)throw new RangeError('sensor');
  return [(1-delta)*mean-q,(1+delta)*mean+q];
}
function intersection(a,b){return [Math.max(a[0],b[0]),Math.min(a[1],b[1])];}
function threshold(delta=.1,q=.03){
  valid(delta,'delta');valid(q,'q');
  if(delta<0||delta>=1||q<0)throw new RangeError('nuisance');
  const first=(6*delta+4*q)/(1+delta);
  const second=(2*delta+4*q)/(1-delta);
  return {first_gate:first,second_gate:second,maximum_epsilon:Math.min(first,second)};
}
function compare(epsilon=.35,delta=.1,q=.03){
  valid(epsilon,'epsilon');if(!(epsilon>0&&epsilon<=1))throw new RangeError('epsilon');
  const closure=gates(0),nonclosure=gates(epsilon);
  const c=closure.map(m=>sensorInterval(m,delta,q));
  const n=nonclosure.map(m=>sensorInterval(m,delta,q));
  const overlap=c.map((x,i)=>intersection(x,n[i]));
  const possible=overlap.every(x=>x[0]<=x[1]+1e-12);
  const bound=threshold(delta,q);
  return {epsilon_mm:epsilon,delta,q,closure_gates_mm:closure,nonclosure_gates_mm:nonclosure,
    closure_intervals_mm:c,nonclosure_intervals_mm:n,overlap_mm:overlap,
    identical_observation_possible:possible,threshold_mm:bound,
    analytic_prediction:epsilon<=bound.maximum_epsilon+1e-12,
    closure_min_mm:0,nonclosure_min_mm:epsilon,
    closure_max_speed_mm_per_ms:.2,nonclosure_max_speed_mm_per_ms:.2*(1-epsilon),
    endpoints_both_mm:[1,1,1],physical_closure_inferred:false};
}
function experiment(){
  const primary=compare(.35,.1,.03);
  const observed=[1.4,.578];
  const witness=primary.overlap_mm.every((r,i)=>observed[i]>=r[0]&&observed[i]<=r[1]);
  return {experiment:'E002-484',evidence:'SYNTHETIC_IDENTIFIABILITY_FALSIFICATION',
    primary,common_observation_mm:observed,common_observation_valid:witness,
    noise_only_positive:compare(.10,0,.03),
    noise_only_negative:compare(.13,0,.03),
    threshold_negative:compare(.36,.1,.03),
    noiseless_scaled_negative:compare(.35,0,0),
    noiseless_unanchored_cosine:{gate_means_mm:cosineGates(),minimum_mm:1-Math.PI/4,
      maximum_speed_mm_per_ms:Math.PI*Math.PI/80,
      endpoint_authenticated:false,identical_to_closure_gates:true},
    claim:'TWO_GATES_DO_NOT_IDENTIFY_CLOSURE_WITHOUT_STRONGER_INDEPENDENT_CONSTRAINTS',
    physical_shutter_acquisitions:0,new_human_reference_sequences:0,
    anatomical_claim:ABSTAIN,physically_validated:false};
}
module.exports={deviation,aperture,integral,gates,cosine,cosineGates,sensorInterval,intersection,threshold,compare,experiment};
if(require.main===module)console.log(JSON.stringify(experiment(),null,2));
