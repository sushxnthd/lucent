'use strict';
// E002-482: synthetic exposure-integrated moving-aperture witness, not physical data.
const PERIOD_MS=1000/30,EXPOSURE_MS=20,BASE_MM=1,AMPLITUDE_MM=1;
const ABSTAIN='ABSTAIN_UNCALIBRATED';
function positive(x,label){if(typeof x!=='number'||!Number.isFinite(x)||x<=0)throw new RangeError(label);}
function deviation(t,e=EXPOSURE_MS,a=AMPLITUDE_MM){
  positive(e,'exposure');
  if(typeof a!=='number'||!Number.isFinite(a)||a<0)throw new RangeError('amplitude');
  if(typeof t!=='number'||!Number.isFinite(t))throw new RangeError('time');
  if(t<0||t>e)return 0;
  const x=t/e;
  return x<=.25?4*a*x:x<=.75?2*a-4*a*x:4*a*(x-1);
}
function aperture(t,moving=true){return BASE_MM+(moving?deviation(t):0);}
function integralDeviation(a,b){
  if(![a,b].every(x=>typeof x==='number'&&Number.isFinite(x))||b<a)throw new RangeError('interval');
  const knots=[a,b,0,EXPOSURE_MS/4,3*EXPOSURE_MS/4,EXPOSURE_MS].filter(t=>t>=a&&t<=b).sort((x,y)=>x-y);
  let sum=0;
  for(let i=1;i<knots.length;i++)sum+=(knots[i]-knots[i-1])*(deviation(knots[i])+deviation(knots[i-1]))/2;
  return sum;
}
function meanAperture(rowOffsetMs=0,moving=true){
  if(typeof rowOffsetMs!=='number'||!Number.isFinite(rowOffsetMs)||rowOffsetMs<0||rowOffsetMs+EXPOSURE_MS>PERIOD_MS)throw new RangeError('row offset');
  return BASE_MM+(moving?integralDeviation(rowOffsetMs,rowOffsetMs+EXPOSURE_MS)/EXPOSURE_MS:0);
}
// Abramowitz-Stegun 7.1.26; absolute erf approximation error <=1.5e-7.
function erf(x){
  const sign=x<0?-1:1; x=Math.abs(x);
  const t=1/(1+.3275911*x);
  const y=1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-.284496736)*t+.254829592)*t*Math.exp(-x*x);
  return sign*y;
}
function Phi(z){return .5*(1+erf(z/Math.SQRT2));}
function phi(z){return Math.exp(-z*z/2)/Math.sqrt(2*Math.PI);}
function H(z){return z*Phi(z)+phi(z);}
function spatial(y,sigma,moving=true){
  positive(sigma,'blur');
  if(typeof y!=='number'||!Number.isFinite(y))throw new RangeError('position');
  if(!moving)return Phi((BASE_MM-y)/sigma);
  const lo=BASE_MM-AMPLITUDE_MM,hi=BASE_MM+AMPLITUDE_MM;
  return sigma/(hi-lo)*(H((hi-y)/sigma)-H((lo-y)/sigma));
}
function numericSpatial(y,sigma,n=8000){
  if(!Number.isInteger(n)||n<=0)throw new RangeError('quadrature count');
  let sum=0;
  for(let k=0;k<n;k++)sum+=Phi((aperture((k+.5)*EXPOSURE_MS/n)-y)/sigma);
  return sum/n;
}
function affineWitness(sigma,step=.1){
  positive(step,'pixel pitch');
  const ys=[];
  for(let i=0;i<=Math.round(4/step);i++)ys.push(-1+i*step);
  const stationary=ys.map(y=>spatial(y,sigma,false)),moving=ys.map(y=>spatial(y,sigma,true));
  const avg=x=>x.reduce((a,b)=>a+b,0)/x.length;
  const xbar=avg(stationary),ybar=avg(moving);
  const covariance=stationary.reduce((s,x,i)=>s+(x-xbar)*(moving[i]-ybar),0);
  const variance=stationary.reduce((s,x)=>s+(x-xbar)**2,0);
  if(variance<1e-16)throw new RangeError('unidentifiable affine fit');
  const gain=covariance/variance,offset=ybar-gain*xbar;
  const maxCalibratedDifference=Math.max(...stationary.map((x,i)=>Math.abs(x-moving[i])));
  const maxAffineResidual=Math.max(...stationary.map((x,i)=>Math.abs(gain*x+offset-moving[i])));
  return {sigma_mm:sigma,pixels:ys.length,pitch_mm:step,gain,offset,max_calibrated_difference:maxCalibratedDifference,max_affine_residual:maxAffineResidual,overlap_exists_at_0p01_per_world:maxAffineResidual<=.02};
}
function rollingGuaranteedDifference(offsetMs,uncertaintyMs=0){
  if(![offsetMs,uncertaintyMs].every(x=>typeof x==='number'&&Number.isFinite(x))||uncertaintyMs<0||offsetMs-uncertaintyMs<0||offsetMs+uncertaintyMs+EXPOSURE_MS>PERIOD_MS)throw new RangeError('unverified clock range');
  const lo=offsetMs-uncertaintyMs,hi=offsetMs+uncertaintyMs;
  const candidate=[lo,hi];
  if(lo<=EXPOSURE_MS/2&&hi>=EXPOSURE_MS/2)candidate.push(EXPOSURE_MS/2);
  return Math.min(...candidate.map(d=>Math.abs(meanAperture(d,false)-meanAperture(d,true))));
}
function maskedResidual(sigma,keep){
  positive(sigma,'blur');
  if(typeof keep!=='function')throw new RangeError('mask');
  const full=affineWitness(sigma);
  let max=0,count=0;
  for(let i=0;i<=40;i++){
    const y=-1+i*.1;
    if(!keep(y))continue;
    count++;
    max=Math.max(max,Math.abs(full.gain*spatial(y,sigma,false)+full.offset-spatial(y,sigma,true)));
  }
  if(!count)throw new RangeError('no visible pixels');
  return {visible_pixels:count,max_residual:max,observational_overlap:max<=.02};
}
function experiment(){
  const quadrature=[];
  for(const sigma of [.2,1,2])for(const y of [0,.5,1,1.5,2])quadrature.push(Math.abs(spatial(y,sigma)-numericSpatial(y,sigma)));
  return {experiment:'E002-482',tier:'SYNTHETIC_MOVING_APERTURE_AND_SPATIAL_FORWARD_MODEL',
    period_ms:PERIOD_MS,exposure_ms:EXPOSURE_MS,minimum_moving_aperture_mm:0,
    moving_peak_speed_mm_per_s:1000*4*AMPLITUDE_MM/EXPOSURE_MS,
    scalar_stationary_mm:meanAperture(0,false),scalar_moving_mm:meanAperture(0,true),
    rolling_2ms_moving_mm:meanAperture(2,true),rolling_5ms_moving_mm:meanAperture(5,true),
    rolling_2ms_pm2ms_guaranteed_difference_mm:rollingGuaranteedDifference(2,2),
    rolling_5ms_pm1ms_guaranteed_difference_mm:rollingGuaranteedDifference(5,1),
    occluded_half_pixels:maskedResidual(1,y=>y<=1),
    spatial_cases:[.2,1,2].map(s=>affineWitness(s)),
    max_independent_quadrature_discrepancy:Math.max(...quadrature),
    physical_shutter_acquisitions:0,new_human_reference_sequences:0,
    anatomical_claim:ABSTAIN,physically_validated:false};
}
module.exports={deviation,aperture,integralDeviation,meanAperture,Phi,spatial,numericSpatial,affineWitness,rollingGuaranteedDifference,maskedResidual,experiment};
if(require.main===module)console.log(JSON.stringify(experiment(),null,2));
