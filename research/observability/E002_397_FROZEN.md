# E002-397 — frozen motion-observability falsification on human video (2026-10-23)

**Frozen before evaluating this new optical-flow observable on either participant.** Continue the E002-371 kernel; do not create a new research branch. This is a prequalification test, not a physical-aperture validation. Earlier E002-395/396 results exposed a cross-person sign reversal and nuisance failure of a dark-pixel proxy. That proxy stays retired regardless of this result.

## Fixed human material and selection

Reuse the already-verified CC0 Eye-BCI SSVEP high-speed video and 1-kHz EEG synchronization: S01 (MD5 `fef02cb7ebf62e4f3efb6303284fd6cb`) and S19 (MD5 `8a16cf12526f7558b4e49926c4bc5e8e`) from Zenodo record 21905748. **Both participants were previously evaluated with a different image feature, so these are NOT untouched participant holdouts.** Do not search other recordings for a favorable result. Select the lexicographically first paired `*_phantom.avi` and `*_sync.csv` session per archive. For S01 exclude the six frames previously inspected in E002-393; S19 has no corresponding exclusion. EEG `Blinks>0` timestamps define *marker-associated* windows, not verified closure events. Apply the exact E002-395/396 frame-gap, ±3-frame event window, and ordered non-event-offset rules; require >=15 pairs per participant. Decode all video frames sequentially and check exact frame count.

## New fixed measurement, no training

Use OpenCV Farneback dense flow on each consecutive pair of grayscale frames, parameters `pyr_scale=.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.2, flags=0`. Estimate nuisance global displacement from the median horizontal and vertical flow over the union of top `[20:100,30:290]` and bottom `[200:270,30:290]` skin/background strips; subtract that vector from all flow. The eye region is fixed to `[118:190,100:230]`, exactly as in the failed proxy. Frame-pair score is the **80th percentile of residual-flow magnitude in the eye region**. Window score is the maximum across the seven consecutive flow pairs ending at frames `k-3,...,k+3`. Higher scores predict EEG marker windows. Do not optimize the ROI, percentile, aggregation, parameters or direction after inspection. This measures image motion, not eyelid aperture or closure.

For each frame before computing flow, apply the same transform consistently to both frames: clean; multiplicative gain 0.70; gain 1.30; Gaussian blur sigma 2; full-frame translation (+8,+6) with replicated border; and a fixed [145:175,130:205] white-glare rectangle. Report per-variant AUC from all event scores versus all control scores; never select only the favorable participant/variant. No threshold tuning or image publication. Mark the presence of any video timestamp gaps and use only contiguous windows.

## Frozen falsifiable predictions

- H1: clean event/control AUC >= 0.70 for **both** S01 and S19.
- H2: clean AUC >= 0.50 for **both**, i.e. no cross-participant sign reversal.
- H3: each participant's gain-0.70 and gain-1.30 AUC declines by <= 0.10 from its clean AUC.
- H4: each participant's translated AUC declines by <= 0.10 from its clean AUC.
- H5: each participant's glare AUC declines by <= 0.10 from its clean AUC.

All predictions may fail. An independent checker recomputes the rank-statistic AUC from anonymous score arrays and verifies the Boolean decisions. Report pair counts and all variants. Even if all pass, this does **not** establish E002-371 physical observability, actual exposure/clock, velocity, human threshold-crossing truth, participant/device generalization or publication novelty.

## Release consequence

If H1/H2 fail, reject this motion observable for event association. If nuisance hypotheses fail, restrict or reject it under the failed conditions. Even if H1–H5 pass, **product decision stays `ABSTAIN_UNCALIBRATED`** for closure duration, PERCLOS, no-hidden-closure and fatigue claims until blinded geometric aperture labels, independently measured exposure/clock and independently bounded eyelid speed exist. CI success is computational verification, never evidence that the scientific hypotheses succeeded.
