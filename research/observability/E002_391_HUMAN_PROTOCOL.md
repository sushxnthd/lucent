# E002-391 prospective human and physical-camera validation protocol (not executed)

**Purpose:** Resolve the central missing empirical evidence for E002-371; distinguish shutter-gap impossibility predictions from optical/labeling failures. E002-391 phase sweeps are optional *calibration-instrument* controls, not a substitute for a single-event human test.

## Stage A — physical camera and surrogate instrument
1. Build a moving-aperture surrogate with independently measured displacement versus time and a hardware clock. Acquire raw ordinary RGB at 30 and 60 Hz, plus >=1000-fps short-exposure reference. Record **actual exposure start/end timestamps**, not nominal FPS; independently measure exposure integration, rolling-shutter row delay and clock offset using a flashed LED/timecode visible to both devices.
2. Sweep programmed event speed, threshold dwell, and event phase. Freeze the E002-371 and E002-389 predictions **before** exposure, including which timing gaps should permit hidden crossings. Hold out one camera and at least 20% of speed/phase combinations.
3. Deliberately stress geometry, illumination/gain, blur, gaze-like geometry, glasses/reflections, missing frames, partial occlusion and clock drift. Do not treat nominal capture metadata as validated timing. Record raw, pre-compression and compressed data separately.
4. E002-391 optional instrument control: repeated phase-locked surrogate event vs independent uniform phase sweep vs ±1-ms jitter. This verifies whether an acquisition method can reveal a known aliased event; do not translate repeated-event detection into an individual-event negative guarantee.

## Stage B — human study, after consent and ethics review
- **Pilot:** 60 consenting adults; no minors. Acquire synchronized >=1000-fps short-exposure eyelid reference and ordinary RGB at 30/60 Hz. Do not claim clinical fatigue diagnosis. Minimize face data retention and separate identity keys; publish only consented, deidentified derived aperture/time traces.
- Disjoint reference-calibration participants estimate eyelid aperture-speed distributions and reference-label adequacy; distinguish an empirically high quantile (statistical) from a physically guaranteed upper bound (not inferable from a finite cohort). Do not use test participants to set speed envelopes.
- Freeze threshold definitions, event-duration cutoffs, camera timing error, RGB aperture-transfer error, nuisance bounds, abstention gates and E002-371 predicted admissible/hidden crossing intervals before touching held-out participants.
- Hold out participants, cameras, illumination conditions and spectacles. Do not pool correlated frames as independent observations. Pre-register participant-cluster bootstrap uncertainty, per-device risk, coverage, sensitivity and **false no-hidden-closure certificates among issued decisions**.
- Label each high-speed event as confirmed threshold crossing, confirmed non-crossing, or **reference-unresolved** based on exposure and temporal adequacy; exclude unresolved labels from naive binary accuracy but report their prevalence and sensitivity bounds.
- For any hard certificate require **deterministic** independently validated worst-case bounds, not only a 95% empirical calibration interval. Otherwise provide calibrated statistical output with explicit assumptions and abstain from hard guarantees.
- Publish code, timing calibration, device parameters, failed predictions, optical controls and data access protocol. Require independent replay and outside technical review before product release.

## Stop / kill criteria
Any unexplained false no-hidden-closure certificate under claimed bounds blocks hard certificates. If the real RGB transfer cannot support aperture inference under held-out nuisance conditions, remove the observable rather than fit it post hoc. If the reference cannot resolve the event, record uncertainty rather than a negative label. No PERCLOS, blink-based fatigue or five-second diagnosis without separate clinical/construct validation.

**Resource boundary:** no hardware or human data were acquired during E002-391; this is a concrete prospective study design only.
