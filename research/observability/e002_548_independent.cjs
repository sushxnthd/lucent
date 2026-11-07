'use strict';
// Independent BigInt exact-rational check for a CONSTRUCTED 10-ms triangular
// closure at a nominal 150-Hz reference rate. NOT a human measurement.
function gcd(a,b) { while (b) { [a,b]=[b,a%b]; } return a<0n?-a:a; }
function rat(a,b=1n) { if(b===0n) throw Error('zero denominator'); const g=gcd(a,b); return [a/g,b/g]; }
function mul(x,y) { return rat(x[0]*y[0],x[1]*y[1]); }
function eq(x,y) { return x[0]*y[1]===y[0]*x[1]; }
const threshold=rat(1n,5n), velocity=rat(180n), exposure=rat(1n,250n), fps=rat(150n);
const mean=rat(velocity[0]*exposure[0],velocity[1]*exposure[1]*4n);
if(!eq(mean,rat(9n,50n))) throw Error('centered mean mismatch');
const phase=rat(1n,750n), detection=mul(fps,phase);
if(!eq(detection,rat(1n,5n))) throw Error('150-fps phase probability mismatch');
const fiveMsMean=rat(180n,800n);
if(!eq(fiveMsMean,rat(9n,40n))) throw Error('5ms centered mean mismatch');
if(fiveMsMean[0]*threshold[1]<=threshold[0]*fiveMsMean[1]) throw Error('5ms should erase threshold');
process.stdout.write('E002-548 independent exact-rational checks passed: 150fps/4ms 1/5, 150fps/5ms 0 (constructed only)\n');
