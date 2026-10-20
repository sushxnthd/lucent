# E002-335 — Frozen human annotation decimation protocol
Frozen: 2026-10-21 04:xx IST, before full EyeBlink8 annotation extraction. Source: Fogelton et al. EyeBlink8; accessible GitHub mirror gbonesso/recon_loc_caract_faces, branch main. Mirrored tags are human-annotated native RGB videos, NOT independent high-speed ocular reference. This is a **human annotation proxy experiment**, not an independent physiology validation.

## Active question (10 requirements)
1. Signal/reference: deterministic 30-to-10-fps frame-index decimation of annotated RGB frames vs native manual blink-interval and 90–100%-closed eye labels.
2. Literature: Fogelton & Benesova CVIU 2016/2018, Soukupova & Cech 2016, recent blink temporal models; sampling theorem not new.
3. Metric: per-event survival across all 3 decimation phases; fully closed event survival, conditional on clean/visible annotation, plus loss by event duration, glasses and non-frontal/occlusion.
4. Main confound: blink annotations are themselves read from RGB, and native frame times/exposure are unverified; cannot establish unseen sub-frame events.
5. Generative model: latent binary blink occupancy b(t); RGB shutter samples integrate a photometric/geometry-transformed b(t); manual frame labels L[n] are annotations of recorded frames, with annotator error. 10-fps derived samples are L[3k+phi], phi in {0,1,2}.
6. Falsification: if a contiguous length-3 run of positive native labels is missed by any phase under complete indexing, implementation/model fails. Any inference about unseen between-frame blinks from labels alone is invalid.
7. Mechanism-derived boundary: for a contiguous run of L positive native frames, survival across phases = min(L,3)/3. In particular L=1 gives 1/3, L=2 gives 2/3, L>=3 gives 1. Noncontiguous positives use the count of represented residues modulo 3. No performance numbers were inspected before this prediction.
8. Untouched holdout: clip 11 (annotated glasses YES), reserved from exploratory model choice; process after remaining clips. Report as holdout only for combinatorial boundary, not participant/device generalization. Other clips are observational, no fitted black-box model.
9. Publication threshold: independent synchronized human reference (ideally >=100Hz), untouched participant/device and lighting/glasses holdout, calibrated exposure/noise, quantitative nuisance controls, preregistered prediction and independent replication. These tags alone fail threshold.
10. Product: reject blink-completeness guarantees from 10-Hz pipeline if native full-closure labels can be phase-aliased; preserve native frames, timestamps and abstain for short closure; do not claim 5-second fatigue diagnosis.

## Frozen parsing and analysis
Parse rows of the form frameID:blinkID:NF:LE_FC:LE_NV:RE_FC:RE_NV:... from .tag, ignoring header and trailer. A blink event is each maximal contiguous run of a nonnegative blink ID; if IDs are noncontiguous, treat runs separately. Clean frame iff NF=X and both NV=X. Event detection at phase phi if a retained frame belongs to its run and is clean. Closure evidence at phase phi iff a retained frame has either LE_FC=C or RE_FC=C and is clean. Closure-eligible event iff at least one native clean C frame. Report all events and clean-only subsets, and full-closure-positive event losses for all three phases. Report no human time in milliseconds unless original acquisition timestamps independently verified. Frame-index nominal 30Hz / 10Hz only.

Controls: geometry-only (blinkID), closure-only (FC), missingness-only (NV/NF), and temporal-smoothness-only (run length). Report uncertainty as descriptive counts, no pseudo-confidence from phase replicates. No training or threshold tuning on clip 11.

Precommitted holdout prediction: any contiguous clean FC-positive run of length >=3 frames is guaranteed observed at all three 10Hz phases; length 1 observed at exactly one phase; length 2 at exactly two. A violation is a failed gate, not a discovered physiological effect.

## Provenance and failure handling
Mirror may omit some source files; log skipped files and their Git blob SHA. Do not silently fill absent annotations or infer timebase. After two blocked attempts, pivot to exact instrument model / alternative accessible dataset. Do not use local laptop.