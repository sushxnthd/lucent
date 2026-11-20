# E002-467 — FROZEN independent human-video validation handoff
Date: 2026-10-26. Frozen before any E002-467 implementation or dataset inspection. Evidence tier: prospective protocol, **not empirical validation**.

## Newly verified acquisition resources
1. Guttmann-Flury, Sheng & Zhu, *Scientific Data* 12:587 (2025), DOI 10.1038/s41597-025-04861-9; original CC0 Synapse dataset DOI 10.7303/syn64005218 (syn64005218). **31 subjects, 63 sessions, 150-fps monocular Phantom Miro M310 video, 300-Hz eye tracking, 1-kHz EEG/EOG/EMG.** Video timestamps and blink peak flags exist, but **shutter integration and anatomical aperture calibration are not independently authenticated**. Paper documents unsynchronized video trials P3004L101 and ME181 and other missing segments. This is a viable *human image-level positive-candidate* source, not a continuous anatomical reference.
2. Clites, Kim & Rootman, *FaceBase* (2026), DOI 10.25550/88-28BJ. **Eight adults; 400-fps 3D eyelid-margin markers; five eyelid behaviors; hardware-synchronized EMG.** Access is **restricted**, General Research Use / Not-for-profit only, with a signed access process. The dataset cannot be treated as acquired. A 400-fps marker trajectory is still not continuous ground truth.
3. Kim et al., *PNAS* (2025), DOI 10.1073/pnas.2508058122, associated primary physiology study. 240-fps human videos in Lee et al., *Biomedical Engineering Letters* (2025), DOI 10.1007/s13534-025-00522-3, are contextual literature, not independent verified raw trajectories.

## Primary frozen question
For E002-371, do independently estimated closing/opening speed bounds and independently authenticated shutter/geometry assumptions exclude threshold crossings on unseen human sequences? **Only an independently timed physical witness inside a claimed excluded gap falsifies the joint claim.** Open frames alone never establish negative anatomical ground truth.

## Data lock, splits, and decisions
- Primary accessible analysis: Eye-BCI, all 31 subject aliases S01–S31; allocate 23 calibration and 8 held-out subjects using lexicographically sorted SHA-256 of the literal UTF-8 string `lucent-e002-467-v1|SXX`; lowest 23 hashes are calibration. All sessions of one subject remain together. Do not change assignment or threshold after opening holdout.
- No images or subject-level measurements enter the repo. Preserve original source identifiers, SHA-256 checksums and permission records in private acquisition manifest. Public aggregate only.
- Frame-level preregistered outcomes: `IMAGE_SUBTHRESHOLD_CANDIDATE` only when aperture upper uncertainty endpoint is strictly below threshold, image quality and annotation adjudication pass; otherwise `UNRESOLVED`. Even a candidate is **not** an anatomical crossing certificate. Unverified shutter/geometry/clock/gain means `ABSTAIN_UNCALIBRATED` for physical decisions.
- Independently verify frame rate from monotonically increasing per-frame timestamps, not nominal FPS or container metadata. A skipped frame, non-monotonic timestamp, unresolved synchrony, absent calibration, glasses glare, gaze change, occlusion, focus/blur, rolling-row timing or disagreement must be counted as unresolved. Do not fill gaps with interpolation to manufacture labels.
- Calibration: estimate empirical speed distributions and stratified error with per-subject cluster units. Sample maxima are **not hard physiological caps**. Freeze a separately justified bounded-speed hypothesis and error set before evaluating holdout. No tuning on held-out outcomes.
- Test predictions for ordinary-camera target rates 30/60/240 fps only if exposure integration and time mapping are independently authenticated. Without this, report image-level sensitivity/coverage, not physical closure exclusions.
- One robust held-out independent crossing witness in a claimed excluded interval => falsify that restricted joint assumption; unresolved intervals and zero witnesses do not establish correctness. Report coverage/abstention, positive witnesses, missingness and per-condition failures with participant-disjoint uncertainty.
- Do not reuse the previous 17-person E002-457/459 dataset for this test. Do not call the Eye-BCI 150-fps camera a 300-fps camera: the **eye tracker** is 300 Hz, the **video** is 150 fps.

## Implementation deliverable and stop rule
Build an executable ingestion/validation gate for independently annotated frame-aperture CSVs with strict subject isolation, timestamp/gap rejection, uncertainty and nuisance flags. Run adversarial synthetic fixture tests to prove no unsupported physical claim can emerge. Real video access/annotation is a separate explicit gate. If unavailable, publish the acquisition manifest template and do not continue synthetic theorem polishing.

No physical or medical product claim. E002-371 remains unvalidated. `ABSTAIN_UNCALIBRATED`. PR #26 stays draft; S21/S22 sealed; Hush PR #45 separate.
