# E002-685 — Executable physical-reference falsification gate

Evidence tier: **instrument replay infrastructure, synthetic self-tests only**. No new human or physical recordings.

## Frozen prospective procedure
Acquire a calibrated occluder trajectory with an independent synchronized photodiode or high-speed reference sensor. Predeclare physical aperture units, threshold, reference uncertainty, maximum physically justified velocity, conservative effective blind gap including exposure/rolling-shutter/clock uncertainty, and calibration/holdout separation **before** inspecting holdout labels. Authenticate the sensor and its calibration out of band. Record one CSV row per tested gap with columns: trial,phase,left,right,threshold,velocity_ceiling,gap_upper,reference_min,reference_error,authenticated. Use 'external_verified' only after an independently recorded chain-of-custody decision; the CSV string alone is not evidence of authenticity.

Run `python research/observability/e002_685_physical_replay.py capture.csv`. Without arguments, the script runs six synthetic self-tests. Endpoint feasibility is checked, then the sharp conditional velocity lower bound max(0,(left+right-velocity_ceiling*gap_upper)/2) is compared strictly with the closure threshold. The reference truth is CLOSED only when reference_min+reference_error <= threshold; OPEN only when reference_min-reference_error > threshold; otherwise INDETERMINATE. A certified exclusion with independently verified CLOSED reference is a falsification, and must block the affected product regime. Keep all failed, indeterminate and abstained trials in the denominator reports.

## Critical limitations
This gate does not authenticate physical records, calibrate clocks or establish physiological velocity ceilings. The instrument trial must independently verify those prerequisites and keep the raw sensor waveforms and camera timestamps available for blinded replay. Reference sensor occlusion and measurement transfer functions must be separately calibrated. Synthetic tests include a deliberately contradictory reference witness to demonstrate that false exclusions are counted; this is **not** a measured error rate.

## Acceptance criteria
No certification release without externally audited calibration, participant-disjoint human validation, independent replay, and prospective false-exclusion/coverage reporting with confidence bounds and nuisance strata. This artifact is intended to make the physical E002-671 experiment immediately machine-replayable, not to substitute for it. Product remains ABSTAIN_UNCALIBRATED; release BLOCKED.
