# E002-326 frozen kernel and human gate

1. Signal/reference: calibrated RGB pupil/iris feature vs independent high-rate anatomical pupil ratio with native timestamps.
2. Literature: pupil-light-reflex latency and RGB smartphone pupillometry; see PRIOR_ART.md.
3. Metric: minimax shutter margin M(s); future human false-certificate rate, coverage and abstention.
4. Nuisance: stimulus-locked automatic exposure, display reflections, illumination and unknown optical gain.
5. Generative model: exposure average of p+n with bounded error, timing, nuisance amplitude/support.
6. Falsification: a held-out null with positive certificate, a reference response outside certified interval, or direct-path persistence beyond calibrated tau_c.
7. Boundary: Scrit in THEOREM.md and FROZEN_PREDICTION.json.
8. Untouched human test: not completed. Reserve participants, devices, light and glasses conditions.
9. Publication threshold: independent prospective human boundary crossing with all nuisance controls, prior-art novelty and external reproduction.
10. Product: reject uncalibrated active-probe physiological and five-second fatigue claims; redesign around reference and photometric controls.

HUMAN PREREGISTRATION: Concurrent ordinary RGB with exposure-start/end metadata, actual stimulus luminance timestamps, independent >=90-Hz eye-reference and clock anchors. Disjoint calibration and final test participants/devices. Freeze normalized ocular feature, skin/iris photometric control, error bounds, response windows, rejection rules and test statistics before final labels. Test a predicted certifying window and neighboring abstention window. Report all trials stratified by participant, gaze, glasses, device and lighting; compare geometry-only, brightness-only, missingness-only, smoothness-only and constant baselines. Report false certificates, abstention, interval coverage and confidence intervals; no universal claim from tiny cohorts.

ACCESS LIMIT: EyeDentify published webcam/Tobii data but processed reference folding and unavailable native timestamps undermine fast-waveform claims. RGBE-Gaze raw RGB/event/gaze data and pupil-reference suitability not established. Stop data archaeology after two blocked attempts; switch scientific route. No human outcome inspected in this kernel.
