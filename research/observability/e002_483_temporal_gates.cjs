'use strict';
// E002-483: synthetic complementary exposure gates; no physical or human data.
const GATE_MS=10, BASE_MM=1, ABSTAIN='ABSTAIN_UNCALIBRATED';
const knots=[[0,0],[5,1],[15,-1],[20,0]];
function finite(x,name){if(typeof x!=='number'||!Number.isFinite(x))throw new RangeError(name);}
function deviation(t){
  finite(t,'time');
  if(t<0||t>20)return 0;
  for(let i=0;i<knots.length-1;i++){
    const [a,fa]=knots[i],[b,fb]=knots[i+1];
    if(t>=a&&t<=b)return fa+(fb-fa)*(t-a)/(b-a);
  }
  return 0;
}
function integral(a,b){
  finite(a,'start');finite(b,'end');if(b<a)throw new RangeError('interval');
  const xs=[a,b,...knots.map(k=>k[0]).filter(x=>x>a&&x<b)].sort((x,y)=>x-y);
  let out=0;for(let i=1;i<xs.length;i++)out+=(xs[i]-xs[i-1])*(deviation(xs[i])+deviation(xs[i-1]))/2;
  return out;
}
function means(phaseMs=0,moving=true){
  finite(phaseMs,'phase');if(phaseMs < -10||phaseMs > 13)throw new RangeError('phase outside frame');
  if(!moving)return [BASE_MM,BASE_MM];
  return [BASE_MM+integral(phaseMs,phaseMs+GATE_MS)/GATE_MS,BASE_MM+integral(phaseMs+GATE_MS,phaseMs+2*GATE_MS)/GATE_MS];
}
function contrast(y1,y2){if(!(y1>0&&y2>0&&Number.isFinite(y1)&&Number.isFinite(y2)))throw new RangeError('nonpositive sensor');return (y1-y2)/(y1+y2);}
function contrastInterval(pair,drift=.1,additive=.03){
  finite(drift,'gain drift');finite(additive,'additive');
  if(drift<0||drift>=1||additive<0||!Array.isArray(pair)||pair.length!==2)throw new RangeError('nuisance');
  const [m1,m2]=pair;for(const m of pair)if(!(m>0&&Number.isFinite(m)))throw new RangeError('aperture mean');
  const xlo=(1-drift)*m1-additive,xhi=(1+drift)*m1+additive;
  const ylo=(1-drift)*m2-additive,yhi=(1+drift)*m2+additive;
  if(xlo<=0||ylo<=0)throw new RangeError('unbounded contrast due to nonpositive signal');
  return {low:contrast(xlo,yhi),high:contrast(xhi,ylo)};
}
function compare(phaseMs=0,drift=.1,additive=.03){
  const stationary=contrastInterval(means(phaseMs,false),drift,additive);
  const moving=contrastInterval(means(phaseMs,true),drift,additive);
  const margin=Math.max(moving.low-stationary.high,stationary.low-moving.high);
  return {phase_ms:phaseMs,stationary,moving,margin,certified_distinguishable:margin>0};
}
function experiment(){
  const baseline=compare(),holdout=[-2,-1.5,-.5,.5,1.5,2].map(s=>compare(s));
  const grid=[];for(let i=0;i<=4000;i++)grid.push(compare(-2+i*.001));
  const minGridMargin=Math.min(...grid.map(x=>x.margin));
  // For |s|<=2, |d(mean)/ds|<=0.2 mm/ms and m1>=1.1, m2>=0.1.
  // Hence dC_min/ds magnitude <= 2*(1.1*0.2)/(.9*1.1+1.1*.1)=0.4/ms.
  // Nearest grid sample within 0.0005 ms: subtract 0.0002 from the margin.
  const certifiedContinuumLowerBound=minGridMargin-.0002;
  return {experiment:'E002-483',tier:'SYNTHETIC_COMPLEMENTARY_GATE_INSTRUMENT',
    full_exposure_scalar_alias_mm:1,gate_ms:GATE_MS,stationary_gate_means_mm:means(0,false),
    moving_gate_means_mm:means(0,true),baseline,holdout,
    phase_pm2_grid_min_margin:minGridMargin,phase_pm2_continuum_margin_lower_bound:certifiedContinuumLowerBound,
    phase_pm2_certified:certifiedContinuumLowerBound>0,
    phase_pm5_controls:[compare(-5),compare(5)],
    independent_gain_30pct_control:compare(0,.3,.03),
    additive_25pct_control:compare(0,.1,.25),
    physical_shutter_acquisitions:0,new_human_reference_sequences:0,
    anatomical_claim:ABSTAIN,physically_validated:false};
}
module.exports={deviation,integral,means,contrast,contrastInterval,compare,experiment};
if(require.main===module)console.log(JSON.stringify(experiment(),null,2));
