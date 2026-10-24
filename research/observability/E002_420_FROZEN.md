# E002-420 frozen protocol — exposure-integrated reference-camera ambiguity

Date: 2026-10-24. Frozen before code and outcome computation. Kernel: E002-371 human observability. Evidence tier: analytical plus independently numerically checked **synthetic shutter experiment**, not a human or physical-camera measurement.

## Question and preregistered falsification

Can a perfectly calibrated boxcar-exposure reference camera, with known acquisition times, known exposure E, zero clock error, zero geometry/photometric noise and a known hard aperture speed cap V, distinguish an always-open eyelid from a hidden closure when two exposure-integrated frames appear open?

Define normalized aperture x(t) in [0,1], closure threshold theta, speed |dx/dt| <= V. Camera records exact exposure averages y_0=(1/E) integral[-E/2,E/2] x(t)dt and y_1=(1/E) integral[d-E/2,d+E/2] x(t)dt, where 0<E<=d. The two worlds are:

- A: x_A(t)=a-V E/8 for all t.
- B: x_B(t)=a outside [0,d], and a-V min(t,d-t) for t in [0,d].

Predict exactly y_0(A)=y_1(A)=y_0(B)=y_1(B)=a-V E/8. World A never crosses theta when a-V E/8>theta; world B crosses theta when a-V d/2<=theta. Both worlds obey the same assumed speed cap and have identical camera averages. The witness is admissible only when 0<=a-Vd/2 and a<=1. An endpoint-based instantaneous-image analysis is invalid on exposure averages unless an additional sound exposure model is used.

**Frozen example:** a=0.30, V=60/s (hypothetical, not measured in humans), d=1/240 s, E=0.002 s, theta=0.20. Predict camera averages 0.285 in both worlds, constant-world minimum 0.285, closure-world minimum 0.175. No nuisance needed.

## Independent verification, before seeing results

1. Compute exact predictions without importing the candidate implementation.
2. Numerically integrate both exposure windows using a midpoint quadrature with >=10,000 bins per window; error <= 1e-7 on the frozen witness.
3. For 1,000 deterministic pseudorandom admissible witnesses with 0<E<=d and theta strictly between the two minima, assert equality of the two-world integrated observations within 1e-6, closure versus no-closure separation, [0,1] physical range and Lipschitz continuity.
4. Include negative controls: E>d, impossible aperture minimum, theta outside the ambiguous interval and missing shutter provenance must not produce a conditional ambiguity certificate.
5. Product output must remain ABSTAIN_UNCALIBRATED, with zero authorized no-closure certificates, regardless of analytic success.

## Physical follow-up (not executed by this software)

Use a calibrated high-refresh programmable occlusion target, independently timed LED/photodiode reference, and two actual cameras at multiple exposure settings. Blind the prediction phase and withhold one camera. Verify camera row timing and transfer response before comparison. A display's advertised refresh rate is **not** adequate timing provenance. If physical shutter or reference truth cannot be authenticated, record unresolved outcomes rather than claiming validation.

## Interpretation

The intended result is a **constructive identifiability counterexample** and an instrument-calibration challenge, not a new general theorem, empirical human-velocity cap, missed-blink frequency or proof of camera behavior. Do not relabel E002-407 human frames using synthetic truth. Preserve E002-417's rejected automatic proxies and E002-419's unresolved-reference accounting.
