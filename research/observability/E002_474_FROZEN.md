# E002-474 FROZEN — cohort-tail versus cohort-mean camera-design decision

Date: 2026-10-27. This is a **post-hoc, cross-evidence product-design stress test**, not a preregistered independent human experiment, new physiology, or physical validation. Freeze this exact analysis before adding its executable implementation. The active scientific kernel remains E002-371.

## Inputs already public and immutable
- E002-459 checksum-linked published 2026 human per-blink aggregate, SHA256 of source CSV `6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43`: pooled calibration closing sample maximum 567.1039281430776 mm/s and opening maximum 274.61633650153254 mm/s. These are **sample estimates, not universal hard caps**.
- E002-473 independently published 2013 cohort **mean of individual peak voluntary closing speeds** 243 mm/s, https://doi.org/10.1098/rsif.2013.0227 . This is a different study/statistic and cannot be substituted for a tail cap.
- E002-472 existing conservative *symmetric* shutter-aware sufficient exclusion design gate. Do not change its mathematics, 1-mm endpoint clearance, 0.1-mm uncertainty, 0.1-ms ordinary clock error, 0.2-ms reference exposure, 0.1-ms reference clock error, or uniform symmetric shutter model.

## Frozen prospective computation and falsification
Evaluate 30 fps/4 ms, 240 fps/1 ms, 300 fps/1 ms, 480 fps/1 ms, and 600 fps/1 ms under (a) the 2013 published mean peak 243 mm/s and (b) the 2026 *sample maximum* 567.1039281430776 mm/s, **solely as hypothetical symmetric hard-speed stress values**. Compare the E002-472 evaluator against independently implemented exact-rational arithmetic. Report critical speed, strict minimum endpoint margin and dimensionless velocity/critical ratio. The 240/1 and 300/1 designs are predicted to lose **conservative conditional feasibility** when substituting the observed 2026 sample maximum for the 2013 mean, while 480/1 retains it under the frozen geometry. Explicitly preserve the E002-460 narrower ideal linear-aperture-mean directional model, which can give a different decision; no result here proves physical impossibility at 240/1.

Kill criteria: any mismatch between independent arithmetic and the actual E002-472 evaluator; any claim that 567 mm/s is a physiological upper bound, that 243 is a peak maximum, that a conservative failure implies an actual hidden closure, or that 480 fps is physically calibrated. No raw human rows, sealed holdouts or videos may be opened. All physical product outputs remain `ABSTAIN_UNCALIBRATED`.

## Decision consequence
If confirmed, retire **240-fps/1-ms at 1-mm margin as a defensible general-purpose conservative-exclusion pilot** under the published 2026 tail stress. Keep it as a physical acquisition/calibration testbed only. A 480-fps/1-ms configuration is an *illustrative sensitivity target*, not a validated device or sufficient product release. Prioritize independently timed physical capture and blinded anatomical trajectories; no more recycled peak-table archaeology after this decision.
