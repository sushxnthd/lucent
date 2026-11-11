# E002-752 | Integrating-reference threshold falsifier (2026-11-11 UTC)

## Frozen synthetic experiment
Extend E002-751's ideal point-sampled reference detector to a rectangular integration window of width e relative to sample spacing h=1, with an event flag only when the closed-aperture occupancy fraction is at least theta. A zero-aperture pulse of duration d begins at phase i/10000, i=0,...,9999. Use exact rational interval intersections, integer sample windows k=-1,...,3, and sweep d/h={1/4,1/2,3/4,1}, e/h={1/4,1/2,1}, theta={1/4,1/2,3/4}. Executable: e002_752_integrating_reference.py. This is not photodiode or human data.

## Locally executed results
All 36 combinations ran using Python standard library; bounds assertions and the impossible-detection condition d < theta*e passed. Representative detections per 10,000 phases:

| d/h | e/h | theta | detections |
|---|---|---|---:|
| 1/4 | 1/4 | 1/2 | 2501 |
| 1/4 | 1/2 | 1/2 | 2501 |
| 1/2 | 1/2 | 1/2 | 5001 |
| 1/4 | 1 | 3/4 | 0 |
| 1/2 | 1 | 3/4 | 0 |

The point-sampled ideal detector in E002-751 detects 2501/10000 quarter-period pulses, but the integrating reference detector with full-period exposure and 75% occupancy threshold detects **none**, irrespective of phase. More generally, if d < theta*e, no integrated observation can reach threshold even with perfect optics and clock. The exact equality cases and the extra endpoint-aligned detection reflect the finite rational phase grid, not a measured probability.

## Interpretation / product consequence
A high sampling rate is insufficient to establish reference-negative labels. Exposure duration and detection threshold jointly determine event observability. The dimensionless duration-to-required-occupancy ratio R=d/(theta*e) is a necessary (not sufficient) condition for detection: R<1 implies universal non-detection under this model. A negative reference flag cannot establish absence of complete closure unless analog integration, detection threshold, timing, and minimum dwell are independently calibrated. Reference-positive events can still falsify an exclusion claim when verified.

Limitations: rectangular linear integration, noiseless idealized aperture-to-signal mapping, no bandwidth, no physical captures, no human velocity bounds. Evidence T1 synthetic. Product ABSTAIN_UNCALIBRATED; release BLOCKED. Next experiment: pulse-width and phase sweep using a physical shutter/LED plus independently timed photodiode, varying analog bandwidth and threshold, then human participant-disjoint testing.
