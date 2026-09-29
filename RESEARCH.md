# Lucent Research Thesis

## 1. Core question

Given approximately five seconds of ordinary front-camera RGB video, how much information about short-term fatigue and cognitive-performance state can be recovered under strict out-of-sample evaluation?

The project is intentionally framed as an empirical question. The answer may be "less than expected."

## 2. Why this question matters

Current low-friction sleep and fatigue products often depend on one of two compromises:

1. **explicit effort**, such as reaction-time tasks, questionnaires, or repeated logging; or
2. **dedicated hardware**, such as watches, rings, headbands, or other sensors.

Lucent investigates a third direction: whether hardware people already have can recover a useful subset of state information with almost no interaction burden.

The scientific challenge is to distinguish a true transient state signal from stable identity and collection artifacts.

## 3. Operational targets

Lucent does not treat "fatigue" as one perfectly observed ground-truth variable.

Candidate targets include:

- psychomotor vigilance / reaction-time outcomes;
- lapse counts or slow-response tails where the task supports them;
- subjective state sleepiness;
- recent sleep duration and timing;
- within-person deviation from a repeated personal baseline.

Each target is analyzed separately before any composite score is considered.

## 4. Working hypotheses

### H1: brief visual state signal exists

Short facial video contains measurable information associated with contemporaneous fatigue or psychomotor performance.

### H2: temporal structure adds information

A short video representation should outperform matched static-frame baselines if useful signal is carried by temporal phenomena such as eyelid dynamics, blink timing, gaze stability, or head micro-movement.

### H3: personal deviation is easier than universal ranking

Predicting how a person differs from their own baseline may generalize better than assigning an absolute cross-person "fatigue score."

### H4: video must add signal beyond context

A useful video model should add predictive information beyond sleep history, time of day, and other non-visual metadata.

### H5: identity is a major shortcut

Performance from random clip-level splits will overestimate real generalization whenever repeated observations from the same participant appear in both train and test sets.

### H6: uncertainty should rise under distribution shift

If the system sees a participant, device, or recording condition outside its training distribution, uncertainty should increase rather than remain spuriously confident.

## 5. Candidate visual signals

The project may investigate:

- eyelid aperture and closure dynamics;
- blink timing and duration;
- gaze stability;
- head-motion dynamics;
- facial action / expression dynamics;
- temporal texture representations learned directly from video.

These are candidate measurements, not assumed causal mechanisms.

## 6. Confounds to attack explicitly

Lucent should be assumed vulnerable to shortcut learning until demonstrated otherwise.

### Person-level
- participant identity;
- age and stable facial morphology;
- habitual expression;
- glasses and stable appearance.

### Recording-level
- device / camera model;
- resolution and frame rate;
- exposure and white balance;
- compression;
- background;
- viewing distance and head pose.

### Protocol-level
- time of day;
- session order;
- sleep schedule;
- test administrator effects;
- labels encoded indirectly by collection conditions;
- multiple clips derived from one recording crossing a split boundary.

## 7. Falsification criteria

The current hypothesis should be weakened or rejected if:

- performance collapses under participant-held-out evaluation;
- a static frame performs as well as the full clip despite a temporal-mechanism claim;
- time-of-day or sleep-history baselines explain nearly all apparent signal;
- identity or device information explains the prediction;
- effects fail to replicate on a fresh collection;
- uncertainty remains badly calibrated under known distribution shift.

A negative result that identifies one of these failure modes is considered useful research.

## 8. Evidence ladder

### Level 0: pipeline sanity
The model can overfit a small controlled subset and all labels, timestamps, and splits pass integrity checks.

### Level 1: within-person association
Video features track repeated changes within the same individuals.

### Level 2: unseen-person generalization
The signal survives participant-held-out evaluation.

### Level 3: nuisance robustness
Performance remains useful across sessions, devices, lighting, pose, and environment changes.

### Level 4: incremental value
Video adds information beyond sleep history, time of day, and static visual baselines.

### Level 5: fresh-cohort replication
A frozen analysis plan reproduces on newly collected participants.

Only Levels 4-5 would support strong product claims.

## 9. Research direction

If a robust signal survives, the next step is not to predict everything. It is to identify the **narrowest state variable that can be measured reliably enough to matter**.

If the signal does not survive, the goal is to make the failure informative enough to show which assumptions about brief passive visual measurement were wrong.
