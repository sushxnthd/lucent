# E002-224 frozen protocol

Question: Does EOTT supply an independently calibrated RGB exposure-to-Tobii timebase?
Pair: webcam eye-image sequence vs same-eye native Tobii pupil diameter.
Metrics: source PTS uniqueness, independent clock anchor (yes/no), native five-second pupil p95-p05 range.
Confound: browser event time is not physical exposure time.
Falsification: independent exposure clock anchor would remove the ambiguity.
Scientific threshold: eight untouched participants, frozen waveform and nuisance gates, independent checker, holdouts.
Product threshold: 75% prospective accepted windows; no fatigue inference.
Kill: switch source after two blocked EOTT timing attempts.
Execute existing E002-222 audit without changing its calculations. No waveform correlation or lag claim.
SCIENCE: timing-source admission only.
PRODUCT: reject lag certification if anchor unverified.
