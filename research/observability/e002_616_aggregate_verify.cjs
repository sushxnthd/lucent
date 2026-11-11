#!/usr/bin/env node
"use strict";
/* E002-616 independent aggregate-only arithmetic audit.
 * This checks the persisted published-human-source result, not source-frame
 * selection or independent anatomical annotation.
 */
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const input = path.join(__dirname, "E002_616_AGGREGATE.json");
const raw = JSON.parse(fs.readFileSync(input, "utf8"));
function audit(d) {
  assert.equal(d.experiment, "E002-616");
  assert.equal(d.evidence, "PUBLISHED_HUMAN_BILATERAL_FC_LABEL_VIRTUAL_POINT_SAMPLING");
  assert.equal(d.source_archive_sha256, "a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223");
  assert.equal(d.source_sequences, 5);
  assert.equal(d.per_sequence.length, 5);
  const t = d.totals;
  const sum = a => a.reduce((x,y)=>x+y,0);
  const keys = ["eligible_bilateral_runs","index_any_phase","actual_any_phase",
    "paired_event_phase_changes","jointly_omitted_event_phase_pairs",
    "long_run_omission_event_phase_pairs","interior_phase_law_checked"];
  for (const k of keys) {
    assert.equal(t[k],sum(d.per_sequence.map(s=>s[k])), "sequence sum "+k);
  }
  for (const k of ["1","2","3","4+"]) {
    assert.equal(t.length_histogram[k],sum(d.per_sequence.map(s=>s.length_histogram[k])), "hist "+k);
  }
  assert.equal(sum(Object.values(t.length_histogram)),t.eligible_bilateral_runs);
  for (const key of ["index_omissions_by_phase","actual_omissions_by_phase"]) {
    assert.equal(t[key].length,10);
    for(let p=0;p<10;p++){
      assert.equal(t[key][p],sum(d.per_sequence.map(s=>s[key][p])),key+" phase "+p);
      assert(t[key][p]>=0 && t[key][p]<=t.eligible_bilateral_runs);
    }
  }
  const i=sum(t.index_omissions_by_phase), a=sum(t.actual_omissions_by_phase);
  const both=t.jointly_omitted_event_phase_pairs, changed=t.paired_event_phase_changes;
  assert.equal(i+a-2*both,changed,"paired symmetric difference");
  assert(both<=Math.min(i,a));
  assert.equal(i,7*t.length_histogram["1"]+4*t.length_histogram["2"]+t.length_histogram["3"],"frozen index law");
  assert.equal(t.interior_phase_law_checked,t.eligible_bilateral_runs);
  assert(t.index_any_phase<=t.eligible_bilateral_runs && t.actual_any_phase<=t.eligible_bilateral_runs);
  assert(t.index_any_phase<=i && t.actual_any_phase<=a);
  for(const s of d.per_sequence){
    const n=s.eligible_bilateral_runs;
    assert.equal(sum(Object.values(s.length_histogram)),n);
    assert.equal(sum(s.index_omissions_by_phase),
      7*s.length_histogram["1"]+4*s.length_histogram["2"]+s.length_histogram["3"]);
    assert.equal(sum(s.index_omissions_by_phase)+sum(s.actual_omissions_by_phase)-
      2*s.jointly_omitted_event_phase_pairs,s.paired_event_phase_changes);
    assert(s.index_any_phase<=n && s.actual_any_phase<=n);
    assert(s.long_run_omission_event_phase_pairs>=0);
    for(const key of ["boundary","missing_index","nuisance"]) assert(s.excluded[key]>=0);
  }
  assert.equal(d.physical_shutter_validated,false);
  assert.equal(d.hard_velocity_ceiling_validated,false);
  assert.equal(d.independent_anatomical_raters,0);
  assert.equal(d.product,"ABSTAIN_UNCALIBRATED");
  assert.equal(d.release,"BLOCKED");
  return {eligible:t.eligible_bilateral_runs,omitted_some_phase_index:t.index_any_phase,
    omitted_some_phase_actual:t.actual_any_phase,index_event_phase_omissions:i,
    actual_event_phase_omissions:a,paired_changed:changed,intersection:both};
}
const result=audit(raw);
if(process.argv.includes("--self-test")){
  const tamper=JSON.parse(JSON.stringify(raw));
  tamper.totals.paired_event_phase_changes++;
  assert.throws(()=>audit(tamper));
  const tamper2=JSON.parse(JSON.stringify(raw));
  tamper2.per_sequence[0].length_histogram["4+"]++;
  assert.throws(()=>audit(tamper2));
}
process.stdout.write(JSON.stringify({experiment:"E002-616",independent_aggregate_audit:"PASS",
  self_test:process.argv.includes("--self-test")?"PASS":"NOT_RUN",...result})+"\n");
