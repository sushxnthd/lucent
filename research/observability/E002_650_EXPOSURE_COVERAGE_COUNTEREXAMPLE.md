# E002-650 | Unenumerated exposure counterexample and enforcement correction

## Falsification
A pulse occupies [25,26] microseconds. A declared exposure is [10,20] microseconds. E002-647 classified this as a certified miss. However a second exposure [24,27] microseconds, from an additional frame/scanline/integration window not represented in the row, intersects the pulse. The same recorded row is compatible with both a true miss and a pulse intersection. Hence a single interval is insufficient unless exposure coverage is complete.

## Enforced consequence
The E002-647 CSV analyzer now requires `exposure_coverage_status=complete_single_exposure`; absent or other values abstain. This is a *self-reported declaration*, not an independently verified completeness certificate. Even when supplied, the result remains USER_SUPPLIED_UNVERIFIED_INSTRUMENT_ROWS. The self-test now includes missing and multiple-exposure abstentions. No physiological or physical inference is authorized.

## Acquisition requirement
A physical run must independently record all relevant exposure windows for each pulse, including rolling-shutter rows, dropped/duplicated frames, temporal processing, and persistence. Multiple windows require an interval-union oracle; this conservative single-exposure analyzer must abstain instead. A manifest signed by an independent acquisition process should bind the reference waveform, camera video, clock mapping, and enumerated windows. Hash strings alone do not authenticate the manifest.

## Evidence and limits
Logical counterexample plus enforcement change; no measured physical shutters, human trials, or physiological bounds. Tests have not been independently executed at authoring. Product remains ABSTAIN_UNCALIBRATED / BLOCKED. Preserve this negative result rather than reporting a physical falsification.
