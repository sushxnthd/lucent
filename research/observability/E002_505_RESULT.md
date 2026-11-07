# E002-505 | Clock-uncertainty reversal of a nominal 30-fps certificate

Date: 2026-10-28. Primary E002-371 research branch and draft PR #26. **Evidence: preregistered synthetic instrument-design calculation; not human or physical camera validation.** Freeze: [E002_505_FROZEN.md](E002_505_FROZEN.md). Reproducer: [e002_505_clock_uncertainty.py](e002_505_clock_uncertainty.py). Hosted [CI run 40667987375](https://github.com/sushxnthd/lucent/actions/runs/40667987375) was **queued at this report's creation**; do not call it a pass before independently checking the completed run.

## Decisive conditional prediction

Apply the already established E002-373 sharp scalar shutter-average bound to a hypothetical 30-fps acquisition with 10-ms exposure, normalized continuous-time speed ceiling V=60/s, endpoint mean b=0.999 with error r=0.001, and closure threshold theta=0.2. None of these quantities has been measured on S01 or independently certified for a camera.

For exposure deficit eta=1-b+r=0.002, the sharp exposure-endpoint deficit is sqrt(2 V w eta)=0.04898979485566. With total blind-gap timing uncertainty j, the conservative blind interval is H=1/30-0.010+j. The scalar hidden-closure risk bound is d_max+V H/2, and strict exclusion requires risk < 0.8.

| Total blind-gap uncertainty j | Risk bound | Conditional scalar classification |
| --- | ---: | --- |
| 0 ms | 0.74898979486 | Excluded, *if all premises hold* |
| 1 ms | 0.77898979486 | Excluded, *if all premises hold* |
| 2 ms | 0.80898979486 | **Not excluded** |
| 2 ms at 60 fps, otherwise identical | 0.30898979486 | Excluded, *if all premises hold* |

The transition occurs at j_crit=1.70034017148 ms of **total** additional blind-gap uncertainty. A nominal 30-fps certificate can reverse solely because independent clock, shutter-edge, trigger or rolling-shutter uncertainty is not tight enough. This is a new quantitative **instrument-selection and calibration requirement** under the pre-existing theorem, not a new physiological observation or a new mathematical law.

## Adversarial interpretation

A 1-ms uncertainty on each of two independently uncertain exposure edges can contribute 2 ms total blind-gap uncertainty. A claimed 1-ms **total** uncertainty is not interchangeable with two separate 1-ms edge uncertainties. If a camera's physical timebase or exposure phase is unknown, do not set j=0 by default. Exposure-duration uncertainty, geometry, brightness, missingness, gaze, glasses and blur must be independently included or cause abstention. The 60-fps calculation is conditional, not proof that a specific phone records at that rate or exposure.

The reproducible Python calculator uses 70-digit decimal arithmetic and a conservative numerical boundary guard, with 12 frozen tests covering the 0/1/2-ms reversal, exact threshold, monotonic timing/mean-error/speed degradation, faster nominal sampling, invalid parameters and unconditional product abstention. Hosted execution remains pending at the report freeze. Do not tune on S01 or present numerical tests as real physical calibration.

## Next evidence and stop

The numerical example identifies an actionable acquisition requirement: to claim this particular hypothetical 30-fps exclusion, independently bound the *total* blind-gap uncertainty below 1.70 ms, while separately certifying V, shutter w, exposure mean b and r, geometry, and nuisance conditions. **The 1.70-ms number is specific to this synthetic parameter set, not a universal device tolerance.**

Two independent blinded anatomical S01 ratings, authenticated physical timebase/shutter, certified between-frame speed envelopes and participant-disjoint high-rate predictions remain missing. No images or individual ratings were published. Stop E002-505 synthetic refinements after hosted verification and return to external human/physical evidence. E002-371 remains physically unvalidated.

**Human anatomical ratings: 0. Authenticated physical camera clock/shutter: 0. Certified human V: 0. Held-out physical predictions: 0. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.** Hush PR #45 unchanged.
