# E002-276 model, controls and prior art

Full RGB model: an image is an exposure-integrated, sampled and quantized photometric transformation of PSF-blurred iris/pupil surfaces, masked by eyelid/glasses aperture, projected by gaze geometry, scaled by camera distance, distorted by differential corneal magnification and contaminated by glare/brightness. Sample times t_k=k/f+clock_error_k. Pupil/iris ratio cancels shared scale only, not differential optics or contour bias.

This run isolates one necessary geometry condition under ideal known boundary angles. It does not validate a complete RGB camera model. Gaussian least squares achieves the stated exact conditional variance. For continuous uniform angles in [-alpha,alpha], eta=1-(sin(alpha)/alpha)^2/[1/2+sin(2alpha)/(4alpha)] ~ alpha^4/45.

Frozen synthetic settings: n=60, sigma=.5 px, true radius=20 px, 4000 trials per angle, tolerance=1 px, seed=2762026. Development alpha .12,.20,.35,.50,.65,.80,1,1.2,1.57. Synthetic holdout alpha .58,.93. Predicted holdout success .59306 and .97454; observed .61175 and .97300. This is not untouched human evaluation.

Wildcard: 60 samples from two antipodal +/-0.15-rad arcs have theoretical radius SD .06455 px; one contiguous +/-0.15-rad arc has SD 18.58061 px. Angular arrangement matters more than count in the oracle model.

Prior art: Barbosa & James 2014 https://pmc.ncbi.nlm.nih.gov/articles/PMC4132980/ ; Topal et al. 2017 https://arxiv.org/abs/1709.06366 ; Wang et al. 2019 https://arxiv.org/abs/1902.04541 ; entrance pupil optics https://pmc.ncbi.nlm.nih.gov/articles/PMC6597540/ ; visible-light pupil https://arxiv.org/abs/2305.06425 .

Failed gates: no human waveform, photometric calibration, participant/device/lighting/glasses holdout, reference-blind admission test, or prospective lag/NRMSE test. No field-level breakthrough claim.
