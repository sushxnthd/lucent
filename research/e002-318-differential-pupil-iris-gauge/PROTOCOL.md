# E002-318 mandatory active kernel and prospective test

1. Signal/reference: apparent p from paired pupil/iris conics in native ordinary RGB; independent high-speed anatomical q reference, synchronized to RGB exposure. Human test NOT RUN.
2. Frontier: Wang/Chern/Alexa 2019 already establishes the projective invariant; Aguirre 2019, Petersch/Dierkes 2022 and 2026 Snip & Stitch analyze gaze/refraction/PFE.
3. Metric: sharp identified-set width Q(1/rho-rho), strict sign certification, untouched coverage, abstention and error by participant/device/lighting/gaze/glasses.
4. Confound: time-varying pupil-vs-iris differential magnification m; also eyelid occlusion, glasses, color pipeline, shutter, sampling and nonconic boundaries.
5. Model: full RGB forward family in THEOREM.md, reduced p_t=m_t q_t and independently bounded rho<=m1/m0<=1/rho.
6. Falsification: any untouched reference q1/q0 outside frozen predicted interval, any false strict sign, or inability to independently establish optics/segmentation bounds. Do not widen after holdout.
7. Mechanism prediction: p0=.50,p1=.53,rho_crit=50/53; .94 ABSTAIN, .95 CERTIFY. Frozen before checks in FROZEN_PREDICTION.json.
8. Human protocol: native >=30 Hz ordinary RGB + trustworthy high-speed independent reference; synchronized shutter/timebase; calibration participants/devices separated from untouched participant/device/lighting/glasses holdout. Freeze segmentation, m-bound and sign rule before holdout. Compare geometry-only, brightness-only, missingness-only, temporal-smoothness and naive ellipse-area baselines. NO HUMAN DATA EVALUATED.
9. Publication threshold: independent calibration and reproduction, prospective unseen boundary crossing, nontrivial certified yield with coverage, and incremental novelty beyond established projective invariant/PFE correction. Synthetic algebra alone insufficient.
10. Product: no uncalibrated rapid pupil waveform or five-second fatigue certification; conditional interval-valued pupil/iris change with abstention. Fall back to shutter-mean eyelid occupancy if contour visibility fails.

Accelerator rule: at most two substantive blocked runs on one dataset/provenance route; then pivot to a different experiment or exact theory. No paid resources or user laptop.