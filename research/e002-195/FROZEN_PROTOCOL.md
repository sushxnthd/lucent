# E002-195: original paired-data byte-range preflight

Frozen before remote test, 2026-10-15 IST. No human waveform scoring authorized.

**Primary signal/reference:** native-time RGB log(pupil radius/iris radius) against independently synchronized same-eye Tobii pupil diameter (mm), with reference validity.
**Frontier:** webcam pupillometry exists; Lucent has no untouched native-time paired RGB/reference success. EyeDentify labels timefolded; EVE access gated; EOTT original archive potentially paired but byte eligibility unknown.
**Scalar metric:** lower 95% participant-bootstrap Pearson waveform correlation on held-out five-second windows, no test-set lag optimization.
**Confounds:** auto-exposure/gamma, illumination, blur, subpixel geometry, eyelid/gaze occlusion, camera/tracker clock offset.
**Falsification:** held-out waveform fails gates or brightness/geometry controls explain equal/greater agreement.
**Publishable gate:** >=8 untouched participants, >=3 windows each, bootstrap lower r>0.30, >0.10 control margin, |lag|<=100ms, amplitude ratio 0.5–1.5, NRMSE<=0.75, >=75% accepted coverage, unseen devices/lighting/glasses, independent checker, mechanism prediction and prior-art audit.
**Product gate:** >=75% intended-use accepted coverage at calibrated accuracy; else abstain.
**Kill:** 2 blocked EOTT access attempts switch route; 3 non-discriminating primary runs reformulate.

**This run:** HEAD + first/tail HTTP byte ranges against original EOTT ZIP, retaining only HTTP headers, SHA256 of response chunks, and ZIP EOCD metadata. Strict 256 KiB read cap. A successful HTTP range is not proof of usable native-time reference. No participant video is retained. Infrastructure failure is not physiological falsification.

**Wildcard:** E002-194 phase diversity remains conditional on known shifts and stable optics. No new human gate tuning or fatigue inference.