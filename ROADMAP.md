# Research Roadmap

Lucent is staged so that each phase can kill the hypothesis before more complexity is added.

## Phase 0: research architecture

**Status: complete**

- [x] define participant-held-out evaluation as primary;
- [x] define leakage / shortcut threat model;
- [x] add reproducible split utilities;
- [x] add preregistration template;
- [x] establish prior-art boundary;
- [x] formulate APST-5 active-sensing hypothesis.

## Phase 0.5: active-probe identifiability

**Status: first result complete**

- [x] implement a delayed asymmetric pupil-response surrogate;
- [x] formulate Bayesian information-gain objective;
- [x] constrain probe duration and total high-luminance exposure;
- [x] enumerate all 84 equal-exposure binary probes;
- [x] optimize on one synthetic parameter population;
- [x] evaluate on 500 fresh parameter draws;
- [x] identify a nontrivial split-pulse design that beats contiguous and evenly spaced controls.

**Result:** [APST5-SIM-001](results/APST5_SIMULATION_001.md)

**Important:** this is a model-based design result, not evidence that fatigue can already be inferred from people.


## Phase 0.75: baseline-compression result

**Status: first result complete**

- [x] partition transient state from stable nuisance parameters;
- [x] derive efficient state information using a Schur complement;
- [x] prove monotonic gain with increasing nuisance-prior precision;
- [x] optimize two-second and five-second probes under matched model assumptions;
- [x] evaluate on independent nuisance/effect populations;
- [x] run ten additional held-out replication populations.

**Result:** [APST5-SIM-002](results/APST5_SIMULATION_002.md)

The current surrogate predicts that a 25% reduction in stable nuisance uncertainty is sufficient for a two-second active probe to exceed a five-second population-level probe on state information across all ten additional held-out replication populations.

This is a **measurement-design prediction**, not a validated human duration claim.

## Phase 0.9: empirical temporal-scale audit

**Status: replication/falsification cycle complete**

- [x] retain the original MTS 2-second exploratory temporal-locality observation;
- [x] run an independent preregistered EyeLink duration test and retain the reversed result;
- [x] run an independent CogBeacon duration test and retain the null/reversed result;
- [x] preregister a within-dataset Massoz target-timescale manipulation;
- [x] observe the Massoz target-history crossover;
- [x] preregister and run a CogBeacon interaction replication;
- [x] retain the failed CogBeacon interaction replication;
- [x] preregister and run an independent Martin PVT/pupil interaction replication;
- [x] retain the failed Martin PVT interaction replication;
- [x] preregister a time-on-task/session nuisance audit of the original Massoz crossover;
- [x] confirm that the Massoz crossover survives that frozen nuisance model;
- [x] perform a literature audit and narrow the novelty claim.

**Evidence summary:**

| Test | Interaction | 95% CI |
| --- | ---: | ---: |
| Massoz original | **+0.2439** | **[+0.1647,+0.3191]** |
| Massoz + time/session nuisance | **+0.2056** | **[+0.1328,+0.2749]** |
| Martin independent PVT/pupil | -0.0264 | [-0.0815,+0.0281] |
| CogBeacon | -0.0645 | [-0.1665,+0.0313] |

**Conclusion:** the target-history crossover is robust inside the Massoz analysis but not general across datasets. The working design principle is now signal × target × protocol alignment, not a universal duration rule.

Full audit: [TEMPORAL-SCALE-AUDIT-001](results/TEMPORAL_SCALE_AUDIT_001.md)

## Phase 0.95: camera-robust observability simulation

**Status: complete**

- [x] freeze a phone-camera stress model before held-out evaluation;
- [x] search all 84 equal-exposure timing patterns by P10 separation;
- [x] evaluate on 500 fresh synthetic people;
- [x] stress 60/30/24 FPS, jitter, frame drops, and observation noise;
- [x] test the already frozen E002 sequence without changing the human protocol.

**Result:** the robust search selected (1,2,9), but the frozen E002 sequence (1,2,8) independently passed the same model-robust criterion with held-out P10 S **11.272** and **100%** of person × camera cells above S=1.25.

This only reduces a model-level camera-sampling risk. E002 still requires real captures.

## Phase 0.97: public-human response and device bridge

**Status: complete; mixed evidence**

