# Failure Modes and Shortcut Threat Model

A visually convincing demo can still be scientifically wrong. This document lists the failure modes Lucent should try to cause before anyone else does.

## 1. Identity memorization

### Failure
Repeated clips from one person appear on both sides of a split. The model learns stable facial identity that correlates with that person's average target.

### Detection
- participant-held-out evaluation;
- compare random vs grouped splits;
- train an identity probe on learned representations.

### Mitigation
Never report random clip splits as the main result.

## 2. Session leakage

### Failure
Frames or neighboring clips from the same recording session cross the split boundary.

### Detection
Audit source-recording and session IDs, not only clip IDs.

### Mitigation
Group by the highest-level shared source unit.

## 3. Device shortcut

### Failure
One device, exposure profile, codec, or resolution becomes correlated with target labels.

### Detection
- device-only baseline;
- device-ID probe;
- held-out-device evaluation.

## 4. Time-of-day shortcut

### Failure
The model or metadata predicts circadian timing rather than the intended state.

### Detection
Compare against time-only and time + sleep-history baselines.

## 5. Static appearance masquerading as temporal signal

### Failure
A temporal architecture scores well even though a single frame contains the same information.

### Detection
Matched static-frame baseline and temporal-order shuffle.

## 6. Protocol leakage

### Failure
Participants look or behave differently because they know which condition they are in, or collection conditions encode the label.

### Detection
Blind quality review where possible; inspect metadata predictability; alter collection order.

## 7. Distribution-shift confidence failure

### Failure
Predictions remain highly confident for unseen devices, lighting, pose, or severe occlusion.

### Detection
Reliability analysis under explicit stress tests.

## 8. Aggregation hides failure

### Failure
A good global average is driven by a subset of participants while others are systematically poor.

### Detection
Report participant-level error distributions and subgroup slices where sample size allows.

## 9. Target ambiguity

### Failure
"Fatigue" is treated as a single ground-truth scalar even when subjective sleepiness and cognitive performance diverge.

### Detection
Analyze targets separately and quantify disagreement.

## 10. Researcher degrees of freedom

### Failure
Many targets, splits, thresholds, and models are tried, but only the best-looking result is reported.

### Detection
Preregister confirmatory analyses and publish negative / null results.

## Adversarial standard

Before accepting a result, ask:

> If I wanted to make this result disappear without changing the underlying phenomenon, which split, baseline, or stress test would I choose?

Run that test.
