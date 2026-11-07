// Independent E002-604 replay: direct geometric integration of a triangle via piecewise trapezoids.
// No Python import or shared numerical implementation.
const assert = require('node:assert/strict');
const width = 0.010, threshold = 0.2, n = 10000;
function deficit(t) { return Math.max(0, 1 - 2 * Math.abs(t) / width); }
function exposureMean(center, duration) {
  const lo = center - duration / 2, hi = center + duration / 2;
  const cuts = [lo, -width/2, 0, width/2, hi].filter(x => x >= lo && x <= hi).sort((a,b)=>a-b);
  let integral = 0;
  for (let i=1;i<cuts.length;i++) {
    const a=cuts[i-1], b=cuts[i];
    integral += (b-a)*(deficit(a)+deficit(b))/2;
  }
  return 1 - integral/duration;
}
function missed(fps, exposure, point=false) {
  const T = 1/fps; let nmiss = 0;
  for (let j=0;j<n;j++) {
    const phase = T*j/n; let detected = false;
    for (let k=-4;k<=4;k++) {
      const c=k*T+phase;
      const y=point ? 1-deficit(c) : exposureMean(c,exposure);
      if (y<=threshold) {detected=true;break;}
    }
    if (!detected) nmiss++;
  }
  return nmiss/n;
}
const minima=[.002,.005,.010,.020].map(e=>({exposure_ms: +(e*1000).toFixed(6),predicted_min_aperture:+(e<=width ? e/(2*width) : 1-width/(2*e)).toFixed(9),integrated_min_aperture:+exposureMean(0,e).toFixed(9)}));
const cases=[[30,.020],[95,.005],[95,.002]].map(([fps,e])=>({fps,exposure_ms:+(e*1000).toFixed(6),average_missed_fraction:missed(fps,e),point_missed_fraction:missed(fps,e,true)}));
for (const m of minima) assert.ok(Math.abs(m.predicted_min_aperture-m.integrated_min_aperture)<1e-9,m);
assert.equal(cases[0].average_missed_fraction,1);
assert.equal(cases[1].average_missed_fraction,1);
console.log(JSON.stringify({experiment:'E002-604',phase_count:n,minima,cases}));
