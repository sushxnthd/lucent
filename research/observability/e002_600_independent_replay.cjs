#!/usr/bin/env node
'use strict';
// Independent Node oracle for E002-600 reviewer scores; no Python imports.
// It does not authenticate reviewer identity, source imagery or shutter timing.
const fs = require('node:fs');
const allowed = new Set(['UNREVIEWED','OCCLUSION','BLUR','GAZE','GLASSES','GEOMETRY','BRIGHTNESS','MISSING','OTHER']);
function oracle(truth,review){
  if(truth.experiment!=='E002-600'||truth.iris_diameter_px!==100||
     review.experiment!=='E002-574'||!['A','B'].includes(review.rater)||
     Object.hasOwn(review,'arm')) throw Error('INVALID_PACKET');
  const keys=Object.keys(truth.clips).sort();
  if(keys.length!==10||Object.keys(review.clips).sort().join('|')!==keys.join('|')) throw Error('INVALID_CLIPS');
  let clean=0,measured=0,covered=0,falseClosed=0,falseOpen=0,nuisance=0,abstainedNuisance=0;
  let cleanOpen=0,cleanClosed=0,correctOpen=0,correctClosed=0,ambiguousMeasured=0;
  for(const clip of keys){
    const gs=truth.clips[clip],rs=review.clips[clip];
    if(!Array.isArray(gs)||!Array.isArray(rs)||gs.length!==19||rs.length!==19) throw Error('INVALID_FRAME_COUNT');
    for(let i=0;i<19;i++){
      const g=gs[i],r=rs[i];
      if(r.frame!==i||!Array.isArray(r.flags)||r.flags.length>1||r.flags.some(f=>!allowed.has(f))) throw Error('INVALID_FRAME');
      const has=r.flags.length===0;
      const expected=has?['flags','frame','iris_diameter','lower_y','measurement_x','uncertainty_px','upper_y']:
        ['flags','frame','iris_diameter','lower_y','uncertainty_px','upper_y'];
      if(Object.keys(r).sort().join('|')!==expected.join('|')||r.iris_diameter!==null) throw Error('INVALID_KEYS');
      if(has){
        const {upper_y:u,lower_y:l,uncertainty_px:e,measurement_x:x}=r;
        if(![u,l,e,x].every(v=>typeof v==='number'&&Number.isFinite(v))||
           !(u>=0&&l>u&&l<=480&&e>=.5&&e<=50&&x>=0&&x<=639)) throw Error('INVALID_COORDS');
      }else if([r.upper_y,r.lower_y,r.uncertainty_px].some(v=>v!==null)) throw Error('INVALID_ABSTENTION');
      if(!g.clean){nuisance++;if(!has)abstainedNuisance++;continue;}
      clean++;
      const truthClosed=g.gap_px<=20;
      if(truthClosed)cleanClosed++;else cleanOpen++;
      if(!has)continue;
      measured++;
      const trueU=g.upper_at_x320+g.slope*(r.measurement_x-320);
      const trueL=g.lower_at_x320+g.slope*(r.measurement_x-320);
      const truthGap=trueL-trueU;
      const observed=r.lower_y-r.upper_y;
      const lo=Math.max(0,observed-2*r.uncertainty_px);
      const hi=observed+2*r.uncertainty_px;
      if(lo-1e-9<=truthGap&&truthGap<=hi+1e-9)covered++;
      const pred=hi/100<=.2?'CLOSED':lo/100>.2?'OPEN':'ABSTAIN';
      if(truthGap>20&&pred==='CLOSED')falseClosed++;
      if(truthGap<=20&&pred==='OPEN')falseOpen++;
      if(pred==='ABSTAIN')ambiguousMeasured++;
      else if(pred==='OPEN'&&!truthClosed)correctOpen++;
      else if(pred==='CLOSED'&&truthClosed)correctClosed++;
    }
  }
  const qualified=measured*100>=80*clean&&covered*100>=95*measured&&falseClosed<=1&&falseOpen<=1&&
    cleanOpen>0&&cleanClosed>0&&nuisance>0&&
    correctOpen*100>=80*cleanOpen&&correctClosed*100>=80*cleanClosed&&
    abstainedNuisance*100>=75*nuisance;
  return {experiment:'E002-600',rater:review.rater,clean_frames:clean,clean_measured:measured,
    clean_interval_covered:covered,clean_open_frames:cleanOpen,clean_closed_frames:cleanClosed,
    correct_decisive_open:correctOpen,correct_decisive_closed:correctClosed,
    ambiguous_measured:ambiguousMeasured,
    clean_false_closed:falseClosed,clean_false_open:falseOpen,
    nuisance_frames:nuisance,nuisance_abstentions:abstainedNuisance,
    qualified_on_synthetic_challenge:qualified,human_validation_of_E002_371:false,
    evidence_tier:'SYNTHETIC_REVIEWER_QUALIFICATION_ONLY',product:'ABSTAIN_UNCALIBRATED',release:'BLOCKED'};
}
if(require.main===module){
  const [truthPath,reviewPath]=process.argv.slice(2);
  if(!truthPath||!reviewPath){console.error('Usage: node e002_600_independent_replay.cjs truth.json review.json');process.exit(2);}
  try{
    console.log(JSON.stringify(oracle(JSON.parse(fs.readFileSync(truthPath)),JSON.parse(fs.readFileSync(reviewPath)))));
  }catch(e){console.error('ABSTAIN:',e.message);process.exit(2);}
}
module.exports={oracle};
