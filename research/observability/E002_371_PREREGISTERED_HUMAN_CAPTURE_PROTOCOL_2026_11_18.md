# E002-371 — prospective human validation protocol (frozen 2026-11-18 UTC)

Status: **protocol only, no human observations**. This document is a pre-data experimental specification, not a claim of ethics approval or empirical validation. Any amendment must be dated and preserved before examining confirmatory outcomes.

## Question and primary estimand
Can a conservative exposure-aware, velocity-bounded shutter-gap criterion exclude a complete eyelid closure between ordinary-camera observations without a false exclusion on held-out synchronized reference video?

Define aperture a(t) in mm (zero = independently annotated full lid closure), with absolute speed |da/dt| <= V. Two ordinary-camera exposure intervals of length E1 and E2 border a dark gap G. Their *calibrated linear aperture means* are m1 and m2, with lower confidence bounds L1,L2. Exposure-endpoint aperture lower bounds are b1=max(0,L1-V*E1/2), b2=max(0,L2-V*E2/2). A hidden closure is excluded only if b1+b2>V*G, with conservative upper bounds for V,E1,E2,G, and all calibration prerequisites independently authenticated. At equality or with missing evidence, abstain. Verify this sufficient condition independently from source code; do not claim necessity under noisy measurements.

## Data acquisition and provenance
Recruit consenting adults under approved local research/ethics and privacy procedures before any collection. Record synchronized high-speed reference video (target >=240 *verified unique frames/s*, preferably >=500) and ordinary-camera stream (nominal 24/30/60 fps). Capture a visible hardware LED timing pulse and measured exposure/readout metadata in both streams. Establish *actual* timestamp uncertainty and dropped/duplicated frame counts from pulse observations, not container FPS. Use independent geometric scale markers; avoid storing identifying face regions when cropped eyelids suffice. Record device model, shutter type, firmware, resolution, light level, exposure settings and all exclusions. Do not use synthetic interpolated frames as high-speed ground truth.

## Independent velocity calibration
Separate calibration participants/sessions from confirmatory sessions; estimate aperture from high-speed reference with two blinded annotators, calibration target and uncertainty interval. A sample maximum or percentile is NOT a certified physiological upper bound. Unless a defensible deterministic upper bound with explicit scope is independently established, report only conditional sensitivity curves across assumed V and force product ABSTAIN. Do not estimate V from the same confirmatory trajectories used to test exclusion.

## Freeze and held-out design
Freeze code, hashes, annotation rules, thresholds and nuisance strata before confirmatory video review. Development set may establish geometry/annotation quality; disjoint participant-level holdout is primary. Target >=20 adults with >=30 spontaneous or prompted blinks each across varied illumination/gaze, including glasses when feasible; this is a feasibility target, not a power claim. Randomize camera timing offsets; evaluate virtual exposure/downsampling only on genuinely high-speed reference timestamps, with verified exposure integration. Mark intervals uncertain if reference frame spacing/annotation uncertainty could hide a closure. Blind reference annotators to exclusion predictions.

## Primary outcomes
Primary safety outcome: number of **false exclusions** / number of reference-confirmed hidden closures, with exact binomial 95% upper confidence bound; report denominator and selection criteria. Zero observed failures does not establish zero risk. Secondary: exclusion coverage among adjudicable gaps, abstention rate, calibration failure rate, uncertainty intervals and per-participant performance. Report paired comparisons to naive instantaneous treatment and to always-abstain. Evaluate at least G/E combinations spanning both sides of the dimensionless boundary R=(b1+b2)/(V*G), including R near 1; for G=0 handle separately. No retrospective threshold tuning on holdout.

## Nuisance and falsification matrix
Stratify by: camera geometry/scale, brightness and illumination transitions, missing/duplicated frames, motion blur, gaze direction, glasses/reflections, rolling shutter, timebase drift/clock error, exposure nonlinearity, inter-annotator disagreement and partial/occluded lids. For each nuisance, run a stress test that deliberately worsens uncertainty; any unjustified exclusion is a safety failure. Missing calibration, nonlinearity, uncertain time sync or unreliable segmentation => ABSTAIN, not a positive product claim.

## Instrument substitute if human recordings cannot be obtained
Build a physical moving aperture with independently measured geometry, high-speed photodiode/encoder reference, triggered LED clock, and camera exposure log. Pre-register triangle and asymmetric motion trajectories including adversarial within-exposure closure; measure actual sensor response and rolling-shutter artifacts. Publish raw traces, calibration, scripts and hashes. Instrument evidence can validate timing/optics but **cannot** validate human eyelid velocity or fatigue inference.

## Decision rules
Reject the proposed product exclusion claim if any independently adjudicated hidden closure is falsely excluded under claimed certified assumptions; investigate annotation and provenance before interpreting. If no defensible physiological V exists, maintain camera-derived hidden-closure inference disabled and ship only explicitly non-diagnostic response-time/self-report workflows with invalidation and abstention. Any successful human experiment supports only the sampled conditions, not universal physiological guarantees.

## Priority and novelty
A Lipschitz observability inequality is not by itself a new physiological law. The contribution, if any, must arise from independently verified capture, a falsifiable boundary prediction, rigorous nuisance robustness and a materially improved calibrated decision policy. Conduct a primary-literature priority audit before publication claims.
