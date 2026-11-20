#!/usr/bin/env node
"use strict";
/* E002-617: independent exact integer phase oracle + aggregate consistency audit.
 * No raw human rows or images; arithmetic only, not independent source reannotation.
 */
const fs = require("fs");
const assert = require("assert");

function missed(kept, a, b) {
  for (let i=a; i<=b; i++) if (kept.has(i)) return false;
  return true;
}
function floorSelection(first,last,phase) {
  const kept = new Set();
  for(let k=0;;k++){
    const i=first+phase+Math.floor(10*k/3);
    if(i>last)break;
    kept.add(i);
  }
  return kept;
}
function exactPhaseLaw() {
  for (const length of [1,2,3,4,5,8]) {
    for (let start=40;start<50;start++) {
      let missedPhases=0, dilatedPhases=0;
      for(let p=0;p<10;p++){
        const s=floorSelection(0,200,p);
        missedPhases+=Number(missed(s,start,start+length-1));
        dilatedPhases+=Number(missed(s,start-1,start+length));
      }
      assert.strictEqual(missedPhases, ({1:7,2:4,3:1})[length]||0);
      assert.strictEqual(dilatedPhases, length===1?1:0);
    }
  }
}
const KEYS=["baseline_pairs","outward_robust_pairs",
 "outward_robust_distinct_events","inward_surviving_baseline_pairs",
 "two_sided_stable_pairs","two_sided_stable_distinct_events"];
function verify(x){
  assert.strictEqual(x.experiment,"E002-617");
  assert.strictEqual(x.source_archive_sha256,
    "a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223");
  assert.strictEqual(x.source_sequences,5);
  assert.strictEqual(x.per_sequence.length,5);
  assert.strictEqual(x.physical_shutter_validated,false);
  assert.strictEqual(x.velocity_ceiling_validated,false);
  assert.strictEqual(x.independent_anatomical_raters,0);
  assert.strictEqual(x.product,"ABSTAIN_UNCALIBRATED");
  assert.strictEqual(x.release,"BLOCKED");
  const t=x.totals;
  assert.strictEqual(t.eligible_bilateral_runs,279);
  assert.deepStrictEqual(t.length_histogram,{"1":4,"2":14,"3":21,"4+":240});
  assert.strictEqual(t.erased_by_inward_trim,18);
  assert.strictEqual(t.index.baseline_pairs,105);
  assert.strictEqual(t.timestamp.baseline_pairs,105);
  assert.strictEqual(t.index.outward_robust_pairs,4);
  assert.strictEqual(t.index.two_sided_stable_pairs,0);
  for(const r of x.per_sequence){
    assert.strictEqual(Object.values(r.length_histogram).reduce((a,b)=>a+b,0),
      r.eligible_bilateral_runs);
    assert.strictEqual(r.erased_by_inward_trim,
      r.length_histogram["1"]+r.length_histogram["2"]);
    assert.strictEqual(r.index.outward_robust_pairs,r.length_histogram["1"]);
    assert.strictEqual(r.index.two_sided_stable_pairs,0);
    for(const key of ["index","timestamp"]){
      const s=r[key];
      assert.strictEqual(s.outward_robust_by_phase.length,10);
      assert.strictEqual(s.outward_robust_by_phase.reduce((a,b)=>a+b,0),
        s.outward_robust_pairs);
      assert(s.baseline_pairs>=s.outward_robust_pairs);
      assert(s.outward_robust_pairs>=s.two_sided_stable_pairs);
      assert(s.two_sided_stable_pairs>=0);
      assert(s.outward_robust_distinct_events<=s.outward_robust_pairs);
      assert(s.two_sided_stable_distinct_events<=s.two_sided_stable_pairs);
    }
  }
  for(const key of ["index","timestamp"]){
    for(const k of KEYS){
      assert.strictEqual(t[key][k],x.per_sequence.reduce((sum,r)=>sum+r[key][k],0),
        key+"."+k);
    }
    for(let p=0;p<10;p++){
      assert.strictEqual(t[key].outward_robust_by_phase[p],
        x.per_sequence.reduce((sum,r)=>sum+r[key].outward_robust_by_phase[p],0));
    }
  }
  for(const k of ["eligible_bilateral_runs","erased_by_inward_trim",
                  "two_sided_selector_disagreements"]){
    assert.strictEqual(t[k],x.per_sequence.reduce((sum,r)=>sum+r[k],0),k);
  }
  for(const k of ["1","2","3","4+"]){
    assert.strictEqual(t.length_histogram[k],
      x.per_sequence.reduce((sum,r)=>sum+r.length_histogram[k],0));
  }
  return true;
}
exactPhaseLaw();
if(process.argv[2]){
  const x=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
  verify(x);
  for(const mutation of [
    o=>{o.totals.index.outward_robust_pairs+=1;},
    o=>{o.per_sequence[0].index.outward_robust_pairs+=1;},
    o=>{o.totals.length_histogram["1"]+=1;},
    o=>{o.totals.timestamp.two_sided_stable_pairs+=1;}
  ]){
    const bad=JSON.parse(JSON.stringify(x));mutation(bad);
    assert.throws(()=>verify(bad));
  }
  console.log(JSON.stringify({experiment:"E002-617",aggregate_audit:"PASS",
    corruptions_rejected:4,independent_floor_phase_cases:60,
    timestamp_outward_robust_pairs:x.totals.timestamp.outward_robust_pairs,
    timestamp_two_sided_stable_pairs:x.totals.timestamp.two_sided_stable_pairs}));
}else{
  console.log(JSON.stringify({experiment:"E002-617",synthetic_exact_phase_oracle:"PASS",
    independent_floor_phase_cases:60}));
}
