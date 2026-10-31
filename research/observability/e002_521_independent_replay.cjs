#!/usr/bin/env node
'use strict';
// E002-521 independent BigInt rational replay, no Python imports or packages.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;}
function rat(n,d=1n){if(d===0n)throw Error('zero denominator');if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return [n/g,d/g];}
function dec(s){s=String(s);if(!/^-?\d+(\.\d+)?$/.test(s))throw Error('invalid decimal');let sign=s[0]==='-'?-1n:1n;if(sign<0n)s=s.slice(1);let [a,b='']=s.split('.');return rat(sign*BigInt(a+b),10n**BigInt(b.length));}
function add([a,b],[c,d]){return rat(a*d+b*c,b*d);}
function mul([a,b],[c,d]){return rat(a*c,b*d);}
function div([a,b],[c,d]){return rat(a*d,b*c);}
function sub(a,b){return add(a,mul(dec(-1),b));}
function lt([a,b],[c,d]){return a*d<c*b;}
function eq([a,b],[c,d]){return a*d===c*b;}
function fmt([a,b]){return b===1n?String(a):String(a)+'/'+String(b);}
function check(ok,msg){if(!ok)throw Error('FAILED: '+msg);}
const theta=dec('0.20'), U=dec('0.19'), K=dec('1'), B=dec('0'), w=dec('8');
const M=add(mul(K,U),B);
const p=sub(dec('1'),div(M,theta));
const duration=mul(w,p);
check(fmt(p)==='1/20' && fmt(duration)==='2/5','frozen 0.05 and 0.4 ms');
check(lt(theta,mul(dec('1.2'),U)),'transport reversal');
check(eq(theta,mul(dec('1'),dec('0.20'))),'contact-only equality');
const seq=[];
for(const e of ['0.01','0.001','0.0001','0.00001']){
  const high=add(theta,dec(e));
  const closure=sub(dec('1'),div(U,high));
  const exactMean=mul(sub(dec('1'),closure),high);
  check(eq(exactMean,U),'two-level construction mean');
  check(lt(p,closure),'sharp infimum approached from above');
  seq.push({epsilon:e,closure_fraction:fmt(closure)});
}
// Nonuniform shutter: all optical weight concentrated in epsilon fraction
// with aperture zero there, 1 elsewhere. Weighted mean=0, physical
// closure fraction=epsilon, which can be arbitrarily small.
for(const e of ['0.01','0.000001']){
 const epsilon=dec(e);
 const weightedMean=mul(div(dec('1'),epsilon),mul(epsilon,dec('0')));
 check(eq(weightedMean,dec('0')),'nonuniform optical mean');
 check(lt(epsilon,dec('0.1')),'small physical closure time');
}
console.log(JSON.stringify({experiment:'E002-521',independent:'BigInt exact rational',fraction:fmt(p),duration_ms:fmt(duration),two_level_approach:seq,nonuniform_shutter_counterexample:true,physical_human_validation:false,product:'ABSTAIN_UNCALIBRATED',release:'BLOCKED'}));
