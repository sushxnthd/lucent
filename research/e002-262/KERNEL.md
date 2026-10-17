# E002-262: Original-human clock-anchor admission (corrected before outcome)
Date 2026-10-17. Frozen source P_33/P_54, start+5..10s.
Question: Does the native same-session Tobii record contain at least two distinct bilateral valid-free gaps of >=100 ms, permitting a subsequent independent RGB eyelid-event clock test?
Signal/reference: RGB eyelid closure times (not yet evaluated) versus native Tobii valid-free event times; primary kernel RGB pupil/iris ratio waveform vs same-eye Tobii pupil diameter.
Frontier: E002-254 proved nearest-valid coverage is insensitive to ±1s offsets. EVE Basler positive control access pending.
Scalar: count of >=100ms intervals between consecutive timestamps in UNION of valid left/right Tobii measurements. >=2 is a necessary, not sufficient, clock offset+drift anchor gate. 150ms sensitivity threshold.
Strongest confound: regular 120Hz invalid Tobii records with valid ~40Hz sampling, tracking loss unrelated to blink, browser start not exposure time.
Decisive falsification: <2 bilateral valid-free gaps; or RGB event mismatch.
Publishable: independent synchronized human waveform, prospective frozen correlation/lag/amplitude/NRMSE, participant/device holdout, nuisance controls, independent checker.
Product: reject unsynchronizable clips; require >=75% prospectively accurate admitted windows.
Kill: if both original clips lack event anchors, retire their blink-clock certification path and prioritize EVE/other verified synchronization. No fatigue claim.
SCIENCE: The initial >=2 consecutive invalid-row proxy failed scientific validity: periodic invalid samples are not sustained signal loss. This correction is pre-outcome and preserved in history.
PRODUCT: Only valid-free gaps can even be considered for an event anchor; no deployment changes until waveform results.
