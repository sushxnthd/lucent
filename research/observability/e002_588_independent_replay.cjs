'use strict';
// Independent BigInt rational reconstruction of E002-588; no Python functions reused.
const fs = require('fs');
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const t=a%b;a=b;b=t;}return a;}
function q(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error('zero denominator');if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];}
function add(x,y){return q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);}
function neg(x){return [-x[0],x[1]];}
function sub(x,y){return add(x,neg(y));}
function mul(x,y){return q(x[0]*y[0],x[1]*y[1]);}
function div(x,y){return q(x[0]*y[1],x[1]*y[0]);}
function cmp(x,y){const z=x[0]*y[1]-y[0]*x[1];return z<0n?-1:z>0n?1:0;}
function eq(x,y){return cmp(x,y)===0;}
function parse(s){const [a,b='1']=s.split('/');return q(a,b);}
const Z=q(0),O=q(1),D=q(1,10),startA=q(21,10),expA=q(4),startB=q(2),expB=q(9,2);
const knots=[[Z,Z],[q(1,9),q(1,40)],[q(8,9),q(9,10)],[O,O]];
function raw(row,phase,start,exp,delay=D){const begin=add(start,mul(q(row),delay));const frac=div(sub(add(begin,exp),phase),exp);if(cmp(frac,Z)<0)return Z;if(cmp(frac,O)>0)return O;return frac;}
function tone(x){for(let i=1;i<knots.length;i++){let [xl,yl]=knots[i-1],[xr,yr]=knots[i];if(cmp(x,xr)<=0)return add(yl,mul(div(sub(x,xl),sub(xr,xl)),sub(yr,yl)));}throw Error('bad x');}
function assert(c,m){if(!c)throw Error(m);}
const input=JSON.parse(fs.readFileSync(0,'utf8'));
assert(input.samples.length===75,'sample count');
let count=0, sat=0;
for(const row of [0,20,40])for(let k=0;k<=24;k++){
 const phase=q(k,2), item=input.samples[count++];
 assert(item.row===row&&eq(parse(item.phase),phase),'phase/row ordering');
 const ya=raw(row,phase,startA,expA),yb=tone(raw(row,phase,startB,expB));
 assert(eq(ya,yb),'two worlds differ at '+row+'/'+k);
 assert(eq(ya,parse(item.A))&&eq(yb,parse(item.B)),'Python mismatch');
 if(eq(ya,Z)||eq(ya,O))sat++;
}
assert(sat===input.saturated_count,'saturation mismatch');
const gapA=sub(q(100,3),add(mul(q(40),D),expA));
const gapB=sub(q(100,3),add(mul(q(40),D),expB));
assert(eq(sub(gapA,gapB),q(1,2)),'gap difference');
assert(eq(parse(input.gap_A_ms),gapA)&&eq(parse(input.gap_B_ms),gapB),'gap Python mismatch');
const probe=q(25,4);
assert(eq(raw(0,probe,startA,expA),Z),'heldout A');
assert(eq(tone(raw(0,probe,startB,expB)),q(1,80)),'heldout B');
assert(eq(parse(input.heldout_A),Z)&&eq(parse(input.heldout_B),q(1,80)),'heldout Python mismatch');
assert(!eq(raw(0,q(6),startB,expB),raw(0,q(6),startA,expA)),'identity control');
assert(!eq(tone(raw(20,q(5),startB,expB,q(101,1000))),raw(20,q(5),startA,expA)),'delay control');
console.log('PASS independent Node BigInt: 75/75 equal, gap 1/2 ms, heldout 0 vs 1/80, controls');
