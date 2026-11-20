# E002-716 — Blinded replay executable and falsification gate

**Evidence tier:** implemented replay infrastructure and local synthetic self-tests, not human or physical validation.

The independently executable Python gate `research/observability/e002_716_blinded_replay.py` takes a CSV with trial ID, participant ID, split (calibration/heldout), conservative aperture endpoint lower bounds, independently justified velocity upper bound, maximum elapsed-time upper bound, reference closure label, reference-validity flag, and nine binary validity flags: geometry, photometry, clock, exposure, missingness, blur, gaze, glasses, and independent velocity provenance.

For each valid trial the prospective rule is `V_upper * delta_upper < aperture0_lower + aperture1_lower`. Any missing nuisance guarantee requires ABSTAIN. A held-out reference-confirmed closure under an EXCLUDE certificate is a direct falsification; uncertain reference labels are not scored. Participant IDs appearing in both calibration and held-out splits are rejected, as are nonfinite bounds and invalid binary flags.

Local self-tests exercised falsification, equality-boundary abstention, clock-invalid abstention, reference-indeterminate exclusion from scoring, participant leakage rejection, and NaN rejection. **All six checks passed locally.** These are software fixtures, not real acquisitions.

## Experimental decision

Use the frozen E002-714 protocol. Acquire independent sensor timestamps, calibrated aperture bounds, a velocity bound justified independently of sampled video, and reference-validity adjudication before unblinding. Pre-register trial exclusions and nuisance validity. Report false exclusions with trial IDs, coverage and abstention by nuisance stratum. Zero false exclusions in synthetic fixtures is not a human accuracy claim. Until a trustworthy velocity ceiling and physical calibration exist, the product remains `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.
