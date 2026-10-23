# E002-392: frozen public-human video feasibility protocol (2026-10-23)

## Primary scientific target
Move E002-371 from synthetic theory to an empirical *human reference* test without conflating high-speed reference video with physical aperture truth. Preserve the one Lucent kernel, branch `research/observability-human-boundary`, and draft PR #25.

## Previously unseen public source
Guttmann-Flury, Sheng & Zhu, *Scientific Data* 12:587 (2025), DOI 10.1038/s41597-025-04861-9; CC0 Eye-BCI data, Synapse syn64005218. Independent MOABB/Zenodo mirror, DOI 10.5281/zenodo.18978288, `S01.zip` (406,561,464 bytes, md5 fef02cb7ebf62e4f3efb6303284fd6cb). The primary paper explicitly says video recorded at **150 fps** with triggers every ~6.6 ms; the mirror description says **~500 fps**. Treat this as a metadata conflict. **Do not silently choose the more favorable rate.** Read actual ffprobe rate, video frame timestamps and sync file; no certificate unless calibrated exposure and clock uncertainty exist. This source is human eye-region video, not synchronized 30-fps RGB plus calibrated physical-aperture ground truth.

## Precommitted test sequence (before fetching frames)
1. Fetch only S01.zip and extract the first `*_phantom.avi` (one human participant), plus same-session XML and synchronization CSV if present. Verify archive MD5. If access fails, preserve error as a negative result; do not silently replace with unrelated data.
2. Inspect ffprobe avg/r_frame_rate, duration, number of frames and packet timestamps. Predict paper-consistent rate near 150 Hz, but **report a failure** if not within 1 Hz. The mirror's 500-fps claim is not independent verification. Report variable or missing timestamps.
3. Produce three contact sheets and a low-level ROI motion/contrast trace on three disjoint 8-s segments at 15%, 50%, 80% of duration. This is **exploratory human imagery**, not an aperture trace. Never interpret pixel darkness or motion energy as a closure without manual adjudication.
4. Independently test a temporal-coverage lemma on discrete **human reference-frame annotations** only after validated annotations exist: an event with continuous closed interval duration at least `1/f_low` cannot be missed by instantaneous uniform sampling at rate `f_low`, for any phase. For shorter events, construct an admissible missed phase. Exposure blur, label uncertainty, clock uncertainty and RGB transfer invalidate this as a real camera certificate unless separately bounded.
5. **No data leakage:** freeze all thresholds and split rules before scoring; this run is exploratory instrument characterization, not confirmatory held-out evaluation. No human reliability numbers from a single participant. Do not use the test video to estimate an allegedly independent physiological speed upper bound.
6. Output a small reproducible artifact with manifest, hash, actual timing, sampling diagnostics, contact sheets, exploratory motion trace, and explicit abstention policy. Do not commit or redistribute identifiable human imagery into Git; CI artifacts are restricted to this technical validation workflow and should be removed if licensing/consent issues arise.

## Falsification and product gates
- Any discrepancy between acquisition claims, frame metadata and actual time stamps blocks deterministic certificates.
- Any absent exposure start/end, shutter transfer, physical aperture calibration or independently justified velocity upper bound => `ABSTAIN_UNCALIBRATED`.
- A 150-Hz human recording is a potentially useful exploratory reference, not sufficient ground truth for submillisecond crossings or a 5-second fatigue diagnosis.
- No unconditional blink reconstruction, PERCLOS, clinical or fatigue claims. External review remains required.
