'use strict';
// E002-590 independent exact BigInt replay; no Python outputs are read.
const assert=require('node:assert/strict');
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n}
function q(a,b=1n){a=BigInt(a);b=BigInt(b);assert(b!==0n);if(b<0n){a=-a;b=-b}let g=gcd(a,b);return [a/g,b/g]}
function add(x,y){return q(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
function neg(x){return [-x[0],x[1]]}
function sub(x,y){return add(x,neg(y))}
function mul(x,y){return q(x[0]*y[0],x[1]*y[1])}
function div(x,y){return q(x[0]*y[1],x[1]*y[0])}
function cmp(x,y){let a=x[0]*y[1],b=y[0]*x[1];return a<b?-1:a>b?1:0}
function eq(x,y){return cmp(x,y)===0}
const Z=q(0),O=q(1),TWO=q(2),FOUR=q(4),HALF=q(1,2);
function critical(c){return cmp(c,HALF)<=0?mul(FOUR,c):div(O,sub(O,c))}
function maxMean(L){return cmp(L,TWO)<=0?div(L,FOUR):sub(O,div(O,L))}
function extremizer(c,L){assert(cmp(L,mul(TWO,c))>=0);let t=div(c,L);
 if(cmp(L,TWO)<=0)return [[Z,c],[t,Z],[add(t,HALF),div(L,TWO)],[O,c]];
 return [[Z,c],[t,Z],[div(add(c,O),L),O],[sub(O,div(sub(O,c),L)),O],[O,c]];
}
function integrate(points,L){let area=Z,maxSlope=Z;
 for(let i=1;i<points.length;i++){
 let [t0,y0]=points[i-1], [t1,y1]=points[i];assert(cmp(t1,t0)>0);
 let dt=sub(t1,t0),dy=sub(y1,y0),s=div(dy,dt);if(cmp(s,Z)<0)s=neg(s);
 if(cmp(s,maxSlope)>0)maxSlope=s;
 area=add(area,mul(dt,div(add(y0,y1),TWO)));
 assert(cmp(y0,Z)>=0&&cmp(y0,O)<=0);
 }
 assert(cmp(maxSlope,L)<=0);
 assert(eq(points[0][1],points.at(-1)[1]));
 assert(points.some(([t,a])=>eq(a,Z)));
 return area;
}
let count=0;
for(let n=1;n<20;n++){
 let c=q(n,20),L=critical(c),area=integrate(extremizer(c,L),L);
 assert(eq(area,c));
 let lower=mul(L,q(99,100));
 assert(cmp(lower,mul(TWO,c))>=0);
 assert(cmp(maxMean(lower),c)<0);
 count++;
}
for(const c of [q(1,5),q(1,2),q(4,5)]){
 let L=critical(c);assert(eq(integrate(extremizer(c,L),L),c));
}
assert(eq(mul(critical(q(1,5)),q(30)),q(24)));
assert(eq(mul(critical(q(1,2)),q(30)),q(60)));
assert(eq(mul(critical(q(4,5)),q(30)),q(150)));
console.log(JSON.stringify({replay:'PASS',exact_grid_cases:count,
  critical_witnesses:'3/3',subthreshold_rejections:count,
  evidence:'idealized synthetic operator only'}));
