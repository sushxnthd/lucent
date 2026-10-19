# E002-306 — frozen measurement-science protocol

1. Exact pair: rectified ordinary RGB visible pupil arc sagitta normalized by independently measured iris radius versus synchronized high-speed pupil/iris radius reference.
2. Frontier: Worring & Smeulders 1995; Al-Sharadqah & Chernov 2009; EllSeg 2020; PuRe 2017; EyeSeg 2025.
3. Metric: minimax full-contour separation |s1-s2|/(2eta); selective reference coverage and abstention.
4. Strongest confound: photometric/glasses edge bias, eyelid occlusion and unknown gaze/optics make eta unbounded.
5. Forward model: see THEOREM.md; reduction to fixed-chord circular arc only after calibration.
6. Falsification: held-out human reference lies outside nominal certified interval; edge uncertainty bound fails under glare/lighting/gaze; reject the real-RGB claim even if geometric theorem holds.
7. Mechanism-derived boundary: radius hypotheses separable iff |s1-s2|>2eta.
8. Untouched human test: native RGB and independently synchronized high-speed eye reference, hold out participants/device/lighting, glasses strata; freeze crossing prediction before reading holdout.
9. Publication threshold: no geometry-only paper claim. Require calibrated edge-error bound, unseen human boundary crossing, independent checker, >=30 participants, >=2 devices, >=3 lighting conditions and glasses/no-glasses strata, strong baselines, uncertainty-aware 95%-nominal reference coverage and risk/abstention analysis.
10. Product consequence: reject uncalibrated rapid pupil/fatigue estimates; allow only conditional interval-valued projected pupil radius with mandatory abstention.

Four controls: geometry-only affine projection, brightness-only contrast collapse, missingness-only central arc loss, and temporal-smoothness-only two smooth radius trajectories with common observations. Synthetic controls passed, NOT human evidence.

Frozen synthetic holdout BEFORE checker: R=19.7px, eta=.22px, q=.08; predicted critical half-angle 40.37258267723 degrees; predicted indistinguishable at 37.37258267723 and distinguishable at 43.37258267723 degrees. Both confirmed independently. This is NOT a human holdout.

Data access: mEBAL2 RGB/NIR dataset requires signed license/credentials; its blink labels do not establish high-speed pupil-radius ground truth. Gaze4HRI gives RGB/mocap gaze, not pupil radius. No dataset archaeology beyond two blocked runs per path.
