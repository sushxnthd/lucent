'use strict';
// Independent exact area calculation with rational BigInts.
// Hypothetical sensor model; not human/physical calibration.
const assert = require('node:assert/strict');
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a}
function Q(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}if(!d)throw Error('zero denom');const g=gcd(n,d);return [n/g,d/g]}
const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const sub=(a,b)=>Q(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
const str=a=>a[1]===1n?String(a[0]):String(a[0])+'/'+String(a[1]);
const B=Q(9,10), T=Q(1,100), TWO=Q(2), ZERO=Q(0);
const apex=div(T,TWO);
function aperture(t){
  if(cmp(t,ZERO)<0 || cmp(t,T)>0)return B;
  if(cmp(t,apex)<=0)return sub(B,div(mul(mul(TWO,B),t),T));
  return sub(div(mul(mul(TWO,B),t),T),B);
}
function trapezoidArea(left,right){return mul(div(add(aperture(left),aperture(right)),TWO),sub(right,left))}
function integrated(center,L){
  if(cmp(L,ZERO)<=0)throw Error('nonpositive exposure');
  const lo=sub(center,div(L,TWO)),hi=add(center,div(L,TWO));
  const knots=[lo,ZERO,apex,T,hi].filter(x=>cmp(x,lo)>=0&&cmp(x,hi)<=0).sort((a,b)=>Number(cmp(a,b)));
  let area=ZERO;
  for(let i=1;i<knots.length;i++)if(cmp(knots[i],knots[i-1])>0)area=add(area,trapezoidArea(knots[i-1],knots[i]));
  return div(area,L);
}
assert.equal(str(integrated(apex,Q(1,250))),'9/50');
assert.equal(str(integrated(apex,Q(1,200))),'9/40');
assert.equal(str(integrated(apex,Q(1,100))),'9/20');
assert.equal(str(integrated(apex,Q(1,225))),'1/5');
assert.equal(str(integrated(add(apex,Q(1,1500)),Q(1,250))),'1/5');
assert.equal(str(integrated(add(apex,Q(1,1500)),Q(1,200))),'241/1000');
const width=Q(1,750);
assert.equal(str(mul(Q(200),width)),'4/15');
assert.equal(str(mul(Q(240),width)),'8/25');
console.log(JSON.stringify({independent:'trapezoid exact rational BigInt',minimum_means:['9/50','9/40','9/20'],phase_probabilities:['4/15','8/25'],status:'PASS'}));
