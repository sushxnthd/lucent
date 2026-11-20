# E002-556 FROZEN | Physical shutter partition-calibration acceptance gate

Date: 2026-10-31. Existing E002-371 human-observability kernel; no new theorem. This is an instrument-facing prospective falsification protocol, not human evidence.

## Question and predeclared outcome
Can an independently timed LED/photodiode sequence measure a conservative shutter temporal-variance interval without assuming a uniform boxcar or inferring zero response at unprobed offsets? A *complete partition* of the exposure support is required: N adjacent, non-overlapping illumination windows cover the full physically bounded support. The camera/photodiode transfer must be independently linear and unsaturated. Each bin records camera response above matched dark, photodiode amplitude, absolute response error, and absolute photodiode error. All values must be positive/finite where appropriate. No missing bins, gaps, or overlaps are allowed.

The target output is an interval for the shutter temporal variance, not a point estimate. Conservative intervals must account for all response uncertainty, finite bin widths, and bounded timing error. Clock error enlarges every bin interval. The calibrated interval is only conditional on externally authenticated clock, response linearity, physical exposure support, and pulse stability.

## Holdout test (freeze before acquisition)
Interleave a random set of composite LED waveforms whose on/off patterns are not used to estimate the partition weights. Independently measure their normalized camera responses (camera above-dark divided by the full-on response). Predict an interval using only the partition-bin response bounds. A holdout observation outside the predicted interval after its declared measurement uncertainty is a **calibration falsification**. Do not refit or widen intervals after observing a failed holdout.

Predeclare: at least 8 bins spanning exposure, >=3 repeats per bin, >=4 composite holdouts, >=2 brightness settings, >=2 exposure settings, >=3 sensor rows for rolling shutters, with independently synchronized photodiode and raw linear ROI intensity. These numbers are acquisition design minima, not a proof of power or physiological generalization.

## Release/abstention gates
The executable may return `INSTRUMENT_CONDITIONAL_PASS` only if all partition, uncertainty, and holdout checks pass **and** an external operator supplies authenticated evidence of timing, linearity, gain, optical support, and native sensor rows. Without that evidence the status remains `SYNTHETIC_OR_UNAUTHENTICATED_ONLY`; any holdout failure returns `CALIBRATION_FALSIFIED`. Even conditional instrument pass is **not** an anatomical closure certificate, a human kinematic ceiling, or production release. Product stays `ABSTAIN_UNCALIBRATED` / `BLOCKED`.

## Nuisance / kill conditions
Dark drift, LED pulse leakage, photodiode saturation, autoexposure/ISP, clipping, unknown rolling-row timing, clock drift, lens/ROI changes, motion blur, geometry, gaze, glasses, occlusion, and missing frames require explicit controls or abstention. A partition LED pulse must measure the *integrated response over that entire bin*, not an impulse at its center. No extrapolation beyond the externally measured support. Physical moving-aperture and blinded human tests remain separate gates.

## Evidence ledger
At freeze: physical optical captures 0; independently blinded human rater pairs 0; certified continuous-time physiological speed/acceleration ceilings 0; held-out physical predictions 0. No human/physical validation claimed.
