# E002 Baseline + Specificity Amendment 014

Status: **PRE-OUTCOME, additive only**  
Parent protocol: `experiments/RGB_REFERENCE_OBSERVABILITY_002_PROTOCOL.md`

## Why this amendment exists

The frozen E002 protocol correctly makes a dimensionless pupil/reference ratio the primary observable, but its explicit baseline list does not separate the simplest prior-art pupil/iris ratio from any later calibrated or quality-aware variant. Pupil/iris normalization is prior art and cannot be a novelty claim. EyeDentify also changes screen colour to evoke pupil responses, so photometric nuisance can covary with the Tobii waveform.

This amendment does **not** alter any frozen E002 gate, threshold, split, preprocessing choice, or PASS/FAIL rule.

## Mandatory comparator ladder

Report all methods on the identical held-out participants and identical accepted/failed clips:

1. raw pupil diameter in pixels;
2. released PupilSense absolute-mm estimate (negative comparator only; no rescue);
3. **direct pupil/iris diameter ratio**, with no learned calibration;
4. any proposed calibrated/quality-aware dimensionless observable;
5. participant-independent mean-response waveform;
6. **photometry-only nuisance predictor** using no pupil geometry.

Any method beyond (3) must report paired participant-bootstrap deltas versus (3) for waveform correlation, normalized RMSE, response-direction agreement, and timing error. A result is not an estimator advance merely because it beats raw pixels or PupilSense.

## Photometry-only negative control

Features may include only quantities that cannot encode pupil geometry directly:

- whole/face/eye-crop luminance summaries;
- RGB or chromaticity summaries outside the segmented pupil;
- stimulus identity/colour and elapsed time, when available.

No pupil diameter, pupil mask area, iris/pupil ratio, pupil-centred texture, or Tobii-derived feature may enter this predictor.

Fit on training participants only. Evaluate unchanged on held-out participants.

Also report:
- within-stimulus Tobii circular-shift/null distribution;
- participant permutation null;
- left-eye RGB vs right-eye Tobii mismatch where both are available.

## Specificity interpretation

A numerical E002 PASS is **not sufficient for a biological-observability claim** if a nuisance-only predictor approaches the geometric observable.

Predeclare the following interpretation flag:

`SPECIFICITY_FAIL` if the photometry-only predictor's held-out median waveform correlation is within 0.10 absolute correlation of the primary geometric observable **or** if its normalized RMSE is within 10% relative of the primary geometric observable.

This flag does not retroactively change E002 PASS/FAIL. It limits interpretation to: *the RGB recording predicts the reference waveform under this stimulus protocol, but geometric pupil observability has not been isolated.*

## Claim boundary

Normalization itself is prior art. A defensible adjacent contribution requires evidence that explicit geometry carries held-out waveform information beyond stimulus/camera photometry, and that any added calibration improves over the uncalibrated pupil/iris ratio on untouched participants.

No fatigue, sleepiness, smartphone deployment, clinical, or five-second state-validity claim follows from this amendment.
