# E002-273 — AFFEC v2 primary-source modality lineage audit

## Decisive provenance result
AFFEC v2's author-maintained README describes the *videostream* modality as 40-Hz, >200-channel derived face landmarks/gaze/action-unit features, stored as JSON sidecars and TSV.gz matrices, not verified RGB eye frames. The upstream v2 archive-builder docstring describes collecting these derived files; its actual glob `sub-*/beh/*_recording-videostream_physio.*` is **extension-unrestricted**. An independent synthetic fixture confirms it would also collect a hypothetical matching MP4. Therefore, source inspection supports **not admitting AFFEC for raw RGB waveform certification** but DOES NOT prove that the 8.9-GB archive contains no image/video bytes. A central-directory inventory remains necessary for definitive absence.

The same README documents **91 repaired JSON sidecars across 24 subjects**, including **22 forced surrogate-template repairs**. Treat these as data-schema provenance risks, not evidence of physiological failure.

## SCIENCE ledger
**Question:** Does a documented 40-Hz videostream contain directly observable ordinary RGB pupil boundary pixels synchronized to same-eye 149-Hz pupil diameter?
**Finding:** No such raw-pixel stream is established by the primary source. Feature-only measurements are not equivalent to independent RGB waveform recovery. Archive byte membership, exposure timing and same-eye pairing remain unverified.
**Limitations:** This is a primary-source lineage audit plus synthetic glob test, NOT a human experiment or impossibility theorem.

## PRODUCT ledger
**Decision:** Deprioritize AFFEC for Lucent's *raw RGB* measurement kernel until direct image bytes, per-frame exposure timestamps and trustworthy same-eye reference synchronization are demonstrated. Do not mislabel derived facial features as original camera images. Switch to the EVE Basler positive-control access path or verify Zenodo 17046553 RAR (10 Tobii/webcam participants) before further feature-only experiments.

## Frozen active kernel
- Signal/reference: visible RGB pupil/iris apparent radius waveform vs native-time same-eye eye-tracker pupil diameter.
- Best-known frontier: EVE Basler 60-Hz visible-color stream has documented synchronization but gated access; EyeDentify labels are temporally folded; EOTT blink-validity clock failed; AFFEC v2 documented as feature stream.
- Scalar observability: lower confidence bound on participant-held-out within-window Pearson r; jointly require lag <= 67 ms, amplitude ratio 0.75–1.25, NRMSE <= 0.70.
- Strongest confound: optical entrance-pupil magnification, illumination-dependent contour extraction, gaze geometry and exposure-clock alignment.
- Decisive falsification: prospective RGB-only admitted windows fail frozen gates or are no better than photometric/geometry-only controls.
- Publishable success: >=8 untouched participants, independent checker, same-eye timestamp proof, participant/device/lighting/glasses holdouts, mechanism-derived unseen boundary.
- Product relevance: >=75% of admitted windows meet all gates with >=50% RGB-only admission coverage; no reference-dependent filtering.
- Kill/reformulate: three non-discriminating runs or no feasible calibrated admission under human holdouts. A data-path access failure is NOT physiological falsification.

## Provenance, results and negative gates
- Pinned upstream commit `f1759103f501282a41a04d6b474a3e89d6f36a6b`; source Git blob IDs in DATASET_MANIFEST.json.
- Publisher MD5 for `videostream.zip`: `b7efc90ca02bc4e571fa90fe2634f0f4` (not downloaded or verified).
- `python3 research/e002-273/audit.py` runs offline mock wildcard test and writes RESULTS.json; `--online` verifies upstream Git blob SHA-1s; `python3 research/e002-273/independent_check.py` verifies fail-closed result and mutations.
- Offline synthetic wildcard test and checker passed. Upstream bytes inspected via connected GitHub source reads, not replayed by the script locally; remote Actions execution pending.
- Failed gates: no verified RGB frames, no verified raw archive hash or member inventory, no clock, no human waveform, no device/lighting/glasses holdout.
- Wildcard effort (~10%): hypothetical matching .mp4 passes the author's glob; **do not** turn a documentation-level absence into a categorical archive-impossibility claim.

## Next highest information-gain action
Directly inspect Zenodo 17046553's 75.2 MB RAR members, verify publisher MD5, locate original webcam frames and native-time Tobii samples. If not present, switch to EVE access and stop wasting effort on unpaired datasets. Keep five-second fatigue inference frozen.
