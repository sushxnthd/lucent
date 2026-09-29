# APST5-SIM-005: Camera-Robust Equal-Exposure Observability

**Status:** completed preregistered surrogate/camera observability analysis.

**Selected robust sequence:** (1, 2, 9)

**Selected sequence meets frozen model-robust criterion:** **YES**.

**Current E002 (1,2,8) meets frozen model-robust criterion:** **YES**.

## Held-out 500-person result

| Probe | high segments | mean S | P10 S | median S | P90 S | S>1.25 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| robust_selected | (1, 2, 9) | 31.242 | **11.590** | 26.291 | 59.777 | 100.0% |
| current_e002 | (1, 2, 8) | 30.459 | **11.272** | 25.822 | 58.040 | 100.0% |
| evenly_spaced | (2, 5, 8) | 18.383 | **6.791** | 15.486 | 34.880 | 100.0% |

## Camera-scenario stress test

| Probe | camera | P10 S | median S | S>1.25 |
| --- | --- | ---: | ---: | ---: |
| robust_selected (1, 2, 9) | high_quality | 36.960 | 52.683 | 100.0% |
| robust_selected (1, 2, 9) | ordinary | 19.051 | 26.172 | 100.0% |
| robust_selected (1, 2, 9) | stressed | 9.242 | 13.320 | 100.0% |
| current_e002 (1, 2, 8) | high_quality | 37.893 | 51.640 | 100.0% |
| current_e002 (1, 2, 8) | ordinary | 18.672 | 25.757 | 100.0% |
| current_e002 (1, 2, 8) | stressed | 9.062 | 12.740 | 100.0% |
| evenly_spaced (2, 5, 8) | high_quality | 21.924 | 31.136 | 100.0% |
| evenly_spaced (2, 5, 8) | ordinary | 10.755 | 15.500 | 100.0% |
| evenly_spaced (2, 5, 8) | stressed | 5.386 | 7.594 | 100.0% |

## Interpretation

Under the committed pupil surrogate and frozen phone-camera stress model, the current E002 split sequence remains distinguishable from the matched-exposure contiguous control in at least 90% of held-out person x camera cells, with a 10th-percentile separation ratio above the E002 threshold.

The minimax/P10 design search selected (1, 2, 9) rather than the frozen E002 sequence (1, 2, 8). Per preregistration, this does not modify E002-v1; it is a candidate for a future protocol version.

## Claim boundary

This is a model/camera observability result. The assumed fractional pupil noise, pupil dynamics, frame drops, and timing jitter are surrogates. Only real synchronized captures can clear E002.

## Reproduction

    python experiments/camera_robust_probe.py
