# E002-439 — physical-clock and held-out human study handoff

**Status:** executable prospective protocol only. No participants, calibrated camera, photodiode, or physical optical clock acquired by this experiment. Obtain consent and institutional approvals where applicable. Keep raw eye videos and participant identifiers out of public CI.

## Hardware and independent evidence

1. Use a **borrowed** calibrated 400–600-fps camera with raw sensor exposure-start/end or externally measured exposure response. Record firmware, sensor mode, global/rolling shutter, optics and gain. A phone's nominal slow-motion FPS, container PTS or uncalibrated optical code is insufficient.
2. Use an independently clocked LED/timecode emitter or validated existing rig. The 2026 RocSync LED clock provides a published design reference; do not claim that Lucent's virtual software is that hardware. Record oscillator calibration/drift against a separate reference and LED drive/photodiode traces. Measure transition latency, light persistence, integration smear and per-row readout offsets using a stationary target and oscilloscope/photodiode if available. Record signed hashes of immutable calibration artifacts. Never infer independent oscillator timing from the same computer that encoded the video.
3. Capture the LED clock in the same sensor exposure as the eyelid or use an independently validated camera-to-clock registration. Verify two clocks' residuals, phase, drift, and exposure intervals, not just their displayed tick indices. Fail closed if CRC passes but the clock's row-splice/bit-transition state is unresolved.
4. Independently measure 3D or scale-corrected upper/lower eyelid aperture in **millimeters** with two blinded raters and anatomical calibration objects. Independently bound error from geometry, head pose, gaze, glasses, brightness, blur and occlusion. A finite observed maximum blink speed does **not** establish a deterministic universal velocity cap.

## Preregistered prospective test

- Seal the exact Lucent analysis commit, candidate physical velocity/acceleration envelopes, optical-clock decode criteria, threshold and nuisance masks **before** revealing held-out annotations. Split by participant (all sessions/eyes), and separately report voluntary, spontaneous and reflex blinks.
- Record synchronized 400–600-fps physical aperture and ordinary 25/30/60-fps camera observations with independently measured shutter kernels. Cross illumination, gaze, head pose, glasses, blur and intentionally missing frames. Keep high-speed and ordinary cameras' timing uncertainties distinct.
- First test the *instrument*: compare LED-derived exposure interval estimates to independently measured photodiode/hardware reference. Report absolute and signed errors, per-row variation, failures and abstentions; do not borrow the 1.34-ms RocSync result as a Lucent calibration.
- Next independently estimate the candidate **necessary** velocity lower witnesses (E002-438) and falsify invalid caps. If no independently defensible hard cap exists, **stop deterministic no-closure certification**. A separate, clearly statistical risk claim would require an entirely different participant-disjoint calibration protocol and risk bounds.
- Only with defensible physical premises freeze E002-371 gap predictions, then compare to independently blinded high-speed dual-rater closure adjudication (E002-436). Count false no-closure certificates, conditional negatives, witnessed crossings, unresolved reference intervals, abstentions and nuisance-stratified failures separately. Do not count unresolved reference frames as verified negatives.

## Required failure tests and release blockers

- Retiming, frame duplication, drop, reordering and replay; CRC collision and two-exposure row splice; optical gain, saturation, flicker and glare; LED-transition smear and camera auto-exposure; shutter readout direction, clock drift and sync-pulse loss.
- Reject physical claims if any optical-timecode or anatomical premise is not independently verified, even when the synthetic decoder and hosted CI pass.
- Require external measurement-science review of timing/geometry and independently reproduced participant-disjoint analysis before enabling a physical closure claim. Require security review if authenticity against adversarial media editing is claimed. Current state is `ABSTAIN_UNCALIBRATED`.
