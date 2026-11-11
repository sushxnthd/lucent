# E002-750 | Photodiode sampling is not continuous closure ground truth (2026-11-11 UTC)

## New falsification of the E002-744 instrument validation assumption

A photodiode *timestamp stream* is not by itself continuous-time ground truth. Let a(t) be aperture, with 0 <= a <= A and |a'(t)| <= V. A sampled photodiode/encoder with sampling period h, zero aperture error and instantaneous samples at t=0,h can observe a(0)=a(h)=b>0 while a triangular full closure a(h/2)=0 occurs whenever Vh >= 2b. Construction: a(t)=max(0,b-V min(t,h-t)) when Vh=2b, or the piecewise linear V-Lipschitz tent with slopes 2b/h <= V. A shutter that is fully closed for arbitrarily short dwell may also be missed by a thresholded photodiode with finite bandwidth, pulse width, or comparator latency. Thus a high nominal acquisition rate alone cannot certify *absence* of a full closure.

Define dimensionless reference observability ratio Q=2b/(Vh). For ideal point samples Q>1 excludes a hidden zero *conditional on* a certified V and calibrated aperture b; Q<=1 does not. If V is not independently certified, neither a finite photodiode sample rate nor a high-frame-rate camera supplies deterministic absence-of-closure truth. The same limitation applies to an encoder unless it continuously bounds position between logged samples.

## Prospective physical falsifier (not yet executed)

1. Before data collection, calibrate photodiode impulse response, analog bandwidth, comparator thresholds, anti-alias filtering, saturation, timestamp jitter, LED/optical latency and shutter transit using a separate electrical reference. Record scope waveforms, not only transition logs.
2. Randomize shutter phase relative to the acquisition clock, with sub-sample closure durations around 0.25h, 0.5h, h and 2h. Include deliberately adversarial phase offsets, exposure integration, nonuniform temporal kernels, dropped observations and clock skew.
3. Independently command and measure physical aperture with an encoder or oscilloscope channel with a documented uncertainty budget. Do not label absence from a photodiode's lack of threshold crossings. Treat unresolvable closures as UNKNOWN.
4. Freeze predicted reference-detection and ordinary-camera-exclusion outcomes *before* exposing held-out waveforms. Report false reference negatives, uncertain cases, and false ordinary-camera exclusions separately by closure dwell and clock phase.
5. Reject a reference-ground-truth claim if any injected known closure is reported OPEN rather than CLOSED/UNKNOWN, or if optical response/calibration cannot bound missed-pulse width. A reference channel may support positive closure witnesses without supporting negative closure labels.

## Consequence for the frozen E002-744 protocol

The proposed independent photodiode/encoder channel must be validated as a detector with quantified missed-event limits, not called continuous truth merely because its clock is independent. Until the detector's temporal transfer function and event-dwell sensitivity are bounded, use positive instrument closures as falsifiers and abstain from negative instrument closure labels. This strengthens the product release block and prevents artificially optimistic specificity/coverage claims.

Evidence tier: T0 analytical counterexample / instrument protocol amendment, **not** measured physical or human validation. No velocity ceiling is established; no device, photodiode, encoder, or oscilloscope was operated. Product ABSTAIN_UNCALIBRATED; release BLOCKED.
