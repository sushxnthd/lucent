# Lucent Research Thesis

## 1. Problem

Most fatigue and cognitive-state measurements impose some explicit burden on the user: reaction-time tasks, questionnaires, wearables, or repeated manual logging. Lucent investigates whether a very short front-camera observation contains enough information to recover part of that signal.

The difficult part is not fitting a model to faces. It is demonstrating that any measured signal reflects **state** rather than person identity, device characteristics, lighting, pose, or other shortcuts.

## 2. Primary question

Given approximately five seconds of ordinary front-camera video, how much information about short-term fatigue and cognitive-performance state can be recovered under strict out-of-sample evaluation?

## 3. Working hypotheses

### H1 — State signal exists
Short facial video contains measurable temporal information associated with changes in fatigue or psychomotor performance.

### H2 — Temporal information matters
Video should outperform equally sized static-frame baselines if useful cues are carried by blink dynamics, eyelid motion, gaze stability, micro-movements, or other temporal structure.

### H3 — Personal baselines matter
Predicting deviation from an individual's baseline may be more reliable than estimating a universal absolute score.

### H4 — Generalization is the real test
Performance that disappears under subject-held-out, device-held-out, or session-held-out evaluation is not sufficient evidence for the core thesis.

## 4. Reference measurements

The research program pairs video with reference variables that can be independently measured, including:

- psychomotor reaction-time performance;
- subjective sleepiness ratings;
- recent sleep duration and timing;
- repeated measurements over time for within-person analysis.

No single proxy is treated as ground truth for the entire construct. Agreement and disagreement between targets are part of the analysis.

## 5. Confounds to actively attack

Lucent should be assumed vulnerable to shortcut learning until shown otherwise. Key confounds include:

- participant identity;
- age and stable facial morphology;
- camera/device model;
- lighting and exposure;
- background and location;
- head pose and viewing distance;
- glasses and occlusion;
- time of day;
- session order;
- label leakage through collection procedure.

## 6. Validation standard

A result becomes interesting only if it survives:

1. participant-held-out evaluation;
2. temporal/session holdouts;
3. device/environment stress tests;
4. comparison with trivial baselines;
5. static-frame versus temporal ablations;
6. uncertainty and calibration analysis;
7. replication on a fresh collection.

The central metric is not just raw predictive performance. It is **how much performance remains when obvious shortcuts are removed**.

## 7. Research direction

If reliable signal survives these tests, the next question is to determine the narrowest state variable that can be measured well enough to support a low-friction real-world system. If it does not, the failure itself should localize which assumptions about passive visual measurement were wrong.
