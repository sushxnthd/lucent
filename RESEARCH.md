# Lucent Research Thesis

## 1. Core question

Can an ordinary smartphone recover useful information about current fatigue and cognitive-performance state in approximately five seconds by **actively perturbing** the visual system and measuring the response?

Lucent now treats passive video as the baseline, not the final architecture.

## 2. Research hypothesis

A known stimulus turns state inference into a system-identification problem.

Passive observation sees a mixture of:

- stable identity;
- current state;
- lighting;
- device behavior;
- pose;
- spontaneous motion;
- context.

Active probing adds an input whose timing is known exactly. If transient state changes the response dynamics, that input can help separate state from nuisance.

The key claim is therefore:

> Under a fixed five-second and exposure budget, a carefully designed display probe should reveal more identifiable state information than a passive clip or a conventional fixed probe.

## 3. Operational targets

"Fatigue" is not treated as one perfect scalar.

Targets should remain separate until evidence justifies combining them:

- psychomotor vigilance / reaction-time outcomes;
- lapse-like events or slow-response tails;
- subjective state sleepiness;
- pupil-light-reflex / autonomic dynamic parameters;
- recent sleep duration and time awake as contextual baselines;
- within-person deviation from personal baseline.

## 4. Working hypotheses

### H1: active > passive
Matched five-second active probing adds information beyond passive five-second video.

### H2: optimized > fixed
Under matched duration and luminous exposure, an information-designed probe outperforms a conventional fixed stimulus.

### H3: temporal placement matters
The timing of perturbations changes parameter identifiability even when total high-luminance exposure is identical.

### H4: person-relative state is easier than universal ranking
Predicting deviation from a person's own baseline may generalize better than assigning one absolute cross-person state score.

### H5: the useful luminance regime is state-dependent
Low-to-mid luminance may carry stronger arousal-related modulation than simply maximizing brightness.

### H6: identity is a major shortcut
Random clip splits will overestimate generalization whenever repeated observations from the same person appear in training and test.

### H7: uncertainty should rise under distribution shift
The system should become less confident on unseen devices, lighting, pose, or ocular conditions.

### H8: personal baselines should compress measurement time
Longitudinal knowledge of stable person-specific dynamics should reduce nuisance uncertainty enough that a shorter active scan can preserve the state information of a longer population-level scan.

This is formalized with nuisance-projected Fisher information in [docs/BASELINE_COMPRESSION.md](docs/BASELINE_COMPRESSION.md).

## 5. Candidate observed channels

The active scan may use:

- pupil diameter dynamics;
- constriction / redilation velocity;
- blink timing;
- eyelid aperture;
- gaze and saccadic response to controlled targets;
- smooth-pursuit response;
- facial photoplethysmographic channels if signal quality permits;
- static and temporal facial representations as secondary signals.

No channel is assumed to be useful before ablation.

## 6. Confounds

### Person-level
- identity;
- age;
- eye color / iris contrast;
- stable facial morphology;
- glasses / contact lenses;
- habitual expression.

### Recording-level
- display luminance calibration;
- camera exposure and white balance;
- frame rate;
- rolling shutter;
- distance;
- pose;
- ambient light;
- device family.

### Protocol-level
- time of day;
- prior dark/light adaptation;
- session order;
- recent caffeine;
- sleep history;
- label timing;
- expectation effects;
- clips from one source recording crossing a split.

## 7. Falsification criteria

The active-sensing hypothesis weakens if:

- optimized active probes do not outperform fixed active probes under matched exposure;
- active five seconds does not outperform passive five seconds;
- participant-held-out effects vanish;
- results are explained by device or identity;
- state targets disagree in a way that invalidates the intended construct;
- fresh-cohort replication fails.

## 8. Evidence ladder

### Level 0: in-silico identifiability
Under explicit model assumptions, active design improves parameter identifiability under matched exposure.

**Current status: achieved provisionally in APST5-SIM-001.**

### Level 0b: personalization-compression prediction
A tighter longitudinal prior over stable nuisance dynamics should shift the duration-information curve leftward.

**Current status: achieved provisionally in APST5-SIM-002.**

### Level 1: hardware observability
A commodity phone can execute the probe and recover repeatable ocular response dynamics.

### Level 2: within-person state sensitivity
Repeated scans track paired state changes within individuals.

### Level 3: unseen-person generalization
The active signal survives participant-held-out evaluation.

### Level 4: active advantage
Optimized active five seconds beats passive five seconds and fixed active five seconds under matched constraints.

### Level 5: nuisance robustness
The active advantage survives device, session, lighting, and environment shifts.

### Level 6: fresh-cohort replication
A frozen probe and analysis plan reproduce on a new cohort.

Only Levels 4-6 justify strong external claims.

## 9. Immediate direction

The next decisive experiment is no longer "train a larger face model."

It is:

> implement the APST-5 probe on a commodity smartphone, verify pupil/eye observability, then run a paired pilot with a preregistered behavioral reference.
