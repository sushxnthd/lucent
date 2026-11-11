# E002-613 RESULT | One-sided human velocity-ceiling kill-test instrument

Date: 2026-11-02. Primary kernel: E002-371. Branch `research/observability-human-boundary`, draft PR #26. **Evidence: executable exact-rational prospective falsification instrument and synthetic controls only; zero newly acquired human data.**

## What was actually established
A proposed hard continuous-time aperture-speed ceiling can be **falsified** from two independently calibrated anatomical aperture observations without any assumed acceleration bound. Let measured aperture difference be `|z1-z0|`, bounded observation errors `e0,e1`, and conservative upper true elapsed time `dt_max`. Then

`L = max(0, |z1-z0| - e0 - e1) / dt_max`

is a **lower bound** on the largest true absolute aperture speed on the observed span, assuming differentiability, correct physical units and trustworthy error/timing brackets. If `L>V_claim`, the proposed ceiling is incompatible with these physical premises. This follows from the mean value theorem and is **not a new theorem or human measurement**. If `L<=V_claim`, there is no positive evidence for a continuous-time upper ceiling; the program must never promote non-rejection to certification.

### Frozen synthetic outcomes
| Input perturbation | Exact lower bound | Claimed 150 mm/s contradicted? |
|---|---:|---|
| 8.0 -> 7.5 mm, errors 0.05 mm each, elapsed upper 2.5 ms | 160 mm/s | Yes, conditional |
| Same, claimed ceiling 160 mm/s | 160 mm/s | No (strict boundary) |
| Same, elapsed upper widened to 3 ms | 400/3 mm/s | No |
| Same, errors widened to 0.25 mm each | 0 mm/s | No |

These are deliberately hypothetical measurements, **not physiological estimates**. Widening measurement uncertainty cannot create a rejection. The result is a falsification test only, not a calibrated speed estimator or product measurement.

## Implemented and independently tested
- `e002_613_cap_falsifier.py`: exact `fractions.Fraction` rational arithmetic, strict finite nonnegative decimal input, conservative elapsed-time upper bound, anatomical/timing evidence digests, eleven nuisance gates, fail-closed unit/schema checks, and research-only product abstention. Caller-supplied digests/attestations do not authenticate physical evidence.
- `test_e002_613_cap_falsifier.py`: **13/13 local Python unittest methods passed**, including all eleven nuisance flags, absent attestations, malformed numbers, time and uncertainty widening, equality, units and output abstention.
- `e002_613_independent.cjs`: independent BigInt fixed-unit arithmetic, **8 synthetic checks passed locally**. Independent fixed-unit implementation is intentionally limited to micrometre/microsecond representable inputs, unlike the arbitrary-precision Python implementation.
- `.github/workflows/e002-613.yml`: hosted verification committed; **queued** at report creation, not claimed passed. No human data are uploaded to CI.

## Prior-art and source correction
**This is an operationalization, not new scientific novelty.** E002-550 already identified the same restricted FaceBase 400-fps eyelid-margin dataset, and E002-562 already built a synthetic high-rate/ordinary-rate sealed prediction replay. E002-550 explicitly recognized observed secant speeds as *lower-bound evidence only*. E002-613 makes the one-sided rejection inequality, conservative uncertainty handling and product abstention independently executable; it does **not** establish a new source, a new observability theorem, a new speed law or independent human validation.

The specific prospective source remains [FaceBase 88-28BJ](https://doi.org/10.25550/88-28BJ), announced 2026-09-01: eight adults, 400-fps 3D eyelid-margin motion capture with hardware-synchronized EMG, five eyelid behaviors, restricted access (General Research Use / Not-for-profit Use Only). Associated [Kim et al., PNAS 2025](https://doi.org/10.1073/pnas.2508058122). **No access has been granted or attempted through circumvention.** Raw original trajectories, verified marker registration, anatomical aperture scale and timing/error certificates remain unavailable. Public supplementary movies are edited visualizations and cannot authenticate original 400-fps raw trajectories.

## Prospective decisive test and release decision
Obtain authorized FaceBase original motion tracks and original sensor metadata, or carry out the existing synchronized physical-camera + blinded human protocol. Freeze candidate ceiling(s), population/behavior scope, participant-disjoint holdout and uncertainty estimates **before** looking at held-out trajectories. For each independently calibrated upper/lower lid marker pair, compute local palpebral aperture and conservative L. A verified held-out `L>V_claim` **kills** that candidate ceiling for its claimed scope; failure to exceed it cannot approve the ceiling. Report per-participant/behavior contradiction and abstention counts. The FaceBase trajectories cannot replace E002-609's real 30-fps shutter/clock calibration or prove whole-eye closure from one local marker.

**Evidence counters:** original new human tracks 0; independently blinded anatomical rater pairs 0; physical shutter/clock measurements 0; defensible hard human continuous-time velocity ceilings 0; participant-disjoint physical E002-371 predictions 0. Lucent `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush branch and draft PR #45 unchanged. No merge or force push.

**Stop condition for synthetic work:** E002-613 completes the one-sided rejection instrument; do not iterate more arithmetic examples next run. The next material advance must be authorized human data, independent anatomical ratings, or actual physical timing.
