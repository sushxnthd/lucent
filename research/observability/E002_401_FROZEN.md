# E002-401 frozen protocol — rolling-shutter two-landmark time-skew falsification

Frozen before executing E002-401 calculations. Research branch: `research/observability-human-boundary`, PR #25. Evidence target: **synthetic calibrated moving-landmark instrument**, not human validation. Do not change predictions after viewing outputs.

## Question and conditional law

E002-399 certifies scalar **physical aperture exposure means**. Upper/lower eyelid landmarks on a rolling-shutter frame are generally observed at *different row times*. A bound on the speed of their difference (physical aperture) does not bound their individual common-mode motion.

Let upper and lower landmark positions be u(t), l(t), aperture x(t)=l(t)-u(t), and let the row exposure means (equal exposure e) be measured at offsets du and dl relative to the nominal center t. The asynchronous separation m is the lower row mean minus the upper row mean. If |u'|<=U and |l'|<=L independently, then

|m - mean_e[x](t)| <= U*|du| + L*|dl| = B_row.

If only |x'|<=V is known, **no finite B_row follows**, because u and l can translate together arbitrarily quickly with x constant. This is a classical Lipschitz triangle inequality, not claimed as a new theorem. The bound is conditional on calibrated per-landmark temporal row offsets, motion bounds, geometry and optical transfer.

## Locked witness

Two frames centered at -0.001 and +0.001 seconds; exposure e=0.001 s; row offsets du=-0.004 s, dl=+0.004 s; threshold theta=0.2; physical aperture velocity Vx=0. Upper and lower each have common velocity +20/s or -20/s. Positions remain inside [0,1] over all simulated exposures.

- W1: physical x(t)=0.19 throughout and common motion +20/s. Asynchronous row separation m=0.35. A naive scalar E002-399 certificate must return **CONFIRMED_NO_CROSSING**, which is false.
- W2: adding B_row=(20+20)*0.004=0.16 to the measurement interval must change W1 to **UNRESOLVED**.
- W3: physical x(t)=0.30 throughout and common motion -20/s. Asynchronous separation m=0.14. Naive certificate must return **CONFIRMED_CROSSING**, which is false. Row-corrected certificate must be **UNRESOLVED**.
- W4: zero row offsets recover the correct certificates for both cases.

## Held-out synthetic instrument and nuisance

Seed 401; 1,000 independent trials. Half x=0.19 and half x=0.30, independent random common-motion sign, absolute speed uniform [15,20]/s, random acquisition phase within +/-0.0002 s. Exposure-mean rows are computed by independently implemented numerical quadrature over two moving boundaries. Row correction uses fixed, independently specified U=L=20/s, |du|=|dl|=0.004 s; no per-trial true speed is supplied to the certificate.

- W5: corrected certificate produces **zero incorrect decisions** across all 1,000 trials, while naive method produces at least 200 incorrect decisions.
- W6: independent numerical quadrature agrees with analytical row means within 1e-9 in at least 100 separately sampled cases.
- W7: a missing row-skew calibration in the two-rater annotation bridge forces **ABSTAIN_UNCALIBRATED**, even if all earlier Boolean gates are asserted. A separately specified global-shutter zero-offset calibration permits previous synthetic positive controls. Increasing calibrated skew cannot create a previously absent certificate.
- W8: all CI tests of E002-399 and E002-400 continue to pass after updating their synthetic calibration fixtures to explicitly declare verified zero row offset.

## Product consequence

Reject any rolling-shutter physical-aperture certificate derived from a single frame's asynchronous upper/lower landmark positions without independently bounded per-landmark row offsets and motion. A physical aperture velocity bound Vx alone is insufficient. No human ground truth, production deployment or real-camera calibration is claimed. Keep PR draft and `ABSTAIN_UNCALIBRATED` until real independent calibration.

## Nuisance scope

This run isolates rolling-shutter temporal geometry and common-mode motion. Pixel segmentation, gaze, glare, glasses, blur, illumination and clock uncertainty remain separately gated by existing Lucent conditions. It does not assert that actual rolling shutter can be corrected from frame-rate metadata alone. The bound assumes equal row exposure durations and a calibrated row-mean geometry; differing exposure profiles require a different conservative integral bound.