- [x] identify an open controlled-luminance human pupillometry dataset;
- [x] freeze a participant-level equal-exposure probe test before outcome analysis;
- [x] retain the failed confirmatory single-kernel E002 result;
- [x] run the predeclared post-primary directional-kernel analysis;
- [x] test complete held-out two-transition superposition adequacy;
- [x] stress the human-calibrated E002 waveform at 50/30/24 Hz;
- [x] identify an independent concurrent EyeLink/Pupil Labs luminance dataset;
- [x] preregister cross-device held-out waveform transfer;
- [x] test person-specific residual transfer against mismatched-participant negative controls.

### PsPM-AOB_UW

**Confirmatory primary:** not supported.

Frozen E002 under one symmetric signed response kernel:

- held-out P10 S **0.824**
- held-out median S **1.059**
- **27.3%** above S=1.25

**Secondary directional model:** positive but explicitly post-primary.

- design search selected frozen E002 **(1,2,8)** at rank 1;
- held-out P10 S **1.264**;
- held-out median S **1.836**;
- **90.9%** above S=1.25;
- full two-transition pooled R2 was positive for **17/22** participants;
- 24/30 Hz sampling preserved essentially the same predicted separation.

### Independent Ehinger concurrent-device dataset

**Preregistered cross-device waveform criterion:** supported.

- 15 participants;
- blocks 1–3 calibration, 4–6 held out;
- macro-r **0.9974**, 95% CI **[0.9948,0.9987]**;
- **15/15** participants held-out r>0.70;
- secondary leave-one-person-out residual transfer macro-r **+0.8910** versus mismatched-person null 95% **[-0.1941,+0.0846]**.

**Conclusion:** the human bridge is substantially stronger than the original surrogate-only story, but it still stops one step short of Lucent's hardware claim. The decisive missing link is ordinary RGB phone capture under E002.

Full synthesis: [APST5-HUMAN-CALIBRATION-001](results/APST5_HUMAN_CALIBRATION_001.md)

## Phase 1: phone observability pilot

**Status: instrument implemented; real captures pending**

The synchronized E002 instrument, fixed probe protocol, offline capture-quality gate, visible-light pupil extractor, and aggregate engineering decision rule are implemented and merged.

Public human EyeLink data and an independent concurrent Pupil Labs/EyeLink dataset now reduce two upstream uncertainties: directional human pupil dynamics and transfer to a dedicated lower-cost video eye tracker. The remaining step still cannot be substituted with public-data analysis: collect repeated real captures on an **ordinary RGB phone front camera** under the frozen E002 protocol.

The instrument can:

- drive a precisely timed display sequence;
- record synchronized front-camera video;
- log actual device brightness / display setting;
- estimate pupil / eye quality per frame;
- preserve raw timing metadata.

Primary question: can the response features required by APST-5 be measured repeatably on commodity hardware?

**Exit rule:** timing + observability must pass, plus either repeatability or matched-exposure temporal distinguishability under the frozen E002 gates.

**Kill condition:** signal quality is too inconsistent across ordinary phones to support dynamic inference.

## Phase 2: paired human pilot

Collect repeated active scans paired with:

- psychomotor vigilance / reaction-time reference;
- state sleepiness;
- recent sleep context.

Use the preregistration template before evaluating the final holdout.

Primary questions:

- does active five seconds beat passive five seconds?
- does optimized timing beat fixed timing under matched exposure?
- which target moves first?

## Phase 3: unseen-person test

Scale collection enough for meaningful participant-held-out evaluation.

Primary questions:

- does the active advantage survive unseen people?
- does personalization help after a small baseline set?
- can identity be decoded from the representation more easily than state?

## Phase 4: device and environment robustness

Stress:

- device family;
- camera frame rate;
- brightness calibration;
- ambient illumination;
- pose;
- distance;
- glasses / occlusion.

The optimizer may need to become **device-aware** while remaining state-general.

## Phase 5: fresh-cohort replication

Freeze:

- display probe;
- preprocessing;
- target;
- model-selection rule;
- primary metric;
- exclusions.

Then collect a new cohort and evaluate once.

## Phase 6: productization

Only after replication:

- choose the narrowest reliable state variable;
- minimize interaction further;
- determine whether longitudinal personalization adds practical value;
- test whether the measurement changes user decisions or outcomes.

Lucent does not need to infer everything. One robust, high-frequency state measurement would be more valuable than a broad set of fragile estimates.
