'use strict';
// Independent implementation of the frozen E002-495 scalar bound.
// No imports from the Python executable or its output JSON.
const assert = require('node:assert/strict');
function test({T,e,V,b,c,shouldAlias,shouldFalseExclude}) {
  if (!(T>0 && e>0 && e<=T && V>0 && b>c && c>=0)) throw Error('bad case');
  const g=T-e, m=2*(b-c)/T, tau=g/2;
  const a=t=>c+m*Math.abs(t-tau);
  const trapezoid=(start,end)=>(a(start)+a(end))/2;
  const left=trapezoid(-e,0), right=trapezoid(g,g+e);
  const alias=m<=V;
  const falseExclude=V*g<2*(b-c) && 2*(b-c)<=V*T;
  assert.ok(Math.abs(left-b)<1e-12 && Math.abs(right-b)<1e-12);
  assert.equal(alias,shouldAlias);
  assert.equal(falseExclude,shouldFalseExclude);
  assert.ok(Math.abs(a(tau)-c)<1e-12);
  return {alias,falseExclude,meanLeft:left,meanRight:right,endpoint:a(0),peak:a(-e)};
}
const frozen=test({T:15,e:5,V:.1,b:.7,c:.1,shouldAlias:true,shouldFalseExclude:true});
const excluded=test({T:15,e:5,V:.1,b:.9,c:.1,shouldAlias:false,shouldFalseExclude:false});
const equality=test({T:15,e:5,V:.1,b:.85,c:.1,shouldAlias:true,shouldFalseExclude:true});
const tinyExposure=test({T:15,e:1e-6,V:.1,b:.7,c:.1,shouldAlias:true,shouldFalseExclude:false});
const contiguous=test({T:15,e:15,V:.1,b:.7,c:.1,shouldAlias:true,shouldFalseExclude:true});
console.log(JSON.stringify({experiment:'E002-495',independent_replay:'PASS',frozen,excluded,equality,tinyExposure,contiguous,physical_camera_calibrated:false,release:'BLOCKED'}));
