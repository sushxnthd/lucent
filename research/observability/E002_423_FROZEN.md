# E002-423 — frozen pulse-calibration falsification protocol

Date: 2026-10-25. Preregistered before implementation or simulated outcomes. This is an **instrument simulation**, not a physical camera, LED, photodiode or human measurement.

## Motivation and model
E002-421/422 assume a known, uniform shutter and correct center times. Nominal frame rate alone does not establish exposure duration, rolling-row delay, synchronization, gain linearity, or clock jitter. A temporally commanded short LED pulse of width `p` starting at phase `s` produces ideal normalized intensity `y = length([s,s+p] intersection [c-E/2,c+E/2])/E` for a linear boxcar shutter of width `E` and row-specific center `c`. The experiment is a synthetic identifiability/diagnostic test of this acquisition model, not a claim that real sensors satisfy it.

## Frozen experiment
- Pulse width 0.50 ms, phases from -3.0 to +7.0 ms in 0.10-ms increments. Separate two rows at indices 0 and 800. Fit independently using only every other phase (training); reserve interleaved phases for unseen-phase validation.
- Hidden synthetic truth: exposure width 2.40 ms, center 0.00 ms at row 0, center 3.20 ms at row 800, and seeded bounded pixel noise of amplitude at most 0.003.
- Fit each row by exhaustive boxcar overlap search on a grid of `E` from 1.50 to 3.30 ms and `c` from -0.50 to 4.00 ms in increments of 0.10 ms; no access to truth inside the fitter. Report training/held-out RMSE and row-center displacement. Use independently implemented continuous overlap as the synthetic generator, not the fitter's function.
- H1: both row exposures recover within 0.11 ms of true E; centers within 0.11 ms of truth; held-out RMSE <= 0.015. The shared-center global-shutter hypothesis must fail at least one row by >= 0.50 ms.
- H2: adversarial independently seeded per-pulse timing jitter uniformly in [-0.80,+0.80] ms must fail held-out RMSE <= 0.015 on at least one row, **or** if not, report a counterexample to this diagnostic (do not retune thresholds).
- H3: gamma-nonlinear camera response `sqrt(y)` must fail the same held-out RMSE gate on at least one row, or preserve negative result.
- H4: shuffled phase-to-observation pairing must fail, or preserve negative result.
- H5: missing phase tags, unverified photodiode reference, saturated intensity, unknown response curve, or unverified rolling-row clock must prevent any *physical* calibration claim regardless of synthetic fit.
- H6: synthetic fit must never unlock E002-371 product certificates; output `ABSTAIN_UNCALIBRATED` and an explicit evidence tier.
- Reproducible independent tests must check the exact overlap integral, fit recovery, adversarial outcomes, and malformed input.

## Real-world study required after this substitute
Use a pulse generator synchronized to a traceable timebase, LED + independent photodiode/oscilloscope to verify optical pulse edges, static uniform panel, RAW linear image intensities, dark/flat calibration, independently measured frame and row timestamps, 3+ rows and multiple exposure settings. Randomize commanded phase, use unseen phase sequences and repeat across devices/temperatures/brightness. Keep any saturation, PWM, HDR, rolling exposure, phase jitter, clipping, automatic gain or nonlinear transfer as model failure until independently bounded. Store hardware traces and hashes privately; publish license-compatible derived measurements and uncertainty intervals only. This synthetic exercise does **not** authenticate a hard human eyelid velocity bound or human landmark truth.

## Prior art and novelty boundary
LED-based shutter and rolling-shutter calibration is established: Huai et al. (2023), Optics Letters DOI 10.1364/OL.474375; Kurosawa et al. (2024), J. Forensic Sci. Tech. DOI 10.3408/jafst.875; review in Sensors (2022) DOI 10.3390/s22051871. This is an engineering falsification gate, not a new general method. Product remains `ABSTAIN_UNCALIBRATED`.
