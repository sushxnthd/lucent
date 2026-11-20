# E002-677 | Rolling-row mismatch defeats nominal-timestamp gap certificates (2026-11-06 UTC)

**Evidence tier:** locally executed, exact-rational adversarial synthetic counterexample; no human/physical evidence. This is a camera-timing nuisance falsification, not a new physiological theorem.

## Construction
Take normalized open aperture 1 at two observations, closure threshold tau=0.30, and assumed maximum speed V=30 aperture units/s. For a blind interval D, the sharp triangular closure witness is feasible if V D >= 2(1-tau)=1.4. A nominal 40-ms timestamp gap gives V D=1.2 and a nominal *exclusion*. But if the observed feature comes from different rolling-shutter rows in the two frames, the first relevant row may be captured 10 ms earlier and the second 10 ms later than their nominal timestamps. The actual blind interval is then 60 ms, giving V D=1.8; a continuous piecewise-linear closure trajectory exists with minimum aperture 1-30(0.060)/2=0.10, below tau. The naive certificate is false even if V is genuinely valid and the endpoint apertures are perfect.

**Critical qualification:** a fixed identical row offset in consecutive frames cancels and does not create this mismatch. The attack requires a *difference* in effective row offsets (e.g., vertical gaze/face movement, crop/ROI changes, differing feature row, or inconsistent frame timestamp semantics). Row offsets must be independently measured, not guessed.

## Executed frozen matrix
Nominal gaps 30/35/40/45/50 ms crossed with symmetric opposing row offsets 0/5/10/15 ms: 20 exact-rational configurations. **10** yield a nominal exclusion while the actual blind interval admits a closure. These are constructed adversarial cases, not an estimated failure frequency. The code asserts the corrected conservative criterion never excludes its own closure witness. Reproduce: `python research/observability/e002_677_rolling_row.py`; expected: `cases 20 false_nominal_certificates 10`.

## Instrument falsification
On an actual rolling-shutter camera, place a timestamped LED edge or moving calibrated aperture at multiple sensor rows. Independently measure row readout times and frame timestamp convention with a photodiode; sweep row displacement and exposure settings. Predeclare row-aware effective exposure intervals and predict which nominal exclusions become abstentions before inspecting reference closures. Compare against a global-shutter control and test blur, missing frames, brightness, glasses-like reflections, gaze, geometry and clock drift. No physical trial was performed.

## Product consequence
A frame-level timestamp alone is insufficient for a gap absence certificate when the effective observation row can move. Compute the **maximum physically possible unobserved gap** over independently bounded row-readout, exposure, clock and tracking uncertainties; apply E002-371 only to that conservative gap. If the required bounds or row linkage are unavailable, **ABSTAIN_UNCALIBRATED**. Production remains **BLOCKED**. No human eyelid speed ceiling or sleepiness claim is established.
