# Lucent Research Thesis

## 1. Core question

Can an ordinary smartphone recover useful information about current fatigue and cognitive-performance state in roughly **2–5 seconds** by actively designing the ocular measurement?

Lucent treats passive video as the baseline, not the final architecture.

## 2. Research hypothesis

Passive observation mixes:

- stable identity;
- current state;
- device behavior;
- ambient light;
- pose;
- spontaneous motion;
- context.

Active probing introduces a known input. Longitudinal history supplies prior information about stable nuisance. Concurrent ocular challenges can interrogate multiple response systems in the same time window.

The architecture is therefore:

[
\text{state}
\mid
\text{active response},\
\text{personal history},\
\text{device/context}.
]

The optimization target is **state information density**, not raw model complexity.

## 3. Operational targets

"Fatigue" is not treated as one perfect scalar.

Candidate targets remain separate:

- PVT / reaction-speed outcomes;
- lapse-like events;
- subjective state sleepiness;
- pupil/autonomic dynamic parameters;
- controlled oculomotor performance;
- within-person deviation from an earlier baseline.

A composite score is justified only after the individual targets are understood.

## 4. Working hypotheses

### H1: active > passive
At matched duration, an informative active probe adds state information beyond passive observation.

### H2: optimized > fixed
At matched duration and exposure, an information-designed probe beats a conventional fixed active probe.

### H3: temporal placement matters
Stimulus timing changes dynamic-parameter identifiability even with identical total exposure.

**Computational status:** supported by APST5-SIM-001.

### H4: stable nuisance can be learned once
Longitudinal history can reduce uncertainty about stable person/device dynamics, leaving a short scan to focus on what changed.

**Mathematical status:** Baseline Compression Principle.

**Computational status:** APST5-SIM-002.

**Human-data status:** the simple personalization transform in MTS-REALDATA-001 did not pass its preregistered primary test.

### H5: immediate state is temporally local
For an immediate functional target, a short state-proximal sensor window may outperform a longer backward average because older observations dilute the current state.

**Human-data status:** exploratory support in MTS-REALDATA-001; independent replication required.

### H6: multimodal probing increases information density
Pupil and controlled gaze/pursuit dynamics can be elicited concurrently, allowing a shorter joint scan to compete with a longer single-channel scan.

**Computational status:** APST5-SIM-003.

### H7: the multimodal gain is not purely an independence artifact
The compression advantage should survive meaningful cross-channel information overlap.

**Computational status:** APST5-SIM-004; 3 s remains above the 5 s pupil-only comparator in the median at 25% incremental weaker-channel information.

### H8: identity is a major shortcut
Random clip splits overestimate generalization whenever the same participant appears in train and test.

### H9: uncertainty should increase under distribution shift
Unseen devices, lighting, pose, or ocular conditions should produce lower confidence rather than confident extrapolation.

## 5. Candidate observed channels

The active scan may use:

- pupil diameter dynamics;
- constriction / redilation velocity;
- blink timing;
- eyelid aperture;
- controlled gaze;
- smooth pursuit;
- reactive saccades where sampling allows;
- facial dynamics as secondary channels.

A channel is retained only if it adds held-out information beyond simpler channels and context baselines.

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
- camera exposure / white balance;
- frame rate;
- rolling shutter;
- distance;
- pose;
- ambient light;
- device family.

### Protocol-level

- time of day;
- prior light adaptation;
- session order;
- caffeine;
- recent sleep;
- label timing;
- expectation / task-learning effects;
- source clips crossing split boundaries.

## 7. Evidence ladder

### Layer A: mathematical design principles

- Baseline Compression Principle.
- Concurrent Multimodal Information Principle.
- Temporal Locality model.

### Layer B: reproduced computational evidence

- **SIM-001:** equal-exposure probe timing.
- **SIM-002:** baseline-conditioned temporal compression.
- **SIM-003:** concurrent pupil + pursuit compression.
- **SIM-004:** redundancy stress test.

### Layer C: existing human-data evidence

- **MTS-REALDATA-001:** immediate PVT performance contains a short-window passive ocular signal.
- Primary personalization hypothesis: **null**.
- 2 s temporal-locality observation: **exploratory positive**.

### Layer D: commodity-phone observability

**Not yet achieved.**

Required: synchronized display/camera timing and repeatable recovery of the modeled ocular dynamics on ordinary hardware.

### Layer E: prospective within-person state sensitivity

**Not yet achieved.**

Required: frozen paired active/passive protocol with behavioral reference.

### Layer F: unseen-person and unseen-device active advantage

**Not yet achieved.**

### Layer G: fresh-cohort replication

**Not yet achieved.**

Only Layers F–G support strong real-world generalization claims.

## 8. Current falsification targets

Lucent should be narrowed if:

- ordinary phone cameras cannot measure the required dynamics reliably;
- active scanning fails to beat passive scanning at matched duration;
- optimized stimulation fails to beat matched fixed stimulation;
- the multimodal channel adds no conditional information once pupil/history are known;
- the public-data temporal-locality effect fails on an independent cohort;
- participant-held-out effects disappear;
- device shifts dominate the signal;
- frozen fresh-cohort replication fails.

## 9. Immediate direction

The next decisive step is empirical:

> **execute a synchronized ~3 s concurrent pupil + pursuit probe on ordinary phone hardware and determine whether the required response dynamics are observable before making any state-prediction claim.**

The current repository has enough computational evidence to specify that experiment. It does not yet have the human phone data to declare it solved.
