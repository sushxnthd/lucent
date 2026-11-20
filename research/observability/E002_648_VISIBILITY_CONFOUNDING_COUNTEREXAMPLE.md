# E002-648 | Visibility-confounding falsification of the instrument oracle (2026-11-04 UTC)

## Finding: a visible frame is not evidence that the certified-missed LED pulse was captured

The E002-647 analyzer currently returns `FALSIFIED / visible_despite_certified_miss` whenever a CSV row reports `measured_visibility=yes` and the certified LED pulse interval is disjoint from the exposure. This inference is not identifiable from the schema. `measured_visibility` is a single Boolean and does not identify *which optical source* produced the signal.

Construct two physical worlds with identical CSV values, including certified pulse [1,4] microseconds, exposure [10,20] microseconds, valid hashes and `measured_visibility=yes`:

* World A: LED pulse is absent from the exposure, but ambient illumination changes during [12,13] microseconds, triggering the visibility detector. The shutter model is correct.
* World B: pulse leakage or a wrongly calibrated exposure interval produces the detector event. The shutter model may be wrong.

Both worlds produce exactly the same E002-647 row. Thus a deterministic classifier of that row cannot soundly conclude shutter-model falsification in both. This is an **information-identifiability counterexample**, not a physical observation. The same confounder can arise from another LED, auto-exposure, compression, sensor persistence, rolling-shutter rows outside the specified region, or incorrect event association.

## Immediate enforcement decision

Treat E002-647's `FALSIFIED` as **an anomaly requiring adjudication**, not a certified falsification, until the evidence establishes pulse-specific causal attribution. The existing script is not changed here because other active runs may be writing its branch; this packet is the durable, explicit negative result and implementation blocker. The next change should rename the outcome to `ANOMALY_UNATTRIBUTED` or return `ABSTAIN` for `measured_visibility=yes` without authenticated source attribution. Do not silently promote the previous result to empirical evidence.

## Precommitted discrimination experiment

Use independently timestamped photodiode pulses and raw fixed-exposure camera frames. Randomize LED-on and LED-off sham trials with identical ambient and camera settings, including randomized pulse phase and blind trial labels. Record a spatially localized LED-region intensity difference against an adjacent reference region; require a baseline dark/control trace, photodiode waveform, and unaltered raw frame with independently verified content hashes. A pulse-specific event is supported only if its spatial/spectral signature and trial-to-trial phase relationship distinguish LED-on from sham, with a predeclared false-alarm threshold. If any of these are missing, abstain.

**Discriminating prediction:** in a genuinely certified temporal miss, no prompt LED-specific integrated signal should appear in the relevant exposure under a validated zero-persistence sensor model; a generic positive visibility flag can occur in both worlds and cannot discriminate them. Sensor persistence and clock uncertainty must be separately bounded. A positive pulse-specific response during a certified miss then challenges at least one joint premise (exposure timing, sync, sensor memory, optical attribution), not automatically the shutter model alone.

## Evidence tier and product consequence

Logical counterexample to the sufficiency of the existing instrument CSV; no new hardware trials, human sequences, physiological bounds or external validation. E002-647 cannot establish physical shutter falsification from a generic visibility flag. Product remains `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Primary E002-371 held-out human validation remains the priority. No merge or Hush changes.
