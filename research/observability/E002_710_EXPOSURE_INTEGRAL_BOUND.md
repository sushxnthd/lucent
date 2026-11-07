# E002-710: exposure integration changes the closure-observability boundary

**Evidence tier:** analytic instrument prediction, not physical or human validation. This is a distinct measurement-model test of E002-371/E002-709, not a claim of priority for a standard Lipschitz argument.

## The falsifiable question
A high-speed reference camera need not have a completely blind interval: its finite exposures integrate light. Can a *full closure during an exposure* be excluded by an integrated aperture measurement, even if the frame endpoints are open? The answer depends on the exposure transfer function, aperture-to-intensity calibration, integration window, and measurement error; frame rate alone is insufficient.

## Exact law for ideal linear exposure averaging
Assume a scalar aperture x(t) in [0,A], x(t) is V-Lipschitz, and the pre/post-exposure baseline is exactly A. For a full closure x(t0)=0 strictly inside a single exposure [0,T], the pointwise bound x(t) <= min(A,V|t-t0|) gives an unavoidable deficit
D = integral_0^T [A-x(t)] dt >= F(t0) = integral_0^T max(0,A-V|t-t0|) dt.
The bound is **sharp**, attained by x(t)=min(A,V|t-t0|), provided the stipulated boundary conditions are feasible. If the closure is at least A/V from both exposure boundaries (T >= 2A/V), then F(t0)=A^2/V. Hence the mean aperture must satisfy mean(x) <= A - A^2/(VT). Define dimensionless detectability Q = A/(VT) and normalized measurement uncertainty eta = delta/A. In this fully contained regime a closure can be ruled out by a measured average whose *lower confidence/uncertainty bound* exceeds A-A^2/(VT); equivalently an observed deficit smaller than A^2/(VT) minus a conservative error bound excludes closure. The distinction between deterministic bounded error and statistical confidence intervals must be explicit.

If the closure lies near an exposure boundary, use F(t0) exactly, **not** A^2/V. For any t0 in [0,T], the universal deficit lower bound is min_t0 F(t0), attained at an exposure endpoint: integral_0^T max(0,A-Vt) dt = A*min(T,A/V) - (V/2)*min(T,A/V)^2. But endpoint baseline constraints can rule out some t0; do not substitute this relaxed bound for a sharp boundary-conditioned certificate. If V is unbounded, the minimum deficit tends to zero: E002-709 remains operative.

## Instrument falsification protocol (freeze before acquisition)
1. Independently measure the camera exposure window and timestamp uncertainty with a pulsed LED or photodiode; characterize rolling shutter per ROI row. Calibrate intensity-versus-occluder-aperture using a static step wedge and test for gamma, auto-exposure, clipping, illumination drift, and nonlinear PSF effects. Lock exposure/gain/focus and record raw frames if possible.
2. Use a motorized or controlled physical occluder with independently logged position and velocity; phase-sweep complete occlusions across exposure boundaries, including fully contained, boundary-straddling and inter-exposure events. Randomize phase and blind the reference labels.
3. Before inspecting phase/position logs, publish per-event **EXCLUDE / POSSIBLE / ABSTAIN** from the measured exposure integral and conservative calibration bounds. A prediction is EXCLUDE only when the worst-case closure-compatible integrated signal is strictly below the observed signal's conservative lower bound. No calibrated V, exposure, response, or noise bound => ABSTAIN.
4. Stress geometry, brightness, blur, gaze surrogate, glasses/reflections, dropped frames, ROI displacement, rolling-shutter timing, and clock uncertainty. Count unequivocal false EXCLUDE events; any such event invalidates the operational certificate under the claimed bounds. Preserve negative results and acquisition hashes.
5. Transfer to human eyelids only after an independent physiological V assumption and an independently validated aperture-to-photometric transfer function; otherwise keep the instrument result instrument-only.

## Product consequence
E002-371's gap-only certificate is **not** the only theoretically available evidence: an *independently calibrated integrated exposure* can constrain hidden closures even without a sample exactly at closure time. But ordinary smartphone RGB intensity is not automatically linear in anatomical eyelid aperture, and high-frame-rate reference negatives are not ground truth without timing/transfer calibration. Do not enable closure exclusion in Lucent on this derivation alone. Current state: ABSTAIN_UNCALIBRATED; production BLOCKED.

## Explicit limitations
No recorded video, physical occluder, human subject, external velocity bound, or instrument response measurement was used here. The analytic result assumes a known linear exposure-average model, exact aperture baseline and a stipulated Lipschitz V; calibration errors and uncertain baseline must be propagated before any certificate. Literature priority and external replication remain open.
