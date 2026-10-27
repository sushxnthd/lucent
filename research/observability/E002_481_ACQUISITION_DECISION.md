# E002-481 physical acquisition decision: sensitivity class, not exact zero

This supplements E002-477/E002-480. It is **not** a physical calibration certificate.

Before seeing a held-out session, use independently authenticated calibration to freeze: minimum feature width L_min and amplitude A_min, independently measured optical pulse width w, timing uncertainty u and correlation model, detector contrast error epsilon, threshold theta, frame period T, row/exposure mode and phase count N. Predict the binary held-out detection for every row, brightness, phase offset and nuisance condition. An eligible positive class-detection prediction requires `A_min*max(0,min(w,L_min,(w+L_min)/2-u-T/(2N)))/w-epsilon > theta` **with a prespecified margin**. If A_min or L_min cannot be justified independently, **ABSTAIN**. Do not interpret a negative optical measurement as exact zero.

Record independent photodiode/logic-analyzer pulse times, pulse-to-frame IDs, raw linear camera response, dark/flat noise, gain/brightness, rolling-row differences, optical tails, saturation, blur, missing/dropped frames and clock jitter/drift. Include injected positive features above and below the threshold, no-feature controls, held-out phase offsets, correlated-clock challenges and post-power-cycle repeatability. Preserve raw logs privately and publish reproducible deidentified analysis. Do not silently refit on holdout failures.

After a physical optical test, obtain independently encoded moving-aperture trajectories with closure-present and closure-absent controls. Human study requires consent/approval, blinded participant-disjoint anatomical references, gaze/glasses/occlusion/illumination challenges and separation of anatomical aperture from image landmarks. Any contradicted exclusion falsifies its joint assumptions. A participant sample maximum is never a universal velocity cap.

Until independent physical and human validation, retain `ABSTAIN_UNCALIBRATED` for hidden closure, blink duration, PERCLOS, fatigue and medical claims. No merge or deployment.
