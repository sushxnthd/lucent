# E002-375 frozen human validation gate (2026-10-23)
No outcomes from human data were inspected. After two targeted searches, no freely usable paired ordinary RGB and high-speed eye-reference sequences were acquired. A 100-fps Silesian5 set requires a signed license.

Pre-register: independent >=250-fps eye reference and native 20/25/30/60-fps RGB. Hardware trigger or two bracketing synchronization anchors. Measure actual exposure w and rolling-shutter timing. Estimate each participant's closed-plateau duration D_i and velocity limit on calibration trials, then freeze before held-out trials.

Primary unseen prediction: if D_i>=F+w, at least one native exposure is fully within closure, independent of shutter phase. If D_i<=F-w, a phase can completely miss the plateau. Test predicted RGB closure visibility only after calibrating eye contrast and uncertainty. Hold out participants/devices/lighting. Compare geometry-only, brightness-only, missingness-only, temporal smoothness-only controls; stress gaze, glasses, blur and clock error.

Falsify if reference and camera exposure timestamps contradict interval coverage. Report image-classifier failures separately from geometric coverage. Abstain whenever calibration cannot certify observation. The published 58-ms mean is not a universal lower bound.
