# E002-745 | Held-out synthetic shutter-gap validation substitute (2026-11-11 UTC)

**Evidence tier T1 only.** Executed the standalone standard-library Python generator locally with seed 745 and 10,000 trials each in calibration program A and distribution-shifted held-out program B. The synthetic motion model is a nonnegative triangular aperture a(t)=floor+v|t-center| with v sampled in [0.5,1] and a known hard model velocity bound V=1. The ground truth hidden closure is floor=0. The conservative rule uses measured aperture lower bounds reduced by the imposed 0.003 absolute error budget, and a physical gap upper bound increased by 0.002. The naive comparator substitutes a nominal 1/30-second interval and unjustified V=0.35.

| Arm | Hidden closures | Conservative exclusions | Conservative false exclusions | Naive false exclusions |
|---|---:|---:|---:|---:|
| A (10,000) | 5,088 | 3,019 | 0 | 4,791 |
| B held-out (10,000) | 4,993 | 2,289 | 0 | 4,993 |

The zero conservative false-exclusion count follows from hard generator assumptions; it is **not** a measured physiological result, a statistical safety guarantee, or independent physical verification. This exercise tests a shifted shutter-gap/motion distribution, but **does not** model realistic optics, exposure integration, rolling shutter, blink geometry, gaze, glasses, or sensor failure. The naive rule is deliberately misspecified and its failure rates are not human-risk estimates. Reproduce: `python research/observability/e002_745_holdout.py`. CSV optional via `--csv /tmp/e002_745.csv`. The test's fixed seed and exact source should be retained before any future empirical test.

**Product decision:** no expansion of allowable closure exclusion. Keep `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. The next information-bearing experiment must obtain independently timed physical shutter/photodiode acquisition under the frozen E002-744 protocol, or blinded participant-disjoint human sequences. Do not count further synthetic enumeration as human validation.
