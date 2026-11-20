# E002-649 — Enforcement correction after E002-648 (2026-11-04 UTC)

## Scientific status
E002-648 proves that a binary visibility flag is not source-identifying: an ambient-light event and an LED-related signal can produce the same trial row even when the certified LED pulse misses the exposure. Therefore E002-647's `FALSIFIED` verdict for generic visible-during-miss was unjustified.

## Durable implementation consequence
The E002-647 analyzer now returns `ABSTAIN / unattributed_signal_despite_certified_miss` for generic visible-during-certified-miss rows. Its synthetic self-test was updated to enforce this outcome. The `CONSISTENT` verdict for invisible-during-miss remains conditional on the supplied (not independently authenticated) timing and visibility metadata; it is not proof of sensor calibration or physiological validity. No row in the current CSV contract can support source-specific falsification, and `FALSIFIED` should not be claimed from this contract.

## Frozen next physical experiment
Randomize LED-on and LED-off controls across matched pulse phases; independently record LED drive, photodiode source signal, camera raw frame sequence and ambient reference. Include delayed sensor persistence, saturation, rolling-shutter row drift, missing frames and clock uncertainty. Before viewing the camera outcome, preregister source-specific intensity-difference thresholds, dark controls, positive controls and exposure-miss predictions. Only independently authenticated source-specific evidence can support a shutter-timing falsification; otherwise abstain. Preserve all anomalies and calibration failures.

## Evidence boundary
Code correction and logical falsification only. No new physical captures, human eyelid recordings, certified physiological speed envelopes or participant-held-out predictions. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Do not count synthetic tests as independent empirical evidence.
