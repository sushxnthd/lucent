// E002-551 independent integer-rational witness oracle, no Python imports.
// Scale apertures by 40000 to verify exact equal-endpoint sharp bounds.
const a = 10000n;          // 0.25
const threshold = 8000n;   // 0.20
function drop(A, denom) {  // A*(1/denom)^2/8 in 1/40000 units
  return BigInt(A) * 40000n / (8n * BigInt(denom) * BigInt(denom));
}
const short = a - drop(8000,200);
const long = a - drop(8000,100);
const misspecified = a - drop(1000,100);
if (short !== 9000n || long !== 6000n || misspecified !== 9500n) {
  throw new Error('exact rational envelope mismatch');
}
if (!(short > threshold && long <= threshold && misspecified > threshold)) {
  throw new Error('exclusion or misspecification decision mismatch');
}
console.log(JSON.stringify({evidence:'SYNTHETIC_ONLY',
  short_lower_numerator_40000:String(short),
  long_lower_numerator_40000:String(long),
  misspecified_lower_numerator_40000:String(misspecified),
  true_closure_at_long:true,
  misspecification_false_exclusion:true}));
