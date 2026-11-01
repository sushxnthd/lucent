'use strict';
// Independent finite-grid replay: separate JS implementation of the optical-step model.
const clip = x => Math.max(0, Math.min(1, x));
const response = (start, length, phase) => clip(1 - (phase - start) / length);
const rows = [0, 20, 40];
const phases = Array.from({length:25},(_,i)=>i/2);
const observations = rows.flatMap(row => phases.map(phase => ({row,phase,y:response(2+.1*row,4,phase)})));
function fit(phaseError, intensityError) {
  const feasible = [];
  for(let is0=0;is0<=8;is0++) for(let ie=4;ie<=12;ie++) for(let id=0;id<=4;id++) {
    const s0=is0/2, E=ie/2, d=id/20;
    const good=observations.every(o=> {
      const start=s0+o.row*d;
      const low=response(start,E,o.phase+phaseError);
      const high=response(start,E,o.phase-phaseError);
      return low<=o.y+intensityError+1e-10 && high>=o.y-intensityError-1e-10;
    });
    if(good) feasible.push({s0,E,d});
  }
  return {count:feasible.length,support:Object.fromEntries(rows.map(row=>[String(row),[
    Math.min(...feasible.map(c=>c.s0+row*c.d)),
    Math.max(...feasible.map(c=>c.s0+row*c.d+c.E))
  ]]))};
}
const exact=fit(0,0), uncertain=fit(.5,.1);
const expected={0:[2,6],20:[4,8],40:[6,10]};
if(exact.count!==1 || JSON.stringify(exact.support)!==JSON.stringify(expected)) throw Error('exact mismatch '+JSON.stringify(exact));
if(uncertain.count!==14 || JSON.stringify(uncertain.support)!==JSON.stringify({0:[1,7],20:[3,9],40:[5,11]})) throw Error('uncertain mismatch '+JSON.stringify(uncertain));
console.log(JSON.stringify({independent_replay:'PASS',exact,uncertain,physical_evidence:false}));
