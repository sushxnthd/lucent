# E002-554 FROZEN | Finite LED pulse calibration cannot certify shutter moments (2026-10-31)

Primary E002-371 human-observability kernel. Freeze **before** simulator and numerical results. Evidence target: exact synthetic **calibration identifiability falsification**, not measured camera response or a new mathematical theorem.

## Prediction
Even if two nonnegative, normalized, full-support shutter kernels have the same exposure support, integrated gain and temporal center, a finite set of calibration pulses restricted to the central 60% of the shutter can give exactly identical readings while their variances differ. Substituting the lower-variance candidate for the true higher-variance kernel into E002-553 can falsely exclude a genuine hidden closure.

## Frozen construction
Normalized exposure coordinate x in [0,1]. Define q(x)=+1 on [0,1/10] and [9/10,1], -1 on [1/10,2/10] and [8/10,9/10], and 0 elsewhere. Set K_high=1+q/2 and K_low=1-q/2. Both must be strictly positive everywhere, have unit mass, center 1/2, and support [0,1]. All calibration LED pulses with support contained in [1/5,4/5] must have exactly equal integrated responses under K_high and K_low. The variance difference is predicted to be 2/125 in normalized coordinates (verify exact fractions).

Apply affine shutter mapping x=(t-a)/h with h=1/2 to exposures [-1/2,0] and [1,3/2] around dark gap [0,1]. Use true anatomical aperture f(t)=(t-1/2)^2, hard A=2, closure threshold theta=3/1000. Actual shutters K_high; wrongly calibrated shutters K_low. Predict the invalid lower bound at the gap midpoint is 1/250 (0.004), falsely excluding true closure (minimum zero), while the correct K_high envelope is zero.

## Frozen tests
1. Independently integrate exact rational mass, first moment, variance and flash-response equality.
2. Assert positive full-support kernels, equal center/gain, and predicted variance gap.
3. Verify the wrong-kernel lower bound exceeds theta while the correct bound does not.
4. A pulse overlapping a perturbed edge region must distinguish the kernels; a complete enough pulse scan can therefore resolve this specific ambiguity.
5. Brightness gain, clock jitter, rolling shutter, saturation, ISP gamma, spatial optics, and anatomical transfer remain uncalibrated; no product claim from this synthetic witness.
6. Independently reproduce fractions in a separate Node.js rational oracle, not using Python output.

## Decision and stop
If the construction succeeds, **reject** treating finite center-only flash samples, shutter support, gain or center as a certificate of shutter variance. Physical handoff: independently clocked photodiode, randomized pulse offsets covering the *entire* exposure and each ROI row, repeated amplitude/dark controls, held-out offsets, and uncertainty bounds on unprobed response; absent coverage/smoothness assumptions, abstain. Stop further synthetic kernel tuning and return to physical acquisition and blinded human validation. Preserve `ABSTAIN_UNCALIBRATED` and release `BLOCKED`.
