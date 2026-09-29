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

## Phase 1: phone observability pilot

Build the smallest instrument that can:

- drive a precisely timed display sequence;
- record synchronized front-camera video;
- log actual device brightness / display setting;
- estimate pupil / eye quality per frame;
- preserve raw timing metadata.

Primary question: can the response features required by APST-5 be measured repeatably on commodity hardware?

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
