# E002-651 — Negative-only shutter trials are not calibration evidence

## Falsification / identifiability result
For a trial with independently known pulse interval P and a *claimed* camera exposure interval E, the oracle returns a certified temporal miss when P and E are disjoint under endpoint uncertainty. A camera report of no pulse-specific signal is compatible with this claim. But it is also compatible with a **wrong exposure-timing model**, including a camera that did not expose at all, a sensor whose optical response was suppressed, or an unrelated exposure window. Therefore any number of negative-only observations cannot identify exposure timing or sensitivity. Calling these trials CONSISTENT invites an unjustified validation interpretation.

## Constructive counterexample
Let pulse P=[1,4] microseconds and asserted exposure E=[10,20] microseconds. No pulse signal is observed. World A: exposure E is correct and the pulse was missed. World B: the true exposure is [2,3] microseconds (intersects P) but sensor gain is zero, so the same observation is obtained. The CSV has identical pulse timestamps, declared exposure, and measured visibility in both worlds. Without independent sensor-response and exposure-reference measurements, the worlds are observationally indistinguishable.

## Enforced product consequence
The analyzer now emits NON_FALSIFYING / miss_not_seen_does_not_validate_timing, never CONSISTENT, for certified misses with no observed signal. This is **not** a positive timing certificate. Other paths still abstain. A synthetic metamorphic assertion demonstrates that a wildly displaced declared exposure interval produces the same NON_FALSIFYING verdict.

## Required discriminating physical experiment
Randomize phase and pulse duration; record reference photodiode waveform, measured shutter/exposure gates, LED-off controls, sensor response, and camera output. Include predeclared positive controls with strong, source-attributed exposure intersections and calibrated optical contrast, and deliberately perturb exposure timing to verify the analysis detects a false model. Keep pulse-only miss trials as negative controls. Use blinded held-out trials and preserve failures. A valid positive control requires independent shutter gate and sensitivity calibration, not merely a CSV declaration.

Evidence tier: logical identifiability counterexample plus committed code; **no acquired physical or human measurements**. No human blink/eyelid claim is authorized. Production BLOCKED; ABSTAIN_UNCALIBRATED.
