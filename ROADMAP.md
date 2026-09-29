# Research Roadmap

Lucent is staged so that each step can kill the hypothesis before more complexity is added.

## Phase 0: research architecture

**Status: complete**

- [x] falsifiable thesis;
- [x] participant-held-out evaluation standard;
- [x] leakage / shortcut threat model;
- [x] preregistration template;
- [x] prior-art boundary;
- [x] reproducible CI.

## Phase 0.5: active-probe timing

**Status: complete computational result**

[APST5-SIM-001](results/APST5_SIMULATION_001.md)

- [x] fixed 5 s budget;
- [x] equal total high-luminance exposure;
- [x] exhaustive 84-pattern timing search;
- [x] independent held-out synthetic population;
- [x] optimized timing beats contiguous and evenly spaced controls.

## Phase 0.6: baseline-conditioned compression

**Status: complete computational result**

[APST5-SIM-002](results/APST5_SIMULATION_002.md)

- [x] separate transient state from stable nuisance;
- [x] derive nuisance-projected state information;
- [x] prove monotonic benefit from tighter nuisance prior under the model;
- [x] show 2 s personalized-information condition can exceed 5 s population condition in held-out simulations.

## Phase 0.7: concurrent multimodal compression

**Status: complete computational result**

[APST5-SIM-003](results/APST5_SIMULATION_003.md)

- [x] add smooth-pursuit state channel;
- [x] optimize pursuit frequency on a design population;
- [x] evaluate 80 state-effect/device-noise conditions;
- [x] show 3 s concurrent probe beats 5 s pupil-only in 72/80 conditions.

## Phase 0.8: redundancy robustness

**Status: complete computational result**

[APST5-SIM-004](results/APST5_SIMULATION_004.md)

- [x] relax full-information-additivity assumption;
- [x] sweep incremental-information fractions from 100% to 0%;
- [x] show 3 s median remains above 5 s pupil-only at 25% incremental weaker-channel information.

## Phase 0.9: public human-data bridge

**Status: complete, mixed result**

[MTS-REALDATA-001](results/MTS_REALDATA_001.md)

- [x] freeze analysis before full run;
- [x] strict leave-one-subject-out analysis;
- [x] keep immediate PVT target fixed across duration;
- [x] retain preregistered null personalization result;
- [x] identify exploratory 2 s temporal-locality effect;
- [ ] replicate the duration effect on an independent cohort.

## Phase 1: commodity-phone observability

**Status: next empirical gate**

Build the minimum research instrument that can:

- drive the concurrent luminance + moving-target probe;
- record synchronized front-camera frames;
- preserve actual frame timestamps;
- record device, brightness, and ambient-light metadata;
- recover pupil / gaze trajectories with per-frame quality;
- run a 3 s and 5 s matched protocol.

**Primary endpoint:** repeatability / observability of response dynamics, not fatigue prediction.

**Kill condition:** ordinary phone hardware cannot recover the required signals with enough repeatability.

## Phase 2: paired naturalistic human pilot

After Phase 1 succeeds:

- repeated sessions across normal day-to-day alertness variation;
- no deliberately induced sleep deprivation required;
- pair scans with a fixed behavioral reference;
- compare passive 3 s, fixed-active 3 s, optimized-active 3 s;
- keep the analysis frozen before the final holdout.

**Primary question:** does active concurrent probing add held-out behavioral-state information?

## Phase 3: temporal-locality replication

Use a new cohort or genuinely independent dataset.

Test:

- 2 s vs 3 s vs 5 s vs longer passive windows;
- same immediate target for every duration;
- duration chosen before final holdout;
- whether target smoothing shifts the optimal window longer.

This is the confirmatory test for the public-data observation.

## Phase 4: unseen-person and unseen-device study

- participant-held-out;
- device-held-out;
- session-held-out;
- ambient-light stress;
- glasses / occlusion;
- viewing-distance variation;
- explicit uncertainty calibration.

## Phase 5: frozen fresh-cohort replication

Freeze:

- probe;
- duration;
- preprocessing;
- target;
- model-selection rule;
- exclusions;
- primary metric.

Collect a new cohort and evaluate once.

## Phase 6: productization

Only after replication:

- choose the narrowest reliable state variable;
- decide whether personalization is worth its complexity;
- minimize interaction;
- measure whether the information changes real decisions or outcomes.

Lucent does not need to infer everything. One robust, high-frequency state measurement is more valuable than many fragile ones.
