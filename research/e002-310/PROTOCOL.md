# E002-310 protocol

Question: Can a photometry-normalized eyelid-edge position from ordinary RGB be certified against independent high-speed anatomical lid reference, and where does it fail?

Signal/reference: RGB upper-lid 50% contrast edge crossing relative to canthi versus synchronized >=250Hz manually verified NIR lid contour.
Literature: Ghosal and Mehrotra (1993) subpixel edges; Journal of Imaging 2020 blur/SNR localization; Navascues-Cornago et al. (2026) 500fps human blink kinematics.
Metric: prospective 95% coverage of calibrated position intervals, empirical boundary crossing, worst-group abstention and error.
Confounds: gaze-linked lid motion, spatial illumination gradients, glasses, missing edge, rolling shutter.
Model: Gaussian PSF + symmetric shutter + constant speed + positive affine brightness + bounded L2 error.
Falsification: reject if calibrated intervals fail held-out high-speed reference coverage or supposedly separable pairs collide.
Prediction: sharp contrast/blur/gaze/noise transition in THEOREM.md; 8.71ms is synthetic only.
Human test: freeze all calibration using training participants; hold out participants and devices/lighting/glasses; compare against geometry-only, brightness-only, missingness-only and temporal smoothness baselines.
Publication gate: independent reproduction, real held-out human transition, prior-art priority clearance.
Product: conditional interval-valued lid position only; abstain otherwise. No uncalibrated pupil/physiology inference.
