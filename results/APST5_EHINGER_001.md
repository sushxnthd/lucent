# APST5-EHINGER-001: Independent Human Luminance-Response Replication

**Status:** completed preregistered independent controlled-luminance analysis.

**H1 independently optimized timing:** **SUPPORTED**.

**H2 frozen E002 timing:** **SUPPORTED**.

## Dataset

Ehinger et al. (2019) public luminance benchmark, using preprocessed event-locked normalized pupil responses.

- EyeLink usable participants: **13**
- EyeLink design participants: **6**
- EyeLink held-out participants: **7**
- Pupil Labs usable participants: **14**
- fit blocks: 1–3; held-out response-noise blocks: 4–6

## EyeLink equal-exposure result

Design-set P10 search selected **(1, 3, 4)**.

| Probe | positions | design P10 S | held-out P10 S | held-out median S | held-out S>1.25 | design rank |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| independent_selected | (1, 3, 4) | 4.983 | **6.301** | 10.624 | 100.0% | 1 |
| frozen_e002 | (1, 2, 8) | 4.380 | **5.395** | 9.180 | 100.0% | 5 |
| sim005 | (1, 2, 9) | 4.663 | **5.713** | 9.479 | 100.0% | 3 |
| evenly_spaced | (2, 5, 8) | 2.566 | **3.001** | 5.699 | 100.0% | 51 |

## Held-out repeat-response noise

| subject | sigma | median bright RMSE | median dark RMSE | split |
| --- | ---: | ---: | ---: | --- |
| VP1 | 0.1114 | 0.0637 | 0.1541 | design |
| VP11 | 0.1038 | 0.0577 | 0.1117 | design |
| VP12 | 0.1281 | 0.1299 | 0.1264 | design |
| VP14 | 0.0684 | 0.0306 | 0.1121 | held-out |
| VP15 | 0.2001 | 0.1650 | 0.2242 | held-out |
| VP19 | 0.0591 | 0.0432 | 0.0793 | held-out |
| VP20 | 0.0683 | 0.0472 | 0.2228 | design |
| VP22 | 0.0574 | 0.0538 | 0.1320 | held-out |
| VP23 | 0.0999 | 0.0821 | 0.1177 | held-out |
| VP24 | 0.0531 | 0.0347 | 0.2339 | held-out |
| VP26 | 0.0533 | 0.0259 | 0.0880 | design |
| VP3 | 0.0748 | 0.0400 | 0.1530 | design |
| VP4 | 0.0654 | 0.0575 | 0.0733 | held-out |

## Secondary mobile-eye-tracker transfer

The EyeLink-selected timing is transferred to the simultaneously recorded Pupil Labs responses without reoptimization.

| Probe | Pupil Labs P10 S | Pupil Labs median S | Pupil Labs S>1.25 | EL↔PL participant S correlation |
| --- | ---: | ---: | ---: | ---: |
| independent_selected | 6.448 | 10.498 | 100.0% | 0.800 |
| frozen_e002 | 5.615 | 9.544 | 100.0% | 0.859 |

## Exclusions

- EyeLink missing incomplete response sets: ['VP2', 'VP25']
- Pupil Labs missing incomplete response sets: ['VP23']

## Interpretation

Frozen E002 timing satisfies the preregistered held-out EyeLink separation criterion in this independent luminance-response dataset under the fixed asymmetric-kernel construction.

The brightening kernel uses the clean pre-return 0–2.8 s portion of the 0→255 condition. The darkening kernel uses the released block-level average of returns to black. This construction is deliberately fixed but is not a full physical model of the E002 display.

## Claim boundary

A positive result supports human ocular waveform distinguishability under a second controlled eye-tracking protocol. Pupil Labs is a mobile infrared eye tracker, not an ordinary RGB front camera. Nothing here establishes phone RGB observability or fatigue-state validity.
