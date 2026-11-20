# E002-741 | Exposure-mean aperture recovery: conditional sharp bound

**Evidence:** exact arithmetic synthetic instrument model, locally executed 2026-11-11 UTC; **68/68** feasible endpoint-ramp constructions passed. No human measurements or camera calibration.

Let aperture a(t) be in [0,1] and L-Lipschitz on a shutter exposure interval of width w. If an independently calibrated instrument reports the **true time average** m = (1/w) integral a(t) dt, then at every t in that exposure,

a(t) >= max(0, m - Lw/2).

Proof: choose any t0. By Lipschitz continuity a(s) <= a(t0)+L|s-t0|. Integrating gives m <= a(t0)+(L/w) integral |s-t0| ds <= a(t0)+Lw/2, because the average distance from any t0 in [0,w] is at most w/2. A linear ramp with its minimum at an exposure endpoint attains equality whenever it remains in [0,1]. Thus the constant 1/2 cannot be decreased uniformly.

For two nonoverlapping exposures, with means m0,m1, widths w0,w1 and a known upper bound G on the **physical gap between exposure supports**, define q_i=max(0,m_i-Lw_i/2). If both q_i>0 and q0+q1>L*G, no zero aperture occurs in either exposure or the gap. Equality abstains. This remains conditional on a defensible L and verified physical exposure timing. Clock and row timing errors must enlarge G.

**Critical limitation:** raw RGB brightness is not a calibrated linear aperture average. Multiplicative gain/illumination, geometry, gaze, glasses, blur, occlusion and exposure nonlinearity can destroy the premise. The executable contains a simple exact gain ambiguity witness. No ordinary-phone exclusion claim is authorized without independent observation-model calibration and nuisance bounds.

**Falsification protocol:** acquire a timed programmable aperture/LED optical shutter with independently recorded photodiode timing; measure the true aperture waveform and camera exposure supports. Predeclare L from actuator characterization, calibrate the aperture-to-observation transfer on separate control waveforms, freeze bounds, then test held-out ramps and triangular hidden closures at varying w and G. Repeat with brightness, blur, missingness, rolling-shutter row shifts and geometry perturbations. Any uncovered closure under a purported certificate kills that observation model. Human follow-up remains participant-disjoint, dual-rater annotated, and explicitly uncertain at high-speed reference sampling gaps.

**Product:** ABSTAIN_UNCALIBRATED / BLOCKED. This mathematical possibility does not rescue raw RGB or provide physiological velocity calibration.
