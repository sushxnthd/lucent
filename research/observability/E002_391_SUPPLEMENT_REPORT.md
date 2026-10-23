# E002-391 supplemental frozen-condition report

Frozen **before** execution in `E002_391_SUPPLEMENT_FROZEN.md` (commit `65fa3d9`); independent seed 39113 and 12,000 fresh trial sets.

| Condition | Predicted | Observed |
|---|---:|---:|
| 60 Hz, one-event phase capture | 60% (exact phase geometry) | 60% theoretical |
| 60 Hz, 12 identical events, locked phase | 60% | 7,192/12,000 = **59.93%** |
| 60 Hz, 12 events, independently randomized phases | 99.9983% | 12,000/12,000 = **100%** |
| 30 Hz, randomized sensor phase but adaptive event timing | 0 captured threshold means | **0/144,000** captured |

The adaptive scheduler positions the triangular event trough exactly halfway between consecutive exposure starts *after observing each phase*. Every event physically reaches aperture zero, yet the smallest exposure mean is **0.56667**, above threshold 0.2. This counterexample demonstrates the necessity of **event-phase independence**; independent random sensor phases alone are not a worst-case guarantee if event timing can adapt or correlate.

The unseen 60-Hz condition passed the previously frozen exact prediction `p=2 theta/(V F)=0.6`. The high 12-event randomized capture rate is **not** a no-hidden-closure certificate for a single blink.

**Evidence limitations:** synthetic instrument; no physiological adaptation mechanism demonstrated; no physical camera, independently calibrated shutter, or human recordings. These sampling facts are not claimed as novel general theory. No deployment claims change beyond limiting phase sweeps to controlled repeatable calibration events and requiring abstention if event-phase independence is unknown.

Reproduce with `python research/observability/e002_391_unseen_adversary.py`. Do not retune seed or thresholds.
