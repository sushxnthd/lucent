# E002-725 — Instrument acquisition record gate and negative-control requirement

## Finding

The frozen E002-724 manifest is a randomized **schedule**, not a measurement record. It has no observed camera exposure interval, independently calibrated timing, measured aperture interval, reference closure label, or independent reference sensor calibration. The existing manifest therefore cannot be replayed as physical validation. A second design limitation is that sixteen nominal phase labels do not by themselves demonstrate that the commanded phase was attained, nor do they specify positive/negative ground-truth closure controls.

## Executable artifact

`e002_725_acquisition_gate.py` validates a minimal acquisition record schema and fails closed on missing fields, malformed/nonfinite numeric bounds, invalid exposure order, negative uncertainty bounds, inconsistent aperture intervals, duplicate trial identifiers, absent reference closure labels, or non-instrument participant identifiers. `RECORD_COMPLETE_NOT_CALIBRATED` means **schema-complete only**: it does not certify calibration, measurements, or a theorem prediction.

Local regression: five checks passed, covering a complete synthetic record, missing reference label, invalid exposure ordering, NaN velocity bound, and duplicate IDs. These are software checks only.

## Frozen physical acquisition amendments

1. Archive E002-724's randomized manifest before acquisition; do not overwrite it.
2. Record independent sensor type and calibration ID; archive raw photodiode/encoder traces and camera frames with native exposure-start/end timestamps, clock offset and bounded synchronization uncertainty.
3. Record **measured** phase, not merely the requested phase. Include independently verified complete-closure and no-closure negative-control trials, with predeclared physical actuator trajectories.
4. Measure or conservatively bound the occluder speed continuously using independent hardware calibration; sampled image slopes are not velocity certificates.
5. Before viewing ground truth, freeze certificate predictions from lower aperture, upper gap, and independently bounded speed. Separately retain reference-invalid and calibration-invalid abstentions.
6. Evaluate nuisance strata separately (lighting, blur, gaze, glasses, occlusion, geometry, missingness, exposure timing) and retain all failures.
7. If any reference-confirmed closure occurs in a certified exclusion interval, classify as falsification of the joint model/calibration. Instrument success cannot authorize human blink claims.

## Evidence tier and product consequence

This artifact is a prospective acquisition gate plus locally tested software, **not physical or human validation**. No new physiological speed ceiling exists. Product must remain `ABSTAIN_UNCALIBRATED`; production remains `BLOCKED`. Next substantive work requires raw independent physical sensor measurements or genuinely held-out human sequences, not another synthetic parameter sweep.
