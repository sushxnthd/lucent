# E002-367 prospective protocol (not yet executed)

Signal: native unresampled ordinary RGB eye video, pupil and iris conic fits, shutter timestamps, gaze, occlusion and brightness metadata. Reference: concurrent calibrated high-speed eye reference with independent clock anchors, physical or explicitly apparent pupil ratio.

Before opening holdout labels, freeze on training participants/devices: differential optical magnification amplitude delta, maximum log-rate K, apparent ratio error e, conic visibility gate and shutter/timebase errors. Predict one crossing using q1-q0>delta*(q0+q1)+2e and constant-pupil nuisance-speed feasibility.

Hold out participants, at least one device, lighting, gaze and glasses. Controls: geometry-only, brightness-only, missingness-only, temporal-smoothness-only, projective conic ratio without gauge correction. Cluster bootstrap by participant; report false certifications, interval coverage, abstention and subgroup results. Do not retrofit on final holdout. Reject transfer when nuisance bounds fail.

No dataset archaeology beyond two substantive blocked runs. No human validation has been executed.
