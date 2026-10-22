# E002-359 prospective protocol (frozen; no human outcomes opened)
Target: native RGB event-vs-none pupil-change observability, reference independent >=90-Hz pupil diameter; >=500-Hz independently clocked aperture for blink-onset timing. Never use a 10-Hz downsampled loader for native RGB timing.

Before opening holdout, independently calibrate native shutter width/readout, RGB ISP and gamma, pixel-integrated annulus/eyelid template, blur, contrast, whole-video residual norm, eye-reference timing and clock drift. Split by participant, reserve a device if possible, and reserve an unseen lighting/gaze/glasses regime. Freeze a numeric predicted crossing of d_min=2epsilon. Report abstention and violations.

Required four baselines: geometry-only, brightness-only, missingness-only, temporal-smoothness-only. Compare identical splits and reference event definitions. Learned black-box secondary only. Primary outcomes: binary event balanced accuracy, conditional certificate coverage, false-certification rate and participant-cluster bootstrap intervals.

No human data evaluated. EyeDentify 30-fps webcam/90-Hz Tobii data are a candidate for slower pupil variation, not automatically a high-speed blink reference. Stop after one more blocked access attempt on this path.