# E002-527 | Postlabel transport-calibration selection changes the apparent falsification

Date: 2026-10-29. Primary E002-371 workstream, branch `research/observability-human-boundary`, draft PR #26. Frozen protocol committed first at `9f63eb51c9a4f6e71930daed6ba9b79bb14f3635`.

**Evidence tier:** prospective synthetic adversarial study-integrity experiment, not new human anatomy, physiological measurement, hardware calibration, or independent replication.

## New attack on the previous locked evaluator

E002-526 protects gap identity, prediction, ordinary-camera closure threshold, and evaluator version, but permits each reference to supply its own `transport_scale_upper` and `transport_offset_upper` after review. An operator can change the purported calibration while keeping the old preregistration digest unchanged.

The frozen artificial reference has mean-aperture upper bound 0.19, ordinary threshold 0.20, and offset 0. The two **hypothetical**, not independently calibrated, transport bounds yield:

| Reference scale upper | Transported aperture upper | Conditional E002-520 decision |
| ---: | ---: | --- |
| 1.20 | 0.228 | UNKNOWN, cannot certify threshold crossing |
| 1.00 | 0.190 | FALSIFIED if all independent attestations are genuine |

Changing only this postlabel calibration input can reverse a putative falsification. Inflation in the opposite direction can suppress a genuine contradiction. This is a **selection bias in the study evidence chain**, not a discovery about actual human blink speeds.

## Committed correction

- [Frozen protocol](E002_527_FROZEN.md) specifies the counterexample and acceptance criteria before implementation.
- [Calibration-locked evaluator](e002_527_calibration_lock.py) uses a new domain-separated, nonce-protected digest binding the exact transport scale/offset upper bounds and calibration ID for each predeclared gap. It rejects postlabel bound inflation, shrinkage, identity substitution, changed predictions/timing/thresholds, extra/missing windows and invalid numeric inputs. It delegates to E002-520 only after stripping lock-only fields.
- [Adversarial regression](test_e002_527_calibration_lock.py) contains 18 test methods, including the old-gate reversal under unchanged digest, both postlabel scale changes, offset changes, unqualified nuisance flags, legitimate precommitted 1.0 and 1.2 scales, and all-abstention safeguards.
- [GitHub Actions workflow](../../.github/workflows/e002_527_calibration_lock.yml) runs Python adversarial tests, historical E002-526 regression, and independent Node arithmetic. **Hosted success is not claimed until a completed run is observed.**

The committed calibration ID is an identifier, **not** a certificate of instrument accuracy. A locally computed digest does not prove it was published before labels, nor authenticate optical response, radiometry, geometry, timing, rater independence or continuous-time speed. Calibration must be independently performed and time-attested before labels can be interpreted. The fixed synthetic example is a demonstration of selection vulnerability, not evidence that any real reference was manipulated.

## Claim and stopping consequence

Any prospective human-validation result must predeclare the ordinary-camera closure predicate **and** the independent cross-camera transport envelope. Otherwise Lucent cannot interpret a postlabel reference threshold crossing as a valid falsification, even if the code reports one. A qualifying independent closure witness falsifies a specific EXCLUDE; a non-witness never validates absence.

**No new independent anatomical reviews, authenticated physical shutter/clock captures, certified human velocity ceilings or held-out physical predictions.** Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Stop extending manifest-lock variants until real independent S01 anatomical review and physical optical calibration become available; the current software suite cannot replace those measurements. Hush PR #45 remains separate and unmerged.
