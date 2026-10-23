# E002-398 — prospective blinded eyelid-aperture annotation handoff (frozen 2026-10-23)

## Purpose and evidence boundary
E002-371 cannot be tested on EEG blink timestamps or optical-flow event AUCs: neither measures physical upper/lower eyelid separation. E002-395–397 demonstrated real participant and optical-nuisance failures. This experiment constructs an independently auditable **blinded human-annotation instrument**, not a new proxy classifier. Reuse already verified S01 and S19 Eye-BCI Phantom videos; both were previously inspected, so neither is a genuine untouched participant holdout. Do not claim this study validates E002-371 until independent aperture annotations and actual camera exposure/velocity calibration exist.

## Fixed source, selection and blinding
Use source S01 MD5 `fef02cb7ebf62e4f3efb6303284fd6cb` and S19 MD5 `8a16cf12526f7558b4e49926c4bc5e8e`. Use the fixed E002-397 EEG-marker/control pair selection with no feature/threshold tuning. From each participant's ordered eligible pairs choose exactly 20 pair indices `floor((i+0.5)*N/20)` for i=0..19. For each pair, include both clips of 7 consecutive video frames, centered on the selected event/control frame. Do not reveal event/control labels to annotators. Crop each 320x288 frame to x=70:260, y=90:220, without geometric interpolation or photometric modification; PNG lossless, no identifying full face. Randomize 40 clip identifiers per participant using SHA256(seed `lucent-e002-398-blind-v1`, participant, index, arm) truncated to 16 hexadecimal characters; verify no collisions. A private linkage file containing event/control and absolute source timestamps must NEVER be uploaded to public GitHub, CI artifacts or paper supplementary materials.

## Frozen instrument checks
C1: each verified source yields 40 clips and 280 cropped PNG frames, exactly 20 event/control pairs.
C2: no source frame IDs, marker labels, person names or timestamps appear in public-safe filenames or annotation sheet; source mapping remains in private linkage.
C3: every PNG decodes to 190x130 pixels, hashes match the manifest, and seven consecutive frames exist per clip.
C4: record per-clip empirical sharpness (variance of Laplacian), saturation fraction and grayscale p95-p05 contrast as descriptive annotation-quality signals; do not retrospectively optimize quality thresholds or discard difficult clips.
C5: produce a deterministic anonymized manifest and a blank annotation sheet. Do not upload actual human frames by default.

## Human study / reference requirements
Two independent raters, blinded to EEG event/control and to all derived classifier scores, should place three paired upper/lower eyelid margin landmarks at left/central/right iris-aligned columns on each frame. Raters flag gaze occlusion, glare, glasses, blur, missing landmarks and unresolvable margins; never impute missing coordinates. Define central aperture as Euclidean upper-to-lower margin distance in pixels, normalized by a **separately calibrated** geometric reference. Record both raters, disagreement, adjudication and interval uncertainty; use unresolved rather than false negative when a high-speed reference cannot resolve a threshold excursion. Camera exposure duration, true frame timestamps, shutter type, optical mapping and independently measured upper velocity bound must be documented before any hard E002-371 no-hidden-closure claim. 152-fps effective event timestamps do not establish these quantities.

For a true prospective test, freeze velocity/optical/timing uncertainty envelopes on disjoint calibration participants and predict which 30/60-Hz ordinary-camera gaps are certifiable on untouched participants/devices. A certificate is scored incorrect if blinded reference uncertainty permits a crossing that the certificate excludes; unresolved references are not scored as negatives. Include nuisance interventions (brightness, geometry, gaze, glasses, blur, missingness, rolling shutter, clock drift), paired camera exposures and an independent analyst. Report selective risk with confidence bounds and abstention rate, not just AUC.

## Release gate
Until independently validated physical aperture and kinematics exist, all hidden-closure, blink-duration, PERCLOS and fatigue claims stay `ABSTAIN_UNCALIBRATED`. A completed annotation pack is an enabling human-validation artifact, not a validated boundary law.
