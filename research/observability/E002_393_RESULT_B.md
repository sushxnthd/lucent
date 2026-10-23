# E002-393B — first synchronized real-human blink reference: gap-aware timing and marker alignment (2026-10-23)

**Evidence tier:** independently recorded human eye-region video plus 1-kHz EEG/experiment synchronization; verified public CC0 source and reproducible hosted CI. **Not** a physically calibrated aperture reference, held-out evaluation, or clinical result.

## Acquisition and reproducibility
- Source: Guttmann-Flury, Sheng and Zhu, *Scientific Data* 12:587 (2025), DOI 10.1038/s41597-025-04861-9, CC0 Zenodo mirror 18978288, S01.zip. Source archive MD5 `fef02cb7ebf62e4f3efb6303284fd6cb` verified on each acquisition.
- Reproduced successfully in GitHub Actions run https://github.com/sushxnthd/lucent/actions/runs/39955263954 .
- **53,680** decoded 320×288 human eye frames; **414,720** 1-ms synchronization rows; **53,680** consecutive, distinct Phantom frame identifiers (166–53,845). AVI metadata says **1 fps**, not the acquisition cadence.
- Camera coverage in EEG clock: **18.829 to 403.982 s**. Unsegmented frame-ID slope: **139.3706 fps**, biased downward by **116 pauses** exceeding 20 ms, totaling **33.269 s** (maximum 0.872 s).
- After removing pauses >20 ms, the observed active-frame rate is **152.2178 fps** (53,563 frame steps over 351.884 s). This **fails** the frozen prediction of agreement within 1 fps of the paper's 150-fps figure; the mirror's ~500-fps prose is also unsupported. Frame interarrival times are primarily 6 and 7 ms because the EEG clock has 1-ms resolution. The 20-ms gap cutoff is exploratory and must be sensitivity-tested; camera's embedded `PhanTime` requires independent reconciliation.
- **112** isolated positive EEG blink markers. **12** are outside the camera recording interval and **7** fall in video gaps; **93** can be aligned to a camera frame within 10 ms. These are not physical closure-duration labels.

## First real human blink alignment
Using the **first six chronologically separated, in-coverage markers** (selection frozen before image inspection), the mapped Phantom IDs are **758, 1249, 1667, 2610, 3284, 4045**. The corresponding AVI indices are **592, 1083, 1501, 2444, 3118, 3879** (fixed 166-frame ID offset). Nearest-frame EEG-clock residuals are **0, -2, -3, +3, 0, +2 ms**.

A technical contact sheet of each event at `frame−15`, `frame`, `frame+15` shows eyelid closure or marked narrowing around these markers, including fully closed-looking frames. **This is qualitative, unblinded, single-participant evidence**, not threshold-calibrated aperture measurements or a validated sensitivity/specificity estimate. No face footage was committed to Git.

## Failed predictions preserved
- The E002-392 preregistered claim that AVI ffprobe would show ~150 fps failed: AVI says 1 fps.
- The E002-393 unsegmented cross-clock ~150-fps prediction failed: 139.3706 fps due to 116 camera gaps.
- The gap-aware active-rate near-150 within 1 fps prediction also failed: 152.2178 fps.
- The first six raw chronological EEG markers preceded camera start; the initial event sheet mapped all six to the first frame and was **invalidated**. Corrected alignment excludes out-of-coverage markers.

## Product and scientific boundary
The evidence validates an **instrument and synchronization pipeline on one real human recording**. It does **not** validate E002-371's physical no-hidden-closure bound. Without exposure start/end, physical aperture, independent physiological velocity envelope, optical calibration and unseen participants/devices, Lucent must issue `ABSTAIN_UNCALIBRATED`. A 1-kHz synchronization clock also limits submillisecond timing claims.

## Next decisive experiment
Parse camera `PhanTime` independently from the same sidecar/XML and reconcile the 152.22-fps active rate with embedded camera timestamps and 150-fps publication claim. Then freeze a **held-out participant** experiment using independently labeled aperture traces, virtual 30/60-fps exposure integration and conservative reference-unresolved labels. Do not train thresholds on these six exploratory examples.
