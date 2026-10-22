# E002-374: nonlinear moment rescue and photometric-gauge counterexample (2026-10-23)

**Evidence: exact synthetic instrument, not human or ordinary-RGB validation.**

The E002-373 aperture trajectory and constant comparator have identical first exposure moments m=191/192. An idealized three-channel instrument measures exposure means of a, a², a³ with common gain g and offset b. The variable history has moments (191/192, 15203/15360, 564811/573440); the constant history has (m,m²,m³).

**Positive rescue:** A calibrated nonlinear second channel separates the two histories by 31/184320 intensity units. Therefore E002-373's scalar collision is NOT a complete-RGB impossibility theorem.

**Exact photometric collision:** In the first two channels, variable-history (g,b)=(1,0) and constant-history (g,b)=(924/955,31/960) give identical measurements. Unknown common gain/offset destroys the 2-channel rescue.

**Sharp 3-channel minimax boundary:** The distance from the variable vector v to the affine orbit g*c+b*1 of the constant vector c in infinity norm is exactly d=3313/82360320 ≈ 4.022568149e-5. Dual certificate w=(c2-c3,c3-c1,c1-c2) satisfies w·c=w·1=0; ||v-gc-b1||∞≥|w·v|/||w||1=d. Equality occurs at g=2437488/2560355, b=3419/71680 with residual (+d,-d,+d). Both are physically admissible positive gain and small offset. With variable-history gain fixed at 1, bounded independent error ε on each hypothesis permits guaranteed discrimination iff 2ε<d. If BOTH gains are unbounded toward zero, no uniform separation exists.

**Quantization:** Exact round-half-up synthetic channel codes for variable vs photometrically adjusted constant histories coincide at 8, 10 and 12 bits; this particular witness differs at 16 bits. This is not a universal bit-depth threshold, and these nonlinear channels are NOT an actual RGB forward model.

**Falsification:** The standard-library checker integrates both exposures with independent exact polynomial convolution and rational interpolatory quadrature, verifies the dual lower bound and its achieving witness, and checks quantized codes.

**Nuisance gate:** Brightness-only nuisance already invalidates uncalibrated nonlinear rescue. Geometry, gaze, glasses, missingness, blur, rolling shutter and synchronization remain untested in real RGB; no human calibration can be inferred from this instrument.

**Product:** Reject unconditional pupil waveform, exact PERCLOS, five-second fatigue diagnosis, and RGB event identifiability. Retain only E002-373 conditional aperture/shutter certificates when exposure, velocity envelope, timebase and per-device photometric error are independently calibrated; otherwise abstain. The frozen participant/device holdout protocol from E002-373 remains the next decisive test.

**Priority:** The mathematics follows classical moment, Chebyshev approximation, inverse-problem gauge and shutter integration principles. Raskar et al., SIGGRAPH 2006 (https://cameraculture.media.mit.edu/cubeportfolio/flutter-shutter/); Agrawal et al., SIGGRAPH 2009 (https://www.media.mit.edu/publications/invertible-motion-blur-in-video/); Kwon et al., J R Soc Interface 2013 (https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/). Publication novelty and human validation are not established.
