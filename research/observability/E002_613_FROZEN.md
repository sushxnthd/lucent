# E002-613 | Frozen one-sided human velocity-cap falsification protocol

Date: 2026-11-02. Parent: E002-371, E002-609, E002-612. Branch: `research/observability-human-boundary`; draft PR #26. Evidence tier: **prospective instrument, no new human observations**.

## Specific scientific question
E002-371's no-hidden-closure certificate assumes an independently defensible **hard continuous-time aperture-speed ceiling**. E002-612 established that a finite sample cannot prove such a ceiling. Can high-rate, independently calibrated human eyelid trajectories nevertheless **falsify** a proposed ceiling without making an unverified acceleration assumption? Yes, conditionally, by a one-sided finite-difference lower bound. This is an elementary mean-value-theorem consequence, **not a novel theorem**. Its value is a prospectively testable, product-changing rejection rule.

For consecutive physical aperture observations `z0,z1` (mm), independent absolute error bounds `e0,e1` (mm), and a conservative **upper** bound `dt_max>0` (seconds) on elapsed true time, define

`L = max(0, abs(z1-z0)-e0-e1) / dt_max` (mm/s).

If `L > V_claim`, then every differentiable continuous-time aperture trajectory consistent with the physical observation/error/time brackets has some time in that interval with `|a'(t)| > V_claim`. Thus the proposed ceiling is **incompatible with the stated measurement premises**. Equality does not contradict. If `L <= V_claim`, no certification follows: arbitrarily fast intersample motion remains possible. Missing independently bounded anatomy, time, geometry or nuisance => abstain. Use exact decimal/rational arithmetic.

## Frozen synthetic controls (not human data)
- `z0=8.0, z1=7.5, e0=e1=0.05 mm, dt_max=0.0025 s` => `L=160 mm/s`; claimed `150` contradicted; claimed `160` not contradicted.
- Widen `dt_max` to `0.003 s` => `L=133.333... mm/s`; claimed `150` no longer contradicted.
- Widen both errors to `0.25 mm` => `L=0`, no contradiction.
- Zero/negative time, negative errors/cap, NaN/Infinity, missing attestations, any nuisance, or mismatched physical units => abstain.
- Independent JavaScript BigInt rational implementation must reproduce boundary and monotonicity controls.

## New concrete human-data route and limits
**FaceBase / Clites Lab, released 2026-09-01:** *Eyelid Kinematics and Orbicularis Oculi Electromyography – Persons Without Facial Pathology*, DOI: https://doi.org/10.25550/88-28BJ . The associated 2025 PNAS study is https://doi.org/10.1073/pnas.2508058122 . Reported design: 8 adults; 3D upper/lower eyelid-margin markers sampled at 400 fps; simultaneous hardware-synchronized EMG; spontaneous, voluntary, reflexive, soft and forced closure. **Restricted-access human-subject data; access must be approved, non-profit/general research use only.** Do not download, redistribute, scrape around access controls or infer permission from a paper's supplementary movies. The published video supplements are visualizations, not authenticated raw eyelid trajectories.

Prospective preregistration **before data access**:
1. Obtain authorized access and actual acquisition/timestamp/marker/uncertainty documentation. No claim that nominal 400 fps equals exact 2.5-ms spacing. Resolve whether matched upper/lower marker pairs permit a calibrated *local palpebral aperture* in mm. If not, mark anatomical premise missing.
2. Freeze candidate `V_claim` values and their intended scope **independently of held-out data**. Published mean/peak speeds are descriptive, not hard ceilings. Assign participant-disjoint exploratory development/holdout; with only eight participants, report uncertainty without low-error-rate claims. Stratify by behavior; do not pool voluntary with spontaneous to assert transportability.
3. Derive conservative observation error from independent marker calibration/registration, 3D-to-aperture geometry and occlusion; conservative time upper bounds from measured synchronization/timestamps. Compute L on consecutive valid pairs. No interpolation across missing markers; abstain for blur, gaze geometry, occlusion, missingness, uncertain clocks, etc.
4. **Primary falsifier:** any independently verified held-out interval with `L>V_claim` invalidates that proposed ceiling for its asserted population/scope, conditional on calibration. A non-falsification is not evidence that the ceiling holds between samples.
5. Separately assess whether medial/central/lateral marker apertures disagree about a chosen closure threshold. If so, a single local aperture cannot automatically represent whole-eye closure. This is an anatomical model audit, not a clinical blink label.
6. Preserve participant-level outcome counts and precommitted thresholds; independent rater/adjudicator blinded to candidate cap. Do not upload raw faces, 3D markers, IDs, or restricted data to GitHub/CI. Report only licensed aggregates and code.

## Non-equivalence and product gate
The 400-fps 3D motion-capture dataset can **reject candidate velocity ceilings**; it does not by itself authenticate a consumer camera's exposure/rolling-shutter/clock, prove a universal velocity ceiling, or provide a physically co-recorded 30-fps shutter-gap test. E002-609 physical two-camera witness remains separately required. A contradiction => candidate ceiling rejected for stated scope and no E002-371 exclusion relying on it. No contradiction => **ABSTAIN_UNCALIBRATED**, not approval. All outputs: production BLOCKED pending external physical/human review.

Source record: https://trackhub.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/ (published 2026-09-01); https://pmc.ncbi.nlm.nih.gov/articles/PMC12358864/ .
