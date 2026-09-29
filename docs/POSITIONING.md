# Positioning: What Lucent Is Actually Testing

Camera-based drowsiness detection already exists. Lucent is not claiming novelty from pointing a camera at a face.

The research question is narrower and harder:

> Can a **very short** ordinary front-camera clip recover a useful, person-generalizable signal about current fatigue or cognitive performance when evaluated against paired behavioral targets and strict participant holdouts?

## How this differs from a typical drowsiness classifier

| Dimension | Common drowsiness-detection setup | Lucent target |
| --- | --- | --- |
| Primary setting | driver monitoring / safety | general low-friction state measurement |
| Sensor | dashboard / IR / dedicated camera or RGB | commodity front-facing RGB camera |
| Observation | often extended video | approximately 5 seconds |
| Target | alert / drowsy class | behavioral + subjective state targets |
| Label source | class annotation / induced condition | paired reaction-time, state sleepiness, recent sleep context |
| Main question | can the class be recognized? | what state information survives unseen people and conditions? |
| Personalization | often secondary | explicitly compared with population-level prediction |
| Evaluation | dataset benchmark dependent | participant-, session-, device-, and environment-held-out |
| Product claim | detect drowsiness | only whatever narrow state variable actually survives validation |

## The actual novelty target

Lucent becomes scientifically interesting if it can demonstrate all of the following together:

1. **short-window sufficiency**: useful information exists in a few seconds, not only long observations;
2. **incremental information**: video adds something beyond sleep history, time of day, and static appearance;
3. **unseen-person generalization**: performance survives complete participant holdout;
4. **state sensitivity**: predictions track changes within people rather than just ranking stable identities;
5. **replication**: the effect survives a fresh cohort after the analysis is frozen.

If those conditions fail, Lucent should narrow or abandon the claim.

## Why five seconds?

Five seconds is not treated as a magic biological threshold. It is a product-driven scientific constraint.

The original Somno system showed the cost of explicit measurement. Lucent asks how far measurement can be compressed before useful information disappears.

That creates an empirical curve rather than a slogan:

`window length -> signal quality -> friction`

The eventual system should be built around the shortest window that remains scientifically defensible, even if that turns out not to be exactly five seconds.

## What Lucent is not

- not a claim that a face reveals every aspect of cognition;
- not a medical diagnosis from a selfie;
- not a benchmark-accuracy project;
- not a replacement for polysomnography;
- not evidence that correlation implies a causal mechanism;
- not a product until the measurement survives replication.

The point of the repository is to make the claim smaller, testable, and progressively harder to fool.
