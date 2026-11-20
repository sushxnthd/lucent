'use strict';
// E002-592 independent exact-rational BigInt replay; no Python results consumed.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let t=a%b;a=b;b=t;}return a;}
function R(a,b=1n){a=BigInt(a);b=BigInt(b);if(!b)throw Error('ZERO_DENOM');if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g];}
const add=(x,y)=>R(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const sub=(x,y)=>R(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>R(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>R(x[0]*y[1],x[1]*y[0]);
const cmp=(x,y)=>{let z=x[0]*y[1]-y[0]*x[1];return z>0n?1:z<0n?-1:0;};
const str=x=>x[1]===1n?''+x[0]:x[0]+'/'+x[1];
const zero=R(0),one=R(1),two=R(2),four=R(4);
function mean(c,tau,d,L){
 if(!(cmp(zero,tau)<=0&&cmp(tau,c)<0&&cmp(c,one)<0&&cmp(zero,d)<0&&cmp(d,one)<0&&cmp(zero,L)<0))throw Error('BAD_DOMAIN');
 let s=sub(one,d),ls=mul(L,s),ct=sub(c,tau),ot=sub(one,tau);
 if(cmp(ls,mul(two,ct))<0)return null;
 if(cmp(ls,mul(two,ot))<=0)return add(tau,div(mul(L,mul(s,s)),four));
 return sub(add(tau,mul(ot,s)),div(mul(ot,ot),L));
}
function verdict(L,k,b,e){
 let c=R(1,2),tau=R(1,10),d=R(3,5),m=mean(c,tau,d,L);
 if(m===null)return ['MODEL_CLOSURE_UNREACHABLE_ONLY',null];
 let margin=sub(mul(k,sub(c,m)),mul(two,add(b,e)));
 return [cmp(margin,zero)>0?'MODEL_SEPARABLE_ONLY':'OVERLAP_ABSTAIN',margin];
}
let fixed=[
 ['low_contrast',R(20),R(1,5),R(1,100),R(1,200),'OVERLAP_ABSTAIN',R(-139,10000)],
 ['high_contrast',R(20),R(3,5),R(1,100),R(1,200),'MODEL_SEPARABLE_ONLY',R(183,10000)],
 ['illumination_drift',R(20),R(3,5),R(1,50),R(1,200),'OVERLAP_ABSTAIN',R(-17,10000)],
 ['high_speed',R(100),R(3,5),R(1,100),R(1,200),'OVERLAP_ABSTAIN',R(-57,50000)],
 ['exact_tangent',R(20),R(60,161),R(1,100),R(1,200),'OVERLAP_ABSTAIN',R(0)]
];
for(let [name,L,k,b,e,expected,margin] of fixed){
 let [actual,m]=verdict(L,k,b,e);
 if(actual!==expected||cmp(m,margin)!==0)throw Error(name+' '+actual+' '+str(m));
}
let knots=[[R(0),R(1,2)],[R(1,50),R(1,10)],[R(31,50),R(1,10)],
           [R(133,200),R(1)],[R(39,40),R(1)],[R(1),R(1,2)]];
let integ=zero;
for(let i=1;i<knots.length;i++){
 let [t,a]=knots[i-1],[u,b]=knots[i],dt=sub(u,t),slope=div(sub(b,a),dt);
 if(cmp(dt,zero)<=0||cmp(slope,R(20))>0||cmp(slope,R(-20))<0)throw Error('INVALID_WITNESS');
 integ=add(integ,div(mul(add(a,b),dt),two));
}
if(cmp(integ,R(839,2000))!==0)throw Error('INTEGRAL');
let state=592>>>0;
function next(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
let counts={MODEL_SEPARABLE_ONLY:0,OVERLAP_ABSTAIN:0,MODEL_CLOSURE_UNREACHABLE_ONLY:0};
for(let i=0;i<1000;i++){
 let L=R(2+next()%119),k=R(1+next()%100,100),b=R(next()%31,1000),e=R(next()%21,1000);
 let [v,margin]=verdict(L,k,b,e),m=mean(R(1,2),R(1,10),R(3,5),L);
 counts[v]++;
 if(m===null){if(v!=='MODEL_CLOSURE_UNREACHABLE_ONLY')throw Error('UNREACHABLE');continue;}
 let upperClosure=add(mul(k,m),add(b,e)),lowerOpen=sub(mul(k,R(1,2)),add(b,e));
 if((cmp(lowerOpen,upperClosure)>0)!==(v==='MODEL_SEPARABLE_ONLY'))throw Error('ENVELOPE');
}
console.log(JSON.stringify({experiment:'E002-592',implementation:'INDEPENDENT_NODE_BIGINT',
 status:'PASS',fixed_cases:fixed.length,witness_integral:str(integ),
 adversarial_trials:1000,seed:592,counts,evidence:'SYNTHETIC_ONLY'}));
