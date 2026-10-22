# E002-374 frozen nonlinear-instrument test, 2026-10-23

Hypothesis: E002-373's equal exposure-mean aperture does not imply equal full RGB observations. Independently integrate a nonlinear channel observing exposure mean of aperture squared. Expected first moment collision m=191/192 and second-moment separation Delta=31/184320 per exposure. Pre-register distinguishability under independent bounded errors epsilon iff Delta>2 epsilon.

Expected exact two-channel photometric collision: variable-history gain=1, offset=0; constant-history common gain=924/955 and additive offset=31/960. These are idealized synthetic instrument parameters, not measured RGB-camera calibrations. The two channels are E[a] and E[a^2]. Verify all values with exact rational arithmetic.

Add a third moment to test whether the two-parameter photometric gauge is overconstrained. No human-validation claim. The frozen E002-373 human protocol remains unchanged. Product gate: scalar collision alone does not establish complete RGB indistinguishability; nonlinear rescue requires independently bounded photometric nuisance.
