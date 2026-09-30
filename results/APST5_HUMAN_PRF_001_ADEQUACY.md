# APST5-HUMAN-PRF-001 Secondary Adequacy and Camera-Rate Diagnostics

**Status:** completed secondary diagnostics predeclared after the failed primary. These results do not replace H1/H2.

## Two-transition superposition adequacy

Directional kernels estimated from fit transitions were used, without refitting, to predict complete held-out five-second disc-on plus five-second return-to-background pupil trials.

| subject | validation trials | pooled R2 | median trial R2 | median trial RMSE (mm) | median return offset (s) |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01 | 7 | 0.4416 | -0.2201 | 0.3487 | 5.0020 |
| 02 | 11 | 0.2407 | -0.7932 | 0.2524 | 5.0040 |
| 03 | 7 | 0.3256 | 0.1195 | 0.2556 | 5.0040 |
| 04 | 11 | 0.3039 | 0.1900 | 0.2852 | 5.0040 |
| 05 | 9 | -0.5433 | 0.2675 | 0.3341 | 5.0040 |
| 07 | 12 | 0.3586 | -0.0895 | 0.2848 | 5.0040 |
| 08 | 11 | 0.5851 | 0.3113 | 0.2856 | 5.0040 |
| 09 | 11 | 0.5611 | 0.0140 | 0.2168 | 5.0040 |
| 10 | 10 | 0.3560 | 0.2067 | 0.2684 | 5.0030 |
| 11 | 9 | 0.2185 | -1.3300 | 0.2620 | 5.0040 |
| 12 | 11 | 0.1008 | 0.0879 | 0.2054 | 5.0040 |
| 13 | 11 | 0.3798 | -0.2294 | 0.4408 | 5.0040 |
| 14 | 4 | 0.5915 | 0.5296 | 0.2217 | 5.0040 |
| 15 | 11 | 0.4389 | 0.0704 | 0.3077 | 5.0020 |
| 16 | 12 | -0.7137 | -2.0786 | 0.4145 | 5.0040 |
| 17 | 11 | 0.5552 | 0.4527 | 0.3123 | 5.0040 |
| 18 | 10 | 0.1266 | 0.1578 | 0.2978 | 5.0040 |
| 19 | 11 | 0.3956 | -0.0351 | 0.2783 | 5.0040 |
| 20 | 11 | -0.4114 | 0.4477 | 0.3074 | 5.0040 |
| 21 | 10 | 0.1274 | -0.0491 | 0.2850 | 5.0030 |
| 22 | 12 | -0.4420 | -1.6331 | 0.4402 | 5.0040 |
| 23 | 9 | -1.3131 | -2.1257 | 0.2901 | 5.0020 |

- participants with pooled R2 > 0: **77.3% (17/22)**
- median participant pooled R2: **0.3147**
- median participant median-trial R2: **0.0422**

## Frozen E002 camera-rate sensitivity

No sequence was re-optimized. The already frozen E002 (1,2,8) was sampled from the directional human-calibrated waveform model.

| sampling rate | held-out P10 S | held-out median S | held-out S>1.25 |
| ---: | ---: | ---: | ---: |
| 50 Hz | **1.264** | 1.840 | 90.9% |
| 30 Hz | **1.263** | 1.838 | 90.9% |
| 24 Hz | **1.263** | 1.837 | 90.9% |

## Interpretation

The directional superposition bridge predicts complete held-out two-transition luminance trials above a zero-R2 baseline for most participants. This strengthens, but does not confirm, the secondary human-calibrated E002 waveform result.

Camera-rate sensitivity only tests temporal sampling of the EyeLink-derived model. It does not model RGB pupil segmentation, phone auto-exposure, or state prediction.

## Failures

- 06: missing source file
