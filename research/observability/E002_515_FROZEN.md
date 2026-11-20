# E002-515 | Physical optical-timing replay: frozen evaluation contract

Date: 2026-10-29. Primary E002-371 workstream, existing draft PR #26. **Frozen before any real instrument recordings.** No physical optical recordings, independent human ratings or camera-exposure truth are currently available. The local artificial fixtures used to debug the evaluator are software tests, not held-out scientific observations.

## Decisive question

Does the E002-514 set-valued shutter-window inference retain independently measured exposure boundaries on *unseen real camera recordings*, including non-affine clocks, while providing conservative upper bounds on unobserved gaps? Do not substitute nominal frame rate, AVI headers, screen animations, simulated optical signals or inferred camera clock for independent acquisition truth.

## Independent, physically measured inputs

1. `photodiode.csv`: `start_ms,end_ms,ch0,...,ch7`. Each row is a contiguous independently clocked optical interval; eight levels are independently measured, normalized to calibrated linear intensity, and piecewise-constant only within an independently justified bandwidth/timing error.
2. `camera.csv`: `frame_id,ch0,...,ch7`. Eight separately imaged, dark/flat-corrected, locked-gain raw camera-region means, in native frame order. No per-frame clock or nominal FPS is supplied to the inverse solver.
3. `reference.csv`: `frame_id,start_ms,end_ms,uncertainty_ms`. Exposure timing from a physically independent camera-sync/oscilloscope channel or an independently validated equivalent, acquired separately from the optical inverse; no timestamp fitted to the camera pixel vectors.
4. Precalibrated `residual-max` and `timing-envelope-ms` from **separate** instrument trials. Neither may be fitted to evaluation failures. Hardware identities, photodiode bandwidth, response linearity, clock phase, sensor geometry, scanline delay, frame continuity, saturation and radiometric calibration require external signed/inspectable evidence. CSV contents and booleans do not authenticate hardware.

Freeze a participant- and device-disjoint evaluation set before viewing reference exposures. Include nuisance strata: brightness, exposure/gain, blur, camera motion, rolling shutter, sensor-row shift, dropped frames, glasses/occlusion, and clock disturbances. A physically measured exposure outside all predeclared candidate intervals is a falsification, not an invitation to retune. For each frame, search all waveform-boundary shutter windows lasting 8–12 ms, without using the reference data. Retain all intervals whose eight-channel maximum radiometric residual is within the fixed calibration envelope. Only after candidate sets are frozen, open independent reference exposures to evaluate boundary coverage and blind-gap upper-bound errors.

## Frozen evaluation and kill criteria

- **FAIL** if any independent reference exposure has no compatible shutter candidate after the *precalibrated* timing envelope; or if any predicted blind-gap upper bound is smaller than the independently measured reference upper bound (including reference uncertainty).
- **ABSTAIN** on empty feasible sets, missing/damaged files, missing calibration, unbounded waveform or sensor response, nonlinearity, unknown code phase, unverified rolling-shutter mapping, clock uncertainty or missing independent truth. Zero evaluated gaps cannot pass.
- Report total frames, empty and unique candidate counts, exposure coverage, evaluated gaps, unsafe gap underbounds and worst gap margin. Stratify by nuisance condition in the private instrument log. No cherry-picked frames, no threshold changes after inspecting outcomes.
- The script can check consistency of supplied files but **cannot authenticate** photodiode origin, clock independence, physical exposure truth, response linearity or human physiology. A synthetic fixture PASS is a software check only. A physically consistent replay is not a certified shutter measurement until external instrument attestation and independent replication.

## Relation to E002-371 and product

This is a direct *real-data ingestion and falsification instrument* for the E002-514 proposed physical experiment, not another synthetic timing sweep. Do not use it to infer eyelid velocity or hidden human closures. The frozen E002-507 two-reviewer S01 packet, independently bounded continuous-time eyelid speed, physical per-gap exposure calibration and participant-disjoint predictions remain required. The product must always output `ABSTAIN_UNCALIBRATED`, release `BLOCKED` at this evidence tier. Hush remains separate.
