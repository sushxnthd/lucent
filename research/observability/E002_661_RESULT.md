# E002-661 — Robust certificate under phase-gain ambiguity

**Evidence:** exact-rational synthetic instrument falsification, not physical or human validation. Reproduction: `python research/observability/e002_661_kernel_set.py`.

E002-660 shows phase-correlated gain can make distinct shutter kernels observationally equivalent. This experiment propagates the entire finite set of kernels compatible with a four-phase linear unsaturated calibration scan and bounded unknown per-phase gains {1/2, 1, 2}, rather than choosing a point estimate. For a Lipschitz aperture with speed bound V, response weights k_i at relative times t_i, and observed integrated aperture A, the robust center-aperture lower certificate is A - V max_k sum_i k_i |t_i|. The adversarial V-shaped aperture attains equality for the maximizing kernel, so this finite-model bound is sharp.

With phase times (-1.5,-0.5,0.5,1.5), A=0.60, V=0.25, and closure threshold 0.30, a presumed rectangular response yields lower bound 0.35 (false certificate of open). An admissible gain-confounded kernel (0.4,0.1,0.1,0.4) has first moment 1.3, giving robust lower bound 0.275 (must abstain). The constructed aperture reconstructs the identical exposure integral. If an independent constant-gain measurement is available, the compatible set collapses to the rectangular kernel in this toy model.

**Limitations:** Finite discretized shutter model, pointwise phase gains, exact aperture measurements, and no spatial image formation. Real gain bounds must be measured, not assumed; temporal interpolation, rolling shutter, geometry, brightness, blur, gaze, glasses, missingness and clock error need independent uncertainty envelopes. No human or instrument data acquired. This test does not validate E002-371.

**Product rule:** Never use a point-estimated shutter response when the calibration is non-identifiable. Propagate the full compatible response set; abstain whenever its worst-case certificate crosses the closure threshold. Maintain `ABSTAIN_UNCALIBRATED`, production `BLOCKED`.

**Next experiment:** Physical phase-randomized pulse scan with independent photodiode and calibrated clock; freeze gain envelope on a calibration split, predict held-out phase responses and shutter-gap certificates, and report false certifications and abstention rates. Obtain independently annotated high-speed eyelid trajectories for the human-held-out test.
