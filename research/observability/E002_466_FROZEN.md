# E002-466 — frozen detection-floor challenge (2026-10-26)

**Frozen before implementation.** Synthetic optical-instrument experiment only. No physical camera measurements or new human anatomical labels. E002-465's ideal phase scanner requires an exact zero/nonzero oracle. Real pulse detection has a nonzero floor.

## Prediction and kill criteria

Use a uniform, linear, noiseless global shutter with true exposure [0,0.4] ms, independently known optical pulse width 0.10 ms, phase grid -0.30 to 0.85 ms in steps of 0.05 ms, and detector threshold 0.15 in normalized integrated intensity. A phase is reported *detected* iff overlap(exposure,pulse)/0.4 > 0.15. Feed the binary detections into the E002-465 zero/positive transition formula **as if non-detection meant zero overlap**. Prediction: at least one true exposure endpoint lies outside the naive inferred interval. The ideal scanner's physical use must be vetoed.

Calibrated repair for the restricted noiseless model: with certified exposure width <= w_max, gain >= g_min >0 and known normalized detection floor tau, a non-detection implies overlap <= delta = tau*w_max/g_min. If a leading transition is genuinely bracketed and the pulse-overlap curve is unimodal, use conservative start interval [previous-nondetected-phase + p - delta, first-detected-phase + p]. For the trailing transition use [last-detected-phase, next-nondetected-phase + delta]. These are **synthetic-model bounds only**, not physically certified shutter supports. Reject missing transition brackets, unknown or drifting floor/gain, nonlinear response, timing uncertainty, optical/sensor tails, noise without separately certified bounds, rolling-row ambiguity, clipping, and missing phases.

## Frozen adversarial checks

1. Confirm the naive false bracket on [0,0.4] ms and verify that the widened bracket contains both true endpoints.
2. At tau=0, recover E002-465 ideal brackets.
3. Test held-out shutter offsets, widths, thresholds and phase offsets with independent exact overlap arithmetic; report any failures without modifying the frozen example.
4. Missing calibration or nuisance controls must yield `ABSTAIN_SHUTTER_UNCALIBRATED`.
5. Product remains `ABSTAIN_UNCALIBRATED`, physical release false, E002-371 not physically validated. No merge or deployment.

**Scientific scope:** a falsification of treating thresholded non-detection as optical zero and an instrument acceptance consequence; not a new physiological law. Physical imaging-path pulse scans, reference-encoder calibration and prospective anatomical testing remain required.
