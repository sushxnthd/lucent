// E002-594 independent exact BigInt replay; does not import Python outputs.
const assert=require('node:assert/strict');
const gcd=(a,b)=>b===0n?(a<0n?-a:a):gcd(b,a%b);
const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return [n/g,d/g]};
const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>Q(a[0]*b[1],a[1]*b[0]);
const eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
const str=x=>x[1]===1n?`${x[0]}`:`${x[0]}/${x[1]}`;
const h=Q(1,100), A=Q(200), e=Q(1,500), two=Q(2);
const accel=div(mul(A,h),two);
const flat=accel;
const noisy=add(div(mul(two,e),h),accel);
const start=Q(249,500);
const end=add(add(start,mul(noisy,h)),mul(Q(-1,2),mul(A,mul(h,h))));
assert(eq(flat,Q(1)));
assert(eq(noisy,Q(7,5)));
assert(eq(end,Q(251,500)));
const nonflat=add(div(Q(1,10),h),accel);
assert(eq(nonflat,Q(11)));
// For a_k(t)=1/2+sin(2*pi*k*t/h)/20, all endpoints equal 1/2.
// The derivative maximum is proportional to k, hence unbounded as k grows.
for(const k of [1,10,100,1000]) assert(mul(Q(k),div(Q(1,20),h))[0]>0n);
console.log(JSON.stringify({
  flat_exact_bound_per_s:str(flat),
  noisy_bound_per_s:str(noisy),
  quadratic_start_aperture:str(start),
  quadratic_end_aperture:str(end),
  quadratic_initial_speed_per_s:str(noisy),
  quadratic_attains_noisy_bound:true,
  nonflat_bound_per_s:str(nonflat),
  uncalibrated_decision:'ABSTAIN_UNCALIBRATED',
  checks:'PASS'
}));
