# E002-456 — prospective shutter-aware anatomical-reference falsification instrument

**Date:** 2026-10-26. **Evidence tier: preregistered executable research protocol + synthetic/adversarial tests; NO NEW HUMAN ANATOMICAL MEASUREMENTS.** [Protocol](E002_456_FROZEN.md) was committed first at `c432c9d2bf77e0918049148fa241c8dca8f87ef1`. This run directly addresses the missing *prospective human falsification instrument* after E002-455 rejected an optical proxy. It does not claim to have validated E002-371.

## What is now executable

[Prospective physical-reference gate](e002_456_prospective_gate.py) consumes independent reference landmarks, explicit mm-scale geometry and shutter/clock metadata, prespecified velocity-cap provenance, two uncertain shutter-averaged endpoints, and nuisance-clearance flags. It calculates a conservative, shutter-aware lower envelope and only conditionally excludes an unobserved threshold crossing when the envelope is strictly above the threshold. The evaluator always refuses physical release.

[Sealed holdout harness](e002_456_sealed_holdout.py) separates *freeze* from *score*: (1) before opening high-rate reference labels, freeze a private per-interval prediction manifest with SHA256 input hashes and a random-key HMAC-SHA256 public commitment; (2) after independent reference adjudication, verify the frozen inputs and score without releasing case IDs or landmarks. Keep the private key/manifest off GitHub; escrow the public commitment with an independent timestamp before unblinding. The program does not verify escrow itself, and a public hash is not proof of independent preregistration.

The reference logic accepts a positive anatomical threshold witness only if its entire exposure support remains strictly inside the ordinary-camera gap despite both clock uncertainties. No witnessed crossing is **never** treated as proof of no closure. One witnessed crossing in a conditionally excluded interval is a falsification of the *joint* velocity, geometry, timing, measurement, and nuisance assumptions, not a disproof of the mathematical bound.

## Frozen synthetic calculations (NOT human results)

Illustrative endpoints: 3.0 mm at both times, threshold 2.0 mm, nominal 10-ms gap, assumed V=100 mm/s, zero endpoint measurement uncertainty.

| Instrument assumption | Conservative lower envelope | Decision |
|---|---:|---|
| Instantaneous, exact clock | 2.50 mm | EXCLUDED_CONDITIONALLY |
| 2-ms uniform symmetric shutter | 2.45 mm | EXCLUDED_CONDITIONALLY |
| 2-ms support-only symmetric shutter | 2.40 mm | EXCLUDED_CONDITIONALLY |
| 1-ms uncertainty per endpoint clock | 2.40 mm | EXCLUDED_CONDITIONALLY |
| V increased to 200 mm/s, exact clock | 2.00 mm | NOT_EXCLUDED (strict equality) |
| V increased to 300 mm/s, exact clock | 1.50 mm | NOT_EXCLUDED |

A synthetic independent reference with aperture 1.8 mm at t=5 ms would falsify the V=100-mm/s joint assumptions for the first row. It is **not** a real human counterexample. The 100/200/300-mm/s limits are illustrative, not physiological upper bounds. Increasing shutter support or clock uncertainty can only weaken an exclusion. The latest implementation additionally guards the reference exposure and reference clock.

## Verification status

- [Core adversarial suite](test_e002_456_prospective_gate.py): 21 test methods, including nuisance fail-closed, boundary equality, exposure-kernel correction, endpoint inconsistency, absent reference, participant leakage, no release promotion, and reference shutter/clock support.
- [Sealed holdout suite](test_e002_456_sealed_holdout.py): 9 test methods, including input tampering, participant/split mutation, premature reference disclosure, private-key isolation, and post-unblinding synthetic falsification.
- [Hosted CI](../../.github/workflows/e002_456_prospective_gate.yml): the earlier versions at [run 40265000006](https://github.com/sushxnthd/lucent/actions/runs/40265000006) and [run 40265103361](https://github.com/sushxnthd/lucent/actions/runs/40265103361) completed successfully. **The latest version with reference exposure/clock guards has not yet been verified as successful at report-writing time.** Do not imply the latest 30-method suite passed until its own run completes.
- The harness includes **zero** external human reference trajectories, two-rater consensus files, authenticated shutter measurements, physical scale calibrations, or held-out participant predictions. Its self-declared calibration IDs and external-bound provenance are not independently authenticated by the program.

## Operational prospective human protocol

1. Obtain consent and use private storage. For an initial feasibility pilot, acquire >=240-fps eyelid video with per-frame exposure information, and separately capture ordinary-camera frames with a common hardware timing target. Mark virtual frame-index decimation explicitly as **not** physical ordinary-camera shutter validation. Prefer independently calibrated >=400-fps anatomical 3D measurements when authorized.
2. Before human trials, independently measure exposure response, rolling-shutter skew, dropped frames, timebase drift, LED synchronization residual, eye-plane mm scale and its uncertainty. If hardware or calibration is unavailable, mark the relevant nuisance **UNKNOWN** and abstain rather than invent calibration.
3. Use two blinded anatomical raters and E002-450/451 repeat-consistency controls. Preserve missing, blurred, gaze-ambiguous, glasses-occluded, and geometry-unstable frames as unresolved. High-rate video is itself discretely sampled: a witnessed crossing is positive evidence, but absence of a crossing between samples cannot be guaranteed.
4. Freeze threshold, V source and scope, exposure correction, nuisance exclusions and input records on development participants. Run `python research/observability/e002_456_sealed_holdout.py freeze --input private_unlabeled.json --manifest private_manifest.json --output public_commitment.json`. Independently timestamp the public commitment **before** high-rate labels are unsealed.
5. On genuinely participant-disjoint holdouts, collect the independent high-rate reference, then run `python research/observability/e002_456_sealed_holdout.py score --input private_annotated.json --manifest private_manifest.json --output deidentified_aggregate.json`. Review every `FALSIFIED_JOINT_ASSUMPTIONS` case against physical acquisition records, and publish subject-level coverage, abstentions, gaze/behavior strata and cluster-aware uncertainty. One authenticated counterexample kills the corresponding restricted claim.
6. Do not infer a universal deterministic bound from an empirical sample maximum, a sample percentile, or zero holdout exceedances. If only finite-population empirical risk is defensible, the product may eventually report a carefully calibrated *risk under stated conditions*, not a guaranteed no-hidden-closure certificate.

## Scientific decision

This run provides a **prospective, tamper-detecting human-validation handoff**, not new human evidence or a breakthrough. E002-371's physical validation remains **NOT_ESTABLISHED**. The only immediate product behavior supported is an offline conditional research audit with explicit abstention. Real hidden-closure guarantees, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. S21/S22 are not accessed. Keep PR #26 draft/unmerged; Hush PR #45 separate.
