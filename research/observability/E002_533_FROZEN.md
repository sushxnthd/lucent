# E002-533 FROZEN | Real-codec photometric falsification of E002-532

2026-10-30. Existing Lucent E002-371 research branch and draft PR #26. This is a **synthetic optical scene passed through actual video encoders/decoders**, not a physical camera or human study. Protocol frozen before executable or results. No subject images.

## Question
Does E002-532's exact LED-duty-fraction calibration survive the **actual codec/quantization/ROI-extraction pipeline**, and does an independently unmeasured camera response nonlinearity invalidate the inferred shutter parameters? This tests an instrument **assumption**, not the eyelid-velocity theorem. It must not promote nominal video PTS to sensor timing.

## Frozen design
Reuse the 40 E002-532 LED pulse intervals, 20 nominal 10-ms frames, 3 ROI row coordinates 0,2,4, training frames 0..9 and held-out frames 10..19, true parameters (delta=1 ms, exposure=2 ms, row delay=0.5 ms/row-unit), 36-candidate grid and tolerance 1/50. Render 20 synthetic RGB frames, 96x96, with three grayscale patches at x=24..71, y=8..19 / 40..51 / 72..83. Every patch's **linear irradiance** is the exact E002-532 duty fraction. Round to 8-bit intensity; reserve dark and bright reference patches at x=0..11 and 84..95 to check normalization. No subject content. Feed the frames through real ffmpeg FFV1 lossless AVI and H.264/yuv420p CRF=23 MP4 at nominal 100 fps. Extract the central 24x8 region of each ROI by OpenCV after decoding. Compare measured patch means after per-frame dark/bright normalization with the exact-rational model. Record ffmpeg and OpenCV versions and encoded SHA256.

## Frozen adversaries
1. **Lossless linear**: train grid fit is unique and held-out maximum brightness residual <=1/50.
2. **H.264 linear**: same unique fit and held-out tolerance <=1/50. If it fails, preserve failure; no codec retuning.
3. **H.264 nonlinear**: render intensity as round(255 * irradiance^(1/2.2)), but **do not** invert gamma in the evaluator. Predict a training model falsification or held-out failure, not a valid unique physical certificate. If a unique fit survives both sets, report this prediction as falsified and explicitly assess false confidence.
4. **H.264 nonlinear with independently specified inverse gamma**: invert using fixed exponent 2.2 on normalized decoded brightness before fitting. Predict recovery of the true candidate within tolerance, subject to 8-bit/codec error; preserve any failure.
5. **Held-out spatial glare**: overwrite the central ROI patch of row=2, frame=15 to full white **after** linear rendering but before encoding. Predict held-out falsification with frozen training candidate unchanged. Do not mask or omit the corrupted observation.
6. **Missing native ROI**: explicitly mark row=2, frame=15 invalid; no imputation. Predict held-out count 29 and missing count 1. This is censoring, not successful measurement of that row.

## Acceptance, kill and interpretation
- The executable must use actual ffmpeg encode/decode; purely numeric E002-532 replay is not sufficient. Keep the exact original candidate grid; do not fit gamma or tune tolerances on holdout.
- Report all conditions, observed brightness residuals, candidate count, fit and failure. Separate model falsification from uncertainty/ambiguous fit. Reject any condition that fails the preregistered threshold.
- Passing a synthetic encoded scene only supports codec-pipeline feasibility **under known rendering/photometric response**. It cannot certify physical exposure, rolling readout, photodiode timing, cross-camera transport, human closure or speed ceilings. No data-derived physical calibration is allowed; ABSTAIN_UNCALIBRATED and BLOCKED remain mandatory.
- If a camera-like nuisance passes despite a wrong model, this is an important **false-confidence failure**; preserve and flag it, rather than calling it robust.
- Independent verification: a separate NumPy/OpenCV pixel extractor or a second decoder/implementation where feasible; tests must exercise negative controls and fail-closed outputs.

## Next empirical gate
Actual photodiode-timed LED capture and blinded S01 anatomical reviews remain required. This synthetic encoded-instrument experiment is the last acceptable bridge only if it reveals a concrete product/instrument consequence. No more grid-theorem polishing without physical data.
