# E002-505 | Frozen clock-uncertainty falsifier for the shutter-gap certificate

Frozen 2026-10-28 before executing the numerical instrument experiment. Primary E002-371 kernel, existing branch and draft PR #26. This is a **synthetic instrument-design prediction**, not human data, a novel theorem, or a verified camera timebase. Do not change the frozen E002-492 S01 annotation sample or revive E002-501's rejected optical proxy.

## Prespecified question

Does a plausible uncertainty in the **actual blind interval** reverse a nominal ordinary-camera no-hidden-closure classification even if the endpoint aperture measurements and assumed speed ceiling remain unchanged? Use the already established sharp scalar exposure bound (E002-373), with conservative exposure-mean error.

Assume an independently certified normalized continuous-time speed cap V (1/s), shutter exposure w, frame period T, minimum exposure mean b, exposure-mean absolute error r, closure threshold theta, and *total* additional blind-gap uncertainty j (seconds), including acquisition clock, trigger/exposure-edge, and rolling-shutter uncertainty. Define H=T-w+j, eta=1-b+r, L=1-theta, and
d_max=min(1, sqrt(2 V w eta)) if eta<=Vw/2, otherwise min(1, eta+Vw/2).
The sharp conditional exclusion requires d_max+V H/2 < L. Equality is not an exclusion. This does **not** certify the premise V, calibrated b, shutter, or j. If any are missing or unverified, product abstains.

## Frozen synthetic cases

Common nominal 30-fps camera: T=1/30 s, w=0.010 s, V=60/s, b=0.999, r=0.001, theta=0.20. No human or device measurement is asserted.

- j=0: predict **conditional exclusion**, with d_max≈0.04898979486 and risk≈0.74898979486 < 0.8.
- j=0.001 s: predict conditional exclusion.
- j=0.002 s: predict **not excluded**, risk≈0.80898979486 > 0.8. This is a *falsification of a naive nominal-clock clearance*, not proof that a blink occurred.
- Critical *total blind-gap* uncertainty j_crit≈0.00170034017 s. Two independent endpoint errors of ±1 ms can conservatively yield j=2 ms and flip the claim; do not confuse per-edge and total error.
- With V unspecified or unverified: always `ABSTAIN_UNCALIBRATED`, even if the numerical conditional classification is exclusion.
- Increasing j or r must never improve exclusion; larger V must not improve exclusion. At equality, abstain.
- At 60 fps, w=0.010, same other assumptions and j=0.002: predict conditional exclusion; no claim of device superiority without real shutter/timing measurements.
- An interval containing both sides of the boundary must abstain; no decimal-rounding clearance.

## Implementation and evidence

Create a standard-library, high-precision independent calculator, frozen tests, and a dedicated hosted CI job. Report risk, j_crit, and conditional classification separately from product/release status. A provenance flag supplied by code is not independent certification. Preserve all failed controls, do not tune parameters on S01, and do not make human physiology or camera fps claims.

**Evidence gate:** zero independent human anatomical ratings; zero authenticated camera clock/shutter; zero certified human V; zero participant-disjoint physical tests. E002-371 physical validation absent; product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. After this prespecified instrument calculation, stop synthetic sensitivity refinements and prioritize actual two-rater S01 and physical timing acquisition. Hush untouched.
