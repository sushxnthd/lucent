#!/usr/bin/env node
'use strict';
// E002-542 independent Node.js arithmetic replay; synthetic only.
const assert = require('node:assert/strict');
function code(seed) {
  let state = seed >>> 0, out = [];
  for (let i = 0; i < 800; i++) {
    state = (Math.imul(1664525, state) + 1013904223) >>> 0;
    out.push((state >>> 31) & 1);
  }
  return out;
}
function mean(array, start, length) {
  let total = 0;
  for (let i = start; i < start + length; i++) total += array[i];
  return total / length;
}
function blur(a) {
  return a.map((v, i) => .25 * a[Math.max(i-1, 0)] + .5*v +
    .25*a[Math.min(i+1, a.length-1)]);
}
function fit(reference, response, gamma) {
  const x=[],y=[];
  for (let frame=0; frame<20; frame++) for (let row=0; row<2; row++) {
    const start=frame*33+7+row*5;
    x.push(mean(reference,start,8));
    y.push(.2+.65*Math.pow(mean(response,start,8),gamma));
  }
  const mx=x.reduce((a,b)=>a+b,0)/40;
  const my=y.reduce((a,b)=>a+b,0)/40;
  const gain=x.reduce((a,v,i)=>a+(v-mx)*(y[i]-my),0)/
    x.reduce((a,v)=>a+(v-mx)*(v-mx),0);
  const offset=my-gain*mx;
  return {gain:Math.round(gain*1e6)/1e6,offset:Math.round(offset*1e6)/1e6};
}
function rms(a){return Math.sqrt(a.reduce((s,x)=>s+x*x,0)/a.length);}
const source=code(20261030);
const output={};
for(const gamma of [1,1.6]) {
  const f=fit(source,source,gamma), errors=[];
  for(const amplitude of [.25,.5]) for(let frame=0;frame<20;frame++)
    for(let row=0;row<2;row++) {
      const x=mean(source,frame*33+7+row*5,8);
      errors.push(.2+.65*Math.pow(amplitude*x,gamma)-
        (f.offset+f.gain*amplitude*x));
    }
  output[gamma===1?'linear':'gamma']=rms(errors);
}
const pulse=Array(800).fill(0);
for(let frame=0;frame<20;frame++){
  const t=frame*33+7; pulse[t-1]=1; pulse[t+8]=1;
}
for(const blurred of [false,true]) {
  const f=fit(source,blurred?blur(source):source,1), errors=[];
  const sensed=blurred?blur(pulse):pulse;
  for(let frame=0;frame<20;frame++)for(let row=0;row<2;row++){
    const t=frame*33+7+row*5;
    errors.push(.2+.65*mean(sensed,t,8)-
      (f.offset+f.gain*mean(pulse,t,8)));
  }
  output[blurred?'temporal_blur':'instantaneous']=Math.max(...errors.map(Math.abs));
}
assert.ok(output.linear<1e-8);
assert.ok(Math.abs(output.gamma-.02630673)<1e-6);
assert.ok(output.gamma>.025);
assert.ok(output.instantaneous<1e-8);
assert.ok(Math.abs(output.temporal_blur-.017679)<1e-5);
assert.ok(output.temporal_blur>.015);
console.log(JSON.stringify({independent_replay:'PASS',synthetic_only:true,...output}));
