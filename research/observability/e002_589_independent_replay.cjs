'use strict';
// E002-589 independent BigInt rational replay. No Python-generated data read.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b]}return a||1n}
function F(n,d=1n){n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d}if(!d)throw Error('zero denominator');let g=gcd(n,d);return [n/g,d/g]}
const add=(a,b)=>F(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const neg=a=>F(-a[0],a[1]);
const sub=(a,b)=>add(a,neg(b));
const mul=(a,b)=>F(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>F(a[0]*b[1],a[1]*b[0]);
const cmp=(a,b)=>a[0]*b[1]<b[0]*a[1]?-1:a[0]*b[1]>b[0]*a[1]?1:0;
const eq=(a,b)=>cmp(a,b)===0;
const min=(a,b)=>cmp(a,b)<0?a:b;
const max=(a,b)=>cmp(a,b)>0?a:b;
const q=(n,d=1)=>F(n,d);
const O=[[q(0),q(1,2)],[q(1),q(1,2)]];
const C=[[q(0),q(1,2)],[q(1,8),q(1,2)],[q(1,4),q(0)],[q(3,8),q(1,2)],[q(5,8),q(1,2)],[q(3,4),q(1)],[q(7,8),q(1,2)],[q(1),q(1,2)]];
function val(K,t){for(let i=0;i<K.length-1;i++){let [t0,y0]=K[i],[t1,y1]=K[i+1];if(cmp(t,t1)<=0)return add(y0,mul(sub(y1,y0),div(sub(t,t0),sub(t1,t0))))}throw Error('outside frame')}
function integrate(K,l,r,power=1){let z=q(0);for(let i=0;i<K.length-1;i++){let a=max(l,K[i][0]),b=min(r,K[i+1][0]);if(cmp(a,b)>=0)continue;let u=val(K,a),v=val(K,b),h=sub(b,a);let mean=power===1?div(add(u,v),q(2)):div(add(add(mul(u,u),mul(u,v)),mul(v,v)),q(3));z=add(z,mul(h,mean))}return z}
function periodic(K,lo,hi,power=1){let s=q(0),cur=lo;while(cmp(cur,hi)<0){let k=cur[0]/cur[1];let e=min(hi,q(k+1n));let a=sub(cur,q(k)),b=sub(e,q(k));s=add(s,integrate(K,a,b,power));cur=e}return div(s,sub(hi,lo))}
function assertEq(actual,expected,label){if(!eq(actual,expected))throw Error(label+': '+actual.join('/')+' != '+expected.join('/'))}
function slope(K){let maxSlope=q(0);for(let i=0;i<K.length-1;i++){let v=div(sub(K[i+1][1],K[i][1]),sub(K[i+1][0],K[i][0]));if(cmp(v,q(0))<0)v=neg(v);maxSlope=max(maxSlope,v)}return maxSlope}
assertEq(slope(C),q(4),'slope');assertEq(slope(O),q(0),'constant');
assertEq(val(C,q(1,4)),q(0),'closure');assertEq(val(C,q(1,5)),q(1,5),'closure threshold entering');assertEq(val(C,q(3,10)),q(1,5),'closure threshold leaving');
for(let k=0;k<24;k++){assertEq(periodic(O,q(k),q(k+1)),q(1,2),'open frame '+k);assertEq(periodic(C,q(k),q(k+1)),q(1,2),'closed frame '+k)}
assertEq(periodic(C,q(0),q(1,2)),q(3,8),'first half');assertEq(periodic(C,q(1,2),q(1)),q(5,8),'second half');
assertEq(periodic(C,q(1,4),q(3,4)),q(1,2),'phase blind spot');assertEq(periodic(C,q(1,8),q(9,8)),q(1,2),'full-duty phase shift');
assertEq(periodic(O,q(0),q(1),2),q(1,4),'nonlinear O');assertEq(periodic(C,q(0),q(1),2),q(7,24),'nonlinear C');
const altered=C.map(([t,y])=>[t,eq(t,q(3,4))?q(9,10):y]);assertEq(periodic(altered,q(0),q(1)),q(39,80),'peak perturbation');
assertEq(add(mul(periodic(C,q(0),q(1)),q(3,2)),q(1,8)),q(7,8),'gain');
assertEq(sub(q(1,2),div(q(3,5),q(2))),q(1,5),'speed certificate boundary');
console.log(JSON.stringify({experiment:'E002-589',independent_bigint_rational_replay:'PASS',full_duty_frames:24,closure_interval:['1/5','3/10'],first_half_closed:'3/8',second_half_closed:'5/8',nonlinear_closed:'7/24',perturbed_closed:'39/80',human_data:false,physical_sensor:false}));
