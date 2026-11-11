#!/usr/bin/env node
"use strict";
// E002-458: independently recompute the shutter/clock fragility of the
// hosted E002-457 *illustrative* directional decision. Not a physical claim.
// This is an exploratory consequence of the previously frozen E002-457 model.
const fs = require("node:fs");
const path = require("node:path");
const assert = require("node:assert/strict");
const data = JSON.parse(fs.readFileSync(path.join(__dirname, "E002_457_HUMAN_AGGREGATE.json"), "utf8"));
assert.equal(data.source_sha256, "6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43");
assert.equal(data.physical_release_authorized, false);
assert.equal(data.participants.calibration, 12);
assert.equal(data.participants.holdout, 5);
const { closing_max: C, opening_abs_max: O } = data.calibration_estimated_peaks_mm_s;
assert.ok(C > 0 && O > 0 && C > O);
const gap = 1000 / 240;
function decision(exposureMs, clockErrorMs) {
  if (exposureMs < 0 || clockErrorMs < 0) throw new Error("negative uncertainty");
  // Uniform, centered, physically calibrated shutter is a *hypothesis*.
  const endpointCorrectionMm = (C + O) * exposureMs / 8000;
  const marginMm = 1 - endpointCorrectionMm;
  if (marginMm <= 0) return { exposure_ms: exposureMs, clock_error_per_endpoint_ms: clockErrorMs, decision: "ABSTAIN_ENDPOINT_UNCERTAIN" };
  const criticalMs = 1000 * marginMm * (1 / C + 1 / O);
  const worstGapMs = gap + 2 * clockErrorMs;
  return { exposure_ms: exposureMs, clock_error_per_endpoint_ms: clockErrorMs,
    critical_gap_ms: criticalMs, worst_gap_ms: worstGapMs,
    decision: worstGapMs < criticalMs ? "EXCLUDED_CONDITIONALLY" : "NOT_EXCLUDED" };
}
const nominal = decision(0, 0);
const oneMs = decision(1, 0);
const twoMs = decision(2, 0);
const twoMsClock = decision(2, 0.1);
const twoPointTwo = decision(2.2, 0);
assert.equal(nominal.decision, "EXCLUDED_CONDITIONALLY");
assert.equal(oneMs.decision, "EXCLUDED_CONDITIONALLY");
assert.equal(twoMs.decision, "EXCLUDED_CONDITIONALLY");
assert.equal(twoMsClock.decision, "NOT_EXCLUDED");
assert.equal(twoPointTwo.decision, "NOT_EXCLUDED");
assert.ok(Math.abs(nominal.critical_gap_ms - data.illustrative_1mm_equal_endpoint_margin.directional_critical_gap_ms) < 1e-10);
const criticalExposureMs = (nominal.critical_gap_ms - gap) /
  ((C + O) * (1 / C + 1 / O) / 8);
assert.ok(Math.abs(criticalExposureMs - 2.177243816420385) < 1e-9);
const output = {
  experiment: "E002-458",
  evidence_tier: "EXPLORATORY_SENSITIVITY_USING_PUBLISHED_HUMAN_SAMPLE_MAXIMA",
  input_source_sha256: data.source_sha256,
  physical_release_authorized: false,
  product_claim: "ABSTAIN_UNCALIBRATED",
  nominal_fps: 240,
  break_even_uniform_centered_exposure_ms_at_zero_clock_error: criticalExposureMs,
  scenarios: [nominal, oneMs, twoMs, twoMsClock, twoPointTwo],
  caveat: "No hard human velocity caps, calibrated anatomical endpoints, verified shutter response, or physical clock provenance."
};
process.stdout.write(JSON.stringify(output, null, 2) + "\n");
