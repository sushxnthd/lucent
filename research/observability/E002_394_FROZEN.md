# E002-394 — frozen real-human dual-clock and virtual-shutter falsification (2026-10-23)

## Question and evidence boundary
E002-393B verified one CC0 human high-speed recording and a 1-kHz EEG synchronization stream but failed the predeclared 150±1 fps active-rate prediction (152.22 fps). Before inspecting the `PhanTime` values, freeze an independent dual-clock test. No pixel measurement or EEG marker is a calibrated physical aperture.

## Frozen tests (do not modify after inspecting data)
1. Parse `PhanTime` *independently* of EEG `Time` and AVI FPS. Accept numeric seconds, parseable clock timestamps, or explicit HH:MM:SS timecodes; if ambiguous, reject camera-clock qualification rather than choose a favorable unit. Report parser choice, parse fraction, nonmonotonic count, and camera-clock slope.
2. On adjacent frames without gaps >20 ms in EEG time, compare EEG and Phantom inter-frame timing. Prediction: at least 95% of inter-clock residuals after robust constant-offset removal are within 2 ms. Report failure if no independent Phantom clock is recoverable.
3. Compute gap-aware frame rate and pause counts under EEG thresholds 15, 20, 30 and 50 ms. Prediction: the active rate stays within 1.0 fps across thresholds; if not, invalidate the unqualified 152.22-fps figure. Report *all* rates and gap counts.
4. Evaluate temporal marker capture under *hypothetical instantaneous-event markers* at 30, 60 and 120 Hz, exposure widths 1, 5 and 10 ms, across 100 predetermined uniformly spaced sampling phases. Prediction: capture fractions are approximately exposure duty cycle when averaging phases (absolute deviation <=0.03); report per-phase minima/maxima and event counts. This measures event-timestamp coverage ONLY, not physical blink detection. Missing/paused video coverage is excluded and counted.
5. Explicitly test that a naive 1-fps AVI interpretation fails against sidecar frame IDs and that the published 150-fps figure cannot be accepted as an independently measured acquisition clock without reconciliation.

## Precommitted failure policy
Do not silently convert clocks, interpolate across gaps, infer physical aperture or closure duration, or use EEG pulses as blink-duration labels. Any ambiguous clock or nuisance requires `ABSTAIN_UNCALIBRATED`. Keep original E002-392/393 negative results. Use untouched participant/device holdouts for any future physical certificate. No identifiable video is committed.

## Reproduction
Run `e002_394_dual_clock.py --archive S01.zip --output out/` against the MD5-verified source, produce machine-readable aggregate results, and run a separate checker with independent calculations. The script must fail on source-hash mismatch and missing sync fields. Hosted CI must download the original public archive and verify its MD5.
