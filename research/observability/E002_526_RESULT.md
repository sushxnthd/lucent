# E002-526 | Qualitative witness and post-hoc closure-threshold reversal

Date: 2026-10-29. Primary E002-371 branch, existing draft PR #26. [Protocol frozen first](E002_526_FROZEN.md) at commit `e1b853c0efb4574f087d07921210a84d893091fc`. **Evidence tier:** synthetic adversarial study-integrity and executable quantitative intake. No real human validation or calibrated hardware.

## New inference failure

The E002-525 prospective lock commits to eligible windows, participant/session attribution, predictions and gap timing, but still calls the categorical E002-519 evaluator. E002-519's CLOSED_WITNESS label is not, by itself, evidence that the *ordinary-camera closure predicate* was crossed. The quantitative E002-520 evaluator already corrects this with an independently justified aperture transport bound, but E002-525 does not enforce it. Moreover, E002-525 does not commit to the ordinary-camera closure threshold. That leaves a second post-hoc degree of freedom even if E002-520 is used later.

Artificial, prespecified counterexample, not a human capture:

| Scenario | Threshold | Reference upper mean | Transport scale | Transported upper | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Legacy categorical E002-519 | not specified | 0.19 | 1.2 | 0.228 | FALSIFIED by label alone |
| Quantitative E002-520, original predicate | 0.20 | 0.19 | 1.2 | 0.228 | UNKNOWN |
| Quantitative E002-520, threshold changed *after* reference | 0.23 | 0.19 | 1.2 | 0.228 | Conditionally FALSIFIED |

All reference flags are **asserted true in the synthetic fixture only**; none are externally authenticated. The original 0.20-threshold case is the decisive test: 0.228 > 0.20, so the qualitative category must not count as a transported closure witness. Raising the threshold to 0.23 reverses the conditional result while leaving the reference observation unchanged. The E002-526 gate must reject that post-hoc change.

## Correction

The new [E002-526 lock](e002_526_locked_transport.py) introduces a **separate, versioned** private manifest, without changing historical E002-525 files. It commits to all eligible gaps and abstentions, participant/session IDs, timing, EXCLUDE/ABSTAIN predictions, **ordinary-camera closure thresholds**, and evaluator identity `E002-520-v1`. A domain-separated nonce-protected SHA-256 digest is intended to be published in an independently verifiable pre-label commit. After reference review, it rejects altered thresholds, denominators, predictions, timing, attribution, evaluator version and duplicate IDs, then delegates to the existing quantitative E002-520 evaluator. No categorical-only E002-519 witness is accepted through this new gate.

The evaluator still relies on owner-provided reference data and calibration flags; the code does not authenticate optical timing, geometry, linear photometry, reference shutter response, two independent raters, or the truth of a continuous-time human speed ceiling. An independently timestamped commitment is necessary but not sufficient. The actual S01 preregistration has **not** been published.

## Verification plan and status

[Twenty adversarial unittest cases](test_e002_526_locked_transport.py) were committed, including the prepatch categorical falsification, original-predicate UNKNOWN, threshold-switch attack, legitimate precommitted threshold change, missing transport, false clock/geometry/rater flags, OPEN_OBSERVED censoring, missing references, altered denominator, altered predictions/attribution/timing, digest and schema attacks. A dedicated [GitHub Actions workflow](../../.github/workflows/e002_526_locked_transport.yml) runs the Python suite and an independent Node arithmetic cross-check. **Do not count tests as passed until hosted results are available.**

The numeric reversal is elementary: `1.2 * 0.19 = 0.228`, strictly above 0.20 and below 0.23. It is not a new mathematical theorem or physiological discovery.

## Product and next physical experiment

No prospective human false-exclusion claim is admissible if the closure predicate or reference-adjudication rule can be selected after viewing the labels. For a physical S01 trial: commit the full E002-526 private-manifest digest before reference review; use independently calibrated optical shutter/clock provenance, independently bounded cross-camera transport and two blinded anatomical raters; retain UNKNOWN and reference censoring; preregister what a failure would mean. Do not promote the synthetic conditional witness to an empirical result.

**New independent anatomical ratings: 0. Authenticated physical shutter measurements: 0. Certified continuous-time human velocity ceilings: 0. Held-out physical predictions: 0.** Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. No merge or deployment. Hush PR #45 remains unchanged.
