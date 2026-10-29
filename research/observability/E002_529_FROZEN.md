# E002-529 | Frozen adversarial test: speed ceiling does not imply closure dwell

Date: 2026-10-29. Primary E002-371 kernel, established branch `research/observability-human-boundary`, draft PR #26. This protocol is frozen **before** the construction, tests, or outcomes. No human measurements, independently calibrated shutter, or certified physiological speed bound are asserted.

## Targeted inference to falsify

E002-528 gives a full-reference-exposure opportunity conditional on **known continuous below-threshold dwell duration** `d`. An attractive but unproved shortcut is to substitute the E002-371 minimum **whole excursion time** `2(b-c)/V` for `d`, given open ordinary-camera endpoints `b`, closure threshold `c`, and speed ceiling `|a'(t)| <= V`. Test whether this shortcut is valid.

## Frozen prediction

For `0<c<b<=1`, `V>0`, and a blind gap `H>2(b-c)/V`, there are continuous, piecewise-linear, V-Lipschitz aperture trajectories `a:[0,H]->[0,1]` with `a(0)=a(H)=b` and a strict below-c interval of **arbitrarily small positive duration epsilon**, even though the entire down/up excursion takes at least `2(b-c)/V`. A reference camera's full-exposure probability for that interval is therefore `clamp((epsilon-e-2u)/P,0,1)`, not `clamp((2(b-c)/V-e-2u)/P,0,1)`.

Explicit construction for `0<epsilon<min(H-2(b-c)/V, 4c/V)`: set `h=V*epsilon/4`; descend at speed V from b to c-h, stay at c-h for epsilon/2, ascend at speed V to b, and center the excursion inside H. The below-c dwell is exactly `epsilon`. The excursion duration is `2(b-c)/V+epsilon`.

Frozen hypothetical numbers: `b=1`, `c=1/5`, `V=60/s`, `H=1/30 s`, `epsilon=1/10000 s`. Predict excursion duration `803/30000? [do not use this mnemonic; compute exact]` and below-c dwell `0.1 ms`. With 240 Hz, 1-ms exposure, 0.1-ms endpoint uncertainty, predict full opportunity `0` and ideal positive overlap `0.264`. With 1000 Hz, 0.5-ms exposure, zero uncertainty, predict full opportunity `0` and overlap `0.6`. Even a certified speed bound alone cannot imply a nonzero minimum reference full-exposure sensitivity for threshold closure.

## Prespecified falsification checks

1. Exact-rational construction; endpoints b; aperture range [0,1]; continuous junctions; each segment's absolute slope <=V; strict below-c duration epsilon; excursion fits inside H.
2. Frozen 240-Hz and 1000-Hz opportunity predictions; show the invalid excursion-time substitution would produce materially higher probabilities.
3. An independent implementation checks segment timing and duration without importing the primary Python evaluator; enumerate 10,000 exact rational reference phases for the 240-Hz case.
4. Held-out: epsilon=1/100000 s with otherwise unchanged parameters, and a high-rate 10,000-Hz camera with 0.01-ms exposure. Also reject `H<=2(b-c)/V` for a positive below-c dwell.
5. Nuisance controls: all calculations are *ideal scalar aperture*, not camera images. No shutter/clock/row/brightness/blur/gaze/glasses/geometry/missingness calibration is assumed. No inference from absent high-speed witness to absence of closure.

## Consequence to preserve regardless of outcome

A reference-camera full-exposure sensitivity guarantee requires an **independently established minimum continuous closure dwell** or another quantitative exposure/measurement detection model. A hard speed ceiling plus open endpoints supplies only a minimum excursion time, not a minimum closed dwell. The human study must not label reference non-observation as a verified negative. Keep `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. No new source archaeology or S01 proxy tuning. Hush remains separate.
