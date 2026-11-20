# E002-582 | Frozen external 100-fps human full-closure label omission test

**Frozen:** 2026-11-01, before retrieving the Silesian5 annotation archive. **Kernel:** E002-371. **Purpose:** obtain an independent human-annotated *positive* temporal alias observation, not certify E002-371, velocity, physical exposure, or any fatigue product. No Silesian5 source has been accessed by this protocol.

## External source and prior-art boundary

Source: Andrej Fogelton's public Silesian5 (Basler5) annotations, https://www.blinkingmatters.com/research (dataset section, direct link labelled "our annotation"). The source reports five participants, 100-fps Basler acquisition, 640x480 video, 300 blinks, 58,884 annotated frames (59,031 originally, some lost in video conversion). Its human annotation includes per-frame **LE_FC/RE_FC**: C denotes an eye **90%-100% closed**, **LE_NV/RE_NV**: N denotes eye not visible, and **NF**: N denotes nonfrontal face. This is not a continuous eyelid-aperture trace or calibrated acquisition clock. Source says blink intervals can include nonclosed onset/offset frames. Video redistribution requires a separate signed license; retrieve **annotations only** and never fetch/share video.

Research question, precommitted before source access: **Can a human-annotated positive full-closure frame/run be entirely absent from nominal ordinary-rate temporal samples of a high-rate human annotation sequence?** A positive demonstrates index-only temporal aliasing of the investigators' *FC labels*. It does **not** establish that an ordinary physical camera with finite exposure would miss the closure. It also does not measure velocity or prove a strict normalized aperture threshold.

## Source-eligibility and parse freeze

Fetch the single archive at the source's linked Silesian5 annotation URL once. Record exact download SHA-256 and ZIP integrity; never log raw rows, face boxes, eye landmarks, per-frame participant identifiers, or images. Accept only textual annotations with the **published 19-field schema**: frame ID, blink ID, NF, LE_FC, LE_NV, RE_FC, RE_NV, face box (4), left eye corners (4), right eye corners (4). Identify five distinct sequences from archive member boundaries, not inferred identities. Require 58,884 valid frame rows in total, strictly increasing unique frame IDs **within** each sequence, and no missing frame IDs **inside an analyzed contiguous run and its immediate flanks**. A partial or differently formatted source must be declared INELIGIBLE rather than guessed or silently repaired. Do not equate reported 100 fps with authenticated timestamps. If timestamp files are not independently calibrated, report frame indices only.

## Locked positive-only endpoint

For each eye separately, define an **FC run** as a maximal consecutive native-frame interval whose eye-specific FC flag is C. Require at least one frame in the run and at least one immediate annotated flank on each side. If either flank or any run frame has eye-not-visible N or nonfrontal N, mark the run NUISANCE_ABSTAIN, not a negative. Reject unknown flag tokens, duplicated indices, inconsistent sequence boundaries, or invalid ZIP. Do not infer anatomical OPEN from FC != C. Do not infer full closure from a blink ID alone.

For each **integer phase** phi=0,...,9, define the nominal 100-to-30 sample indices as r(k)=phi+floor(10k/3), for all k>=0 within the sequence's absolute native-frame-index origin. A run is **label-omitted** in phase phi if it has at least one FC-positive native frame and no r(k) inside the run. Evaluate **all ten phases** without selecting a favorable phase; report aggregate eligible FC runs, abstentions, missed runs per phase, and number of runs missed in every phase, separately by eye and at subject level. Report a worst-phase and best-phase rate as descriptive within-source quantities, **not population confidence intervals**. Do not treat eyes, phases, or events within a person as independent participants.

A positive omission is a *human-label index alias witness*. No negative 30-fps shutter exclusion, reference sensitivity, real 30-fps exposure, continuous-time velocity bound, or PERCLOS/blink/fatigue score follows. If no positive events, preserve zero without tuning. The frozen primary criterion is **at least one nuisance-eligible human FC run omitted by at least one of the ten phases**. All-phase omission is a stricter secondary endpoint.

## Adversarial falsifiers and provenance

Before authentic source analysis, test a one-frame FC run omitted under at least one phase; a long run sampled under all phases; nonfrontal/not-visible abstentions; missing frame IDs and duplicated rows; different left/right labels; malformed flags; ZIP path traversal and decompression limits; deterministic phase invariance under member order. No artificial human labels or fabricated rater pairs. If public archive is inaccessible or schema incompatible, preserve the access failure and stop; do not retune the protocol after viewing the data.

The investigator labels are **not two independent blinded raters**, and the source's 90%-100% closed definition is **not** E002-576's iris-normalized aperture <=0.20. No independent velocity, physical shutter, external timing, or held-out prospective physical prediction exists. Treat this dataset as an independent **human-label external control**, not a substitute for E002-567 synchronized physical study or E002-573 independent-rater LPW holdout.

**Product consequence frozen:** Any positive finding establishes that sparse frame sampling can omit independently published human FC-positive labels in this source; it does not license Lucent physiological claims. The gate remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush stays untouched.
