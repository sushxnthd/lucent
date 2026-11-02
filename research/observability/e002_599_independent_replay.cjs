#!/usr/bin/env node
"use strict";
/* E002-599 independent integer-rational geometry and alias oracle.
   Does not import the Python adjudicator or human imagery. */
const assert=require("node:assert/strict");
const phases=[[0,3,6,10,13,16],[1,4,7,11,14,17],[2,5,8,12,15,18]];
function interval(u,l,e,d,delta){
  return {lo:BigInt(Math.max(0,l-u-2*e)),loDen:BigInt(d+delta),
          hi:BigInt(Math.max(0,l-u+2*e)),hiDen:BigInt(d-delta)};
}
function verdict(a,b,cal){
  if(!cal)return "UNCERTAIN";
  const [d,delta,xref,tol,slope]=cal;
  if(slope===undefined)return "UNCERTAIN";
  if(Math.abs(a.x-b.x)>1)return "DISAGREEMENT";
  if(Math.abs(a.x-xref)>tol||Math.abs(b.x-xref)>tol)return "UNCERTAIN";
  const x=interval(a.u,a.l,a.e+slope*Math.abs(a.x-xref),d,delta),
        y=interval(b.u,b.l,b.e+slope*Math.abs(b.x-xref),d,delta);
  if(x.lo*y.hiDen>y.hi*x.loDen||y.lo*x.hiDen>x.hi*y.loDen)return "DISAGREEMENT";
  if(5n*x.hi<=x.hiDen&&5n*y.hi<=y.hiDen)return "CLOSED";
  if(5n*x.lo>x.loDen&&5n*y.lo>y.loDen)return "OPEN";
  return "UNCERTAIN";
}
function witness(states,indices){
 let count=0;
 for(let k=0;k+1<indices.length;k++){
  const left=indices[k],right=indices[k+1];
  if(states[left]==="OPEN"&&states[right]==="OPEN"&&states.slice(left+1,right).includes("CLOSED"))count++;
 }
 return count;
}
const open={u:200,l:240,e:1,x:320},closed={u:200,l:202,e:1,x:320};
assert.equal(verdict(open,open,[100,1,320,1,10]),"OPEN");
assert.equal(verdict(closed,closed,[100,1,320,1,10]),"CLOSED");
assert.equal(verdict(open,open,null),"UNCERTAIN");
const states=Array(19).fill("UNCERTAIN");
states[0]=verdict(open,open,[100,1,320,1,10]);
states[1]=verdict(closed,closed,[100,1,320,1,10]);
states[3]=verdict(open,open,[100,1,320,1,10]);
assert.deepEqual(phases.map(p=>witness(states,p)),[1,0,0]);
const mismatched={u:129,l:130,e:1,x:58};
assert.equal(verdict(mismatched,mismatched,[100,1,320,1,10]),"UNCERTAIN");
assert.equal(verdict(closed,{...closed,x:315},[100,1,320,1,10]),"DISAGREEMENT");
assert.equal(verdict({...closed,x:321},{...closed,x:321},[100,1,320,1,10]),"UNCERTAIN");
assert.equal(verdict(closed,closed,[100,1,320,1]),"UNCERTAIN");
assert.equal(verdict({u:200,l:220,e:2,x:320},{u:200,l:220,e:2,x:320},[100,1,320,1,10]),"UNCERTAIN");
// Exact geometry counterexample: real aperture is 30px at every column,
// cross-column upper at 58 and lower at 0 falsely imply 1px.
const u=x=>100+x/2,l=x=>130+x/2;
assert.equal(l(58)-u(58),30);
assert.equal(l(0)-u(58),1);
assert(30/100>0.2&&1/100<=0.2);
console.log(JSON.stringify({experiment:"E002-599",status:"INDEPENDENT_SYNTHETIC_ORACLE_PASS",
 phase_witnesses:[1,0,0],cross_column_false_closure_refused:true,
 human_rater_pairs:0,physical_shutter_calibrations:0,
 product:"ABSTAIN_UNCALIBRATED",release:"BLOCKED"}));
