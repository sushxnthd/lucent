# E002-262: Human bilateral-event clock preflight
Date: 2026-10-17. Pre-outcome gate, source pins and prior data are frozen.
Question: Can the native Tobii reference independently supply at least two candidate binocular blink-loss episodes during original-human five-second RGB windows, allowing any subsequent RGB/event clock calibration?
Signal/reference: RGB eyelid closure (not evaluated) / Tobii bilateral validity-loss timestamps. Primary kernel remains normalized RGB pupil/iris dynamics / same-eye Tobii pupil diameter.
Frontier: E002-254 found nearest-reference matching insensitive to ±1s offsets. E002-261 EVE Basler is a synchronized positive control, but registration pending.
Scalar: number of distinct bilateral invalidity episodes of >=2 consecutive samples, with <=100ms intra-episode gaps, within start+5..10 seconds. >=2 only admits clock offset+drift estimation; does not prove synchronization or that losses are blinks.
Strongest confounds: tracker dropout unrelated to blink, eyelid occlusion without invalidity, webcam exposure timestamps, lighting/gaze.
Decisive falsification: fewer than two reference candidates in a window, or RGB candidate mismatch after independent detection.
Publishable success: untouched human within-session waveform, native timing provenance, nuisance controls, independent replay, holdouts, mechanism-derived prediction.
Product relevance: a rejected clock gate prevents spurious rapid ocular claims. Final threshold >=75% accurate accepted windows.
Kill: if both original windows fail event admission, retire them for crossmodal blink clock certification and switch to EVE or other independently synchronized human data. Do not pursue fatigue.
SCIENCE: preflight counts and negative gates only; validity dropout is not a proven blink.
PRODUCT: reject unsuitable data rather than inventing synchronization. No app/UI build.
