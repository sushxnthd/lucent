# E002-542 | Executable physical-acquisition and human-validation handoff

**Status: NOT PERFORMED.** This is a prospective protocol for authorized investigators, not evidence of a physical camera calibration or a participant study. It supplements, and does not replace, the already frozen E002-502, E002-519, E002-525 and E002-527 protocols. Do not put identifiable video, raw clock traces, participant mappings or individual ratings in the public repository.

## Stage 0: independent measurement and safety prerequisites

- Two independently clocked measurement channels: LED drive timing and **photodiode-measured optical output** sampled sufficiently faster than the shortest planned flash (target >=10 kHz for >=1-ms pulses, with measured sampling error). Use a common calibrated timebase or document a separately bounded synchronization error. An LED command timestamp alone is not an optical emission timestamp.
- An ordinary camera with locked focus, exposure, white balance and gain where supported; RAW/native frames preferred. Record model, firmware, codec, rolling-scan direction, native frame IDs and actual exposure settings. If manual control, native identity, or temporal-response calibration is unavailable, record `ABSTAIN`.
- A high-frame-rate reference camera with independent exposure and scanline calibration, not merely nominal fps metadata. For a human follow-up, use consented footage, documented data retention and local/private review. Do not claim that even a 600-fps reference is continuous-time ground truth.
- A rigid static optical target, diffuser and camera mount for Stage A. A mechanical aperture/fiducial with independently measured motion for Stage B. No human subjects until instrument transfer is characterized.
- An operator who cannot alter the predeclared thresholds after inspecting the held-out response. Record all failed acquisitions, not just successful clips.

## Stage A: physical shutter-response falsification (pre-register before capture)

1. Fix LED/camera geometry and measure dark, full-intensity, and independently calibrated 0.25/0.50 intensity levels with the photodiode. Characterize LED rise/fall, ambient flicker, saturation and exposure-dependent gamma/ISP. Acquire a separate linear-response/RAW control where possible.
2. Split aperiodic LED codes by **whole acquisition session**, not individual frames: training uses amplitude 1.0 coded illumination; hold out intermediate amplitudes and edge-pulse waveforms. Never use the held-out sessions to fit phase, gain, offset, exposure, row delay or residual cutoff.
3. For edge sweeps, step short LED pulses through the entire uncertain exposure/scanline interval, including 2 ms outside both ends. Use photodiode-measured optical onset/offset, not intended command times. Repeat at multiple row ROIs and across restarts, brightness levels and exposure settings. Derive a **set of possible shutter sensitivity kernels** with explicit uncertainty, not a single best-fitting timestamp.
4. Independently estimate timing error by repeated clock-reference checks before/after capture. Report drift, jitter, frame drop/missingness, rolling-row skew, ROI geometry and codec/ISP alterations. Freeze an allowed error envelope from independent noise and calibration controls.
5. Reject any transfer model whose held-out optical response lies outside its preregistered uncertainty envelope; reject if multiple timing kernels remain observationally compatible or the photodiode trace is missing. A good training residual is insufficient. Record failures by nuisance stratum.
6. Export only privacy-reviewed aggregate metrics: total sessions, number invalid, kernel uncertainty bounds, held-out residual distributions, and per-condition failures. Keep all native frame/photodiode records and integrity hashes in owner-private storage.

**Minimum input record per capture (private):** `session_id`, `device_model`, `firmware`, `manual_settings`, `native_frame_id`, `row_roi`, `photodiode_clock_id`, `photodiode_sample_rate_hz`, `led_onset_interval_ms`, `led_offset_interval_ms`, `frame_clock_interval_ms`, `pixel_brightness_interval`, `raw_or_isp`, `missing_or_clipped`, `partition`, `source_digest`. Interval bounds must include uncertainty; never replace unknown values with zero.

## Stage B: mechanical aperture and observability-bound test

Use the calibrated optical setup with a mechanical shutter/opaque target of independently measured aperture. Record synchronized ordinary and high-rate views. Predeclare each ordinary-camera guaranteed blind interior using **worst-case** clock, exposure and rolling-row bounds. Independently measure aperture geometry and motion; do not derive a hard speed ceiling by taking the largest sampled frame-to-frame velocity. Freeze E002-371/538/539 predictions before viewing the high-rate outcome. Include shifted phase, blur, glare, geometry mismatch and deliberately missing frames. Treat high-rate non-observation as censored. A qualified, independently timed closed-aperture witness inside a predicted exclusion is a falsification.

## Stage C: prospective human study (only after Stages A/B)

- Obtain consent and an appropriate ethics review determination before recruitment; no clinical/fatigue diagnosis or safety-critical use. Recruit a participant-disjoint calibration group and a sealed evaluation group. The earlier E002-537 analysis warns that 12 calibration participants are insufficient for nontrivial 95% split-conformal participant-level calibration under its assumptions.
- Collect native high-rate and ordinary-camera recordings with independently verified shutter timing, fixed gaze tasks plus controlled gaze changes, lighting, glasses/no-glasses where feasible, motion blur, eyelid geometry variation, and explicit missingness. Record task and nuisance strata, not identities in public outputs.
- Two genuinely independent blinded human raters mark upper/lower eyelid landmarks, iris scale, uncertainty and nuisance abstention using the existing E002-502 private packets. Freeze both ratings before adjudication. Rater independence cannot be inferred from file labels or software flags.
- Before inspecting held-out high-rate frames, publish a nonce-protected digest of every gap ID, timing envelope, anatomical threshold, participant split, `EXCLUDE`/`ABSTAIN` prediction, motion envelope source and calibration ID using E002-525/527-style prospective locking. No denominator changes after outcome review.
- A participant-specific hard continuous-time speed/acceleration bound is **not** established by sampled peaks or literature means. If such a bound cannot be independently justified, prohibit E002-371 hidden-closure **exclusion** claims. Positive witnessed contradictions can still falsify a prediction; missing witnesses remain reference-censored.
- Report participant-level false-exclusion witnesses, reference-censored fraction, abstention rate, interrater disagreement, timing/geometry uncertainty, nuisance strata and confidence intervals. Separate exploratory feasibility from locked confirmatory results. Never count multiple windows from one participant as independent participants.

## Release blockers and stop rules

**Stop / ABSTAIN** if the optical clock is unauthenticated, shutter kernel is multimodal, nonlinear transfer/blur is unresolved, participant consent or native provenance is missing, raters are not independent, cross-camera anatomical predicates do not transport, reference sensitivity is unbounded, or continuous-time human motion ceilings lack a defensible basis. A zero-observed-error pilot does not clear these blockers.

**Allowed before calibration:** display explicitly labeled experimental, nonmedical, noncertifying observations and instrument quality diagnostics. **Forbidden:** no-hidden-blink certification, continuous-time blink duration, PERCLOS, sleepiness/fatigue score based on unvalidated closure inference, or deployment-ready claims.

Next external action is a genuine physical capture with an independent photodiode/clock and camera, followed by two completed blinded S01 anatomical reviews on an authorized private machine. No such captures or reviews were performed in E002-542.
