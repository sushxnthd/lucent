# E002-512 | Frozen rolling-shutter scanline displacement falsification

Frozen 2026-10-29 **before implementation** on the existing `research/observability-human-boundary` branch, draft PR #26. This is a *new synthetic scanline-timing nuisance counterexample*, **not** human or physical camera validation. No more S01 metadata investigation.

## Question and restricted model

E002-373 assumes two equal-duration exposures of the *same* scalar aperture trajectory separated by a known blind gap. For a single tracked rolling-shutter scanline, exposure start in frame j is `t_j + line_delay * row_j`. If the tracked eyelid scanline moves vertically between frames, the effective blind gap is `H = frame_period - exposure + line_delay*(row_2-row_1)`, even if the nominal frame period and exposure are correct. Row indices must be in the sensor's native readout coordinates; unknown cropping, binning, reversed readout, nonlinear line timing, per-row exposure, or a multirow RGB/landmark aggregate **invalidates this simple model**. A scanline gap calculation is not a general full-RGB guarantee.

With independently bounded row localization error `u` on each endpoint and independent nonnegative clock-gap uncertainty `j`, the conservative gap is `H_max = P-w+ell*(row_2-row_1+2u)+j` for known nonnegative `ell`. Require `H_min >= 0` for all admitted row positions; otherwise refuse because exposures may overlap. Use the unchanged E002-373 sharp scalar deficit `d_max` and compare `d_max + V*H_max/2 < 1-theta` (strict). The result is **conditional** on independently certified exposure means/error, timebase, shutter readout, scanline geometry, and hard continuous-time velocity envelope. No numerical case grants product clearance.

## Frozen numerical predictions

Illustrative `P=1/30 s`, `w=10 ms`, `V=60/s`, `b=0.999`, `r=0.001`, `theta=0.2`, `ell=100 microseconds/row`, `j=0`, `u=0`, first row 100. Predict:
- second row 100 (drift 0): conditional exclusion; risk approximately 0.7489898.
- second row 110 (drift +10): conditional exclusion; risk approximately 0.7789898.
- second row 120 (drift +20): NOT excluded; risk approximately 0.8089898.
- second row 80 (drift -20): smaller risk, but no clearance without independently authenticated geometry.
- row 100->110 with `u=5`: NOT excluded (worst-case +20-row displacement).
- unknown readout direction/rate, uncertain or multirow ROI, missing speed or clock calibration: abstain; do not assume global shutter.

The expected crossing is the E002-505 critical total timing error ~1.70034 ms, equivalent to ~17.0034 rows at the illustrative line delay. This is a **new rolling-shutter nuisance mechanism applied to an existing theorem**, not a novel mathematical theorem or measured physiological effect.

## Frozen adversaries and kill rules

Test monotonic risk with positive drift, row-uncertainty and line delay; reversed drift; strict equality abstention; row index out of sensor; row error crossing sensor bounds; missing/nonfinite timing; unknown readout; multirow ROI; overlapping exposures; invalid shutter; positive speed and mean error. Independently reproduce drift 0/10/20 risk with Node.js arithmetic, not imported Python implementation.

If an independently calibrated device violates affine scanline timing, or a real eyelid ROI cannot be reduced to a tracked scanline observing one common aperture trajectory, **kill the scanline certificate rather than fitting a convenient readout**. This experiment only narrows what Lucent may claim; it cannot validate E002-371 or replace independent S01 anatomical ratings, shutter/clock calibration, or held-out physical prediction.

Product remains `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. No human labels, actual camera readout or physical V claimed. Hush untouched.
