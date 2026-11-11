# E002-639 | Sampled velocity is not a certified continuous-time ceiling (2026-11-03 UTC)

## Falsification target
The E002-371 exclusion theorem assumes a *continuous-time* bound on eyelid closing/opening speed. A maximum finite difference computed from a sampled high-speed video does **not** certify that bound, even when its acquisition frame rate is known. This note gives a constructive counterexample, rather than another proof of the shutter-gap theorem.

## Explicit smooth witness
Let the reference camera sample at times `t_k = k Δ`. For any positive aperture `A`, define on one interval
`a(t) = A cos²(π(t-kΔ)/Δ)`, for `kΔ ≤ t ≤ (k+1)Δ`, with constant aperture `A` outside the interval. At both sampled endpoints `a=A`, so the measured secant speed is **zero**. At the midpoint, `a=0`: a complete hidden closure. The trajectory is continuously differentiable when extended by constants, and its maximum absolute derivative is `π A / Δ`, not zero. For `A=2 mm` and `Δ=10 ms`, the true peak speed is approximately **628.319 mm/s**, despite a zero measured interframe velocity. The witness is a mathematical adversary, not a claim about actual human eyelids.

The same failure persists under arbitrary finite sampling: an excursion may be inserted between two consecutive samples with zero sampled displacement. Sampling at 1000 fps reduces the width of the unobserved interval but does not, by itself, establish a physiological speed ceiling.

## Falsifiable consequence
**Reject** any Lucent `EXCLUDE` verdict whose `v_close_mm_s` or `v_open_mm_s` was obtained solely as the maximum frame-to-frame eyelid displacement divided by frame interval. Such a number is a *lower bound* on the unknown peak velocity, whereas the theorem needs an *upper bound*. Adding frame-rate metadata or timestamp uncertainty does not reverse the inequality.

A valid upper envelope needs additional independently justified assumptions or measurements: e.g. a calibrated mechanical encoder with a certified intersample acceleration bound; or a prospective physiological envelope established across subjects and nuisance conditions with explicitly limited population coverage. Even a finite empirical maximum cannot certify a deterministic population-wide ceiling without a justified extrapolation model. All other cases must remain `ABSTAIN_UNCALIBRATED`.

## Instrument test
Acquire simultaneous high-speed reference and encoder/photodiode traces of a motorized occluder. Randomize phase relative to the reference clock, then compare (i) finite-difference peak speed, (ii) independently bounded peak speed from encoder plus acceleration uncertainty, and (iii) truth of closure. Freeze the threshold and clock uncertainty before viewing blinded labels. A reference-confirmed closure that a finite-difference-only certificate excludes is the primary failure. Preserve non-exclusions and calibration failures.

## Evidence tier
Constructive analytical counterexample; no physical acquisition, human blink data, measured acceleration envelope, or population-valid velocity bound. Existing E002-631 blinded protocol remains the governing physical study. This note must not be described as human validation. Production remains blocked.
