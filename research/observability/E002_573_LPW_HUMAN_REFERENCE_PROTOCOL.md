# E002-573 | LPW 95-Hz human-reference pilot: prospective, positive-only validation

**Frozen 2026-10-31 before any LPW frames or labels were inspected.** Kernel E002-371. This protocol supplements, and does not supersede, E002-567's physically synchronized shutter/photodiode study. No human physiological measurements are reported here.

## Why this source is a real advance over the unresolved S01 timebase

Primary source: Marc Tonsen, Xucong Zhang, Yusuke Sugano and Andreas Bulling, *Labelled Pupils in the Wild*, ETRA 2016, DOI [10.1145/2857491.2857520](https://doi.org/10.1145/2857491.2857520). [Institutional dataset page](https://www.mpi-inf.mpg.de/departments/computer-vision-and-machine-learning/research/gaze-based-human-computer-interaction/labelled-pupils-in-the-wild-lpw) and [official 2.4-GB archive](https://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip).

The original investigators describe **66 eye-region videos from 22 human participants, about 95 frames/s, ~130,856 frames**, with gaze, illumination, off-axis camera, glasses/contact lenses and makeup variation. This is a credible *reported acquisition rate* for a human reference-only pilot. It is **not** independently authenticated per-frame exposure timing, a calibrated 95-Hz reference sensitivity guarantee, or a human eyelid-aperture ground truth. The provided pupil-center/ellipse annotations are **not closure labels**. The official license limits the dataset to **non-commercial scientific research**; never redistribute images, videos or derived personal identifiers in this repository or public CI artifacts.

## Pre-registered question and falsifier

Can two independent blinded human anatomical raters identify **positive closed-eye frames** in native 95-fps human video that would be unobserved after a predeclared ordinary-rate temporal subsampling of the *same native frames*? A confirmed interior-positive native frame between two anatomically open subsampled endpoints is a **native-frame alias witness**, not an exposure-integrated 30-fps physical camera event.

**One-sided endpoint:** number of two-rater-confirmed interior CLOSED native frames between two independently OPEN low-rate endpoints, by participant and nuisance stratum. Also report all ambiguous/abstained windows and all source frames considered. A zero count is **not** evidence that hidden closure is impossible: a 95-fps reference can miss subframe events and neither shutter timing nor exposure integration is certified.

## Locked selection and blindness

1. Verify official archive SHA-256 at local acquisition and retain its exact URL, download date, license and raw video hashes in an owner-only immutable manifest. Do not assume that a video's container playback FPS is its independently measured exposure cadence. Extract native frame counts and presentation timestamps; reject duplicates, nonmonotonic timestamps, unreported dropped frames, unexpected dimensions and participant-ID ambiguity. These checks are eligibility, not proof of physical timing.
2. Enumerate source participants using the archive's actual documented identifiers, not assumed numeric filenames. Assign whole participants to DEVELOPMENT or HELD_OUT by sorting SHA-256(`E002-573-LPW-v1|participant_id`) lexicographically and taking the first 11 for development and the remaining 11 for holdout. Preserve exact IDs and hashes privately before viewing held-out labels. Do not select a split after inspecting blink frequency.
3. DEVELOPMENT may be used to tune the *annotation interface and abstention rubric only*. Freeze all landmark definitions, normalized aperture threshold, rater qualification, uncertainty floor, subsampling phase schedule and inclusion/exclusion rules **before** any HELD_OUT ratings. No model fitting or threshold selection on HELD_OUT.
4. To avoid cherry-picking blink-rich windows, enumerate every eligible held-out video and every complete non-overlapping 19-native-frame window from its first native frame. Assign deterministic pseudorandom priority SHA-256(`E002-573-window-v1|video_sha256|start_frame`); take the first 10 windows per held-out video for the initial feasibility pilot. Record how many windows are excluded by the cap, and never claim population blink prevalence from this case sample. If too few positive events are found, report insufficient positive opportunities and stop rather than tuning the selection on held-out labels.
5. Prepare two separate blinded 19-frame packets for **two actual different human raters**, with independent qualification, separate answer-key custody, private delivery, no source indices/candidate status/other-rater marks, immutable timestamped exports, and nuisance-specific abstentions. Do not substitute an AI or scripted JSON for human ratings. Use existing E002-497/E002-566 annotation and audit machinery where compatible; do not duplicate it.
6. After both exports are sealed, independently adjudicate CLOSED, OPEN and UNCERTAIN using a **pre-established strictly positive geometry/iris-scale uncertainty bound**. If this bound cannot be justified, only descriptive rater agreement is permissible, not a quantitative OPEN/CLOSED certificate. Keep rater disagreement as abstention, not a majority-imputed negative.
7. Construct 95-to-ordinary-frame **index-only** decimation using a frozen phase schedule (all integer phases for nominal 3:1 thinning, and 19-frame complete windows). Do not call this a simulated shutter exposure or true 30-fps capture. For each candidate interior positive, require two OPEN endpoints with no intervening retained CLOSED frame; count by participant and nuisance. Report per-phase outcomes without choosing a favorable phase.
8. For each positive alias witness, save source/video hash, private frame indices, blinded adjudication, nuisance strata and frozen phase. Publish only aggregates and source citations, not identifiable imagery. Independent replication must be able to reproduce with authorized dataset access.

## Hard falsification and go/no-go

- **Falsifies a native-frame exclusion claim:** a two-rater-confirmed CLOSED interior frame lies between two two-rater-confirmed OPEN retained frames under the frozen phase, with integrity and geometry controls passed.
- **Does not validate E002-371:** even a successful alias witness lacks independent shutter integration, an externally authenticated physical clock, a continuous-time eyelid velocity ceiling and certified 95-Hz negative sensitivity. These are mandatory in E002-567 Stage B.
- **Reject/abstain:** missing frame timing or source identity; unreadable eye; eyelash/eyewear occlusion; reflection; gaze-induced geometry failure; motion blur; changing illumination/exposure; rater disagreement; unjustified iris-scale uncertainty; mixed participant split; license breach. Report counts separately, not silently discard.
- **Stop after the frozen pilot** if no qualified independent human raters or source access are available; do not continue source archaeology or fabricate human annotations. A 2.4-GB archive download should occur only once in an authorized, no-cost environment, outside public CI. Do not auto-download it hourly.

## Evidence ledger at freeze

| Evidence | Status |
|---|---|
| Publicly described ~95-fps human eye video source | **IDENTIFIED** (published acquisition rate, not independently certified) |
| Source archive locally acquired and hashed | **NOT DONE** |
| Independent human rater pair | **0** |
| Anatomical positive native-frame witness | **0** |
| Physical shutter/photodiode captures | **0** |
| Certified continuous-time human velocity ceiling | **0** |
| Held-out physical-camera closure prediction | **0** |

**Product decision:** `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Even a completed LPW pilot can justify at most a limited **native-frame aliasing demonstration**. It cannot justify absence-of-closure, blink duration, PERCLOS, sleepiness or fatigue claims. Continue physical study E002-567 as the decisive gate.
