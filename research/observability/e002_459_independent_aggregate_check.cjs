#!/usr/bin/env node
// E002-459: independent post-outcome arithmetic/structure verifier.
// Does not re-estimate human landmarks, verify physical speed caps, or replace source-SHA checks.
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const read = p => JSON.parse(fs.readFileSync(p, "utf8"));
const canonical = x => Array.isArray(x) ? x.map(canonical) :
  x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const eq = (a,b) => assert.deepEqual(canonical(a), canonical(b));
const near = (a,b) => assert.ok(Math.abs(a-b) <= 1e-10*Math.max(1,Math.abs(a),Math.abs(b)), `numeric mismatch: ${a} vs ${b}`);
const a = read(process.argv[2] || "research/observability/E002_459_HUMAN_AGGREGATE.json");
assert.equal(a.source_sha256, "6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43");
eq(a.participants, {calibration:12,holdout:5});
eq(a.blinks, {calibration:1657,holdout:649});
assert.equal(a.product_claim,"ABSTAIN_UNCALIBRATED");
assert.equal(a.physical_release_authorized,false);
assert.equal(a.human_anatomical_trajectory_validation,"NOT_ESTABLISHED");
const gs=["bottom","center","top"];
assert.equal(gs.reduce((n,g)=>n+a.training_gaze_counts[g],0),1657);
assert.equal(gs.reduce((n,g)=>n+a.heldout_gaze_transfer[g].heldout_blinks_in_gaze,0),649);
for(const g of gs) {
 const z=a.heldout_gaze_transfer[g];
 assert.equal(z.calibration_blinks_in_gaze,a.training_gaze_counts[g]);
 assert.equal(z.heldout_participants_in_gaze,5);
 for(const k of ["center_only_transfer","pooled_transfer","gaze_matched_transfer"]) {
  assert.equal(z[k].blinks,z.heldout_blinks_in_gaze);
  assert.ok(z[k].exceed_either_blinks>=z[k].exceed_closing_blinks);
  assert.ok(z[k].exceed_either_blinks>=z[k].exceed_opening_blinks);
  assert.ok(z[k].exceed_either_blinks<=z[k].exceed_closing_blinks+z[k].exceed_opening_blinks);
  assert.ok(z[k].exceed_either_participants<=z[k].participants);
 }
 for(const key of ["closing_mm_s","opening_mm_s"]) {
  assert.ok(a.pooled_training_caps[key]>=a.gaze_matched_training_caps[g][key]);
  assert.ok(a.pooled_training_caps[key]>=a.center_only_training_caps[key]);
 }
}
const bottom=a.heldout_gaze_transfer.bottom.center_only_transfer;
const top=a.heldout_gaze_transfer.top.center_only_transfer;
const primary=a.primary_noncenter_center_trained;
for(const k of ["blinks","exceed_closing_blinks","exceed_opening_blinks","exceed_either_blinks"])
 assert.equal(primary[k],bottom[k]+top[k]);
assert.equal(primary.participants,5);
assert.equal(a.center_only_noncenter_falsified_in_sample,primary.exceed_either_blinks>0);
function check(caps, verdict) {
 const t=1000*(1/caps.closing_mm_s+1/caps.opening_mm_s);
 near(verdict.critical_gap_ms_for_hypothetical_1mm_endpoints,t);
 assert.equal(verdict["240fps_conditional_exclusion_ideal_only"],(1000/240)<t);
}
check(a.center_only_training_caps,a.hypothetical_1mm_ideal_camera.center_only);
check(a.pooled_training_caps,a.hypothetical_1mm_ideal_camera.pooled);
for(const g of gs) check(a.gaze_matched_training_caps[g],a.hypothetical_1mm_ideal_camera.gaze_matched[g]);
if(process.argv[3]) eq(a,read(process.argv[3])); // fresh independently rerun Python analysis
console.log("E002-459 independent aggregate arithmetic + optional fresh-CI comparison PASS; physical validation NOT_ESTABLISHED");
