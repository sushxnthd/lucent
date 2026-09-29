# Lucent

Lucent is a research project investigating how much useful fatigue and cognitive-performance signal can be recovered from a few seconds of ordinary front-camera video.

It grew out of **Somno**, an earlier sleep-debt system that combined reaction-time testing, facial signals, subjective measures, and longitudinal sleep history. Somno exposed a practical bottleneck: repeated explicit measurement creates friction. Lucent asks whether part of that measurement stack can be reduced to a brief, passive observation.

## Core research question

> Can roughly five seconds of commodity front-camera video predict meaningful changes in fatigue or cognitive performance in a way that survives identity, device, lighting, and environment shifts?

The goal is not to assume the answer is yes. The goal is to determine exactly which signals, if any, survive rigorous out-of-sample testing.

## Current research program

- Pair short facial-video clips with stronger reference measurements such as psychomotor reaction time, subjective sleepiness, and sleep-history variables.
- Separate **within-person change** from simple identity recognition.
- Test generalization across unseen participants, devices, sessions, lighting conditions, and time.
- Compare against trivial and non-visual baselines.
- Run controlled ablations to identify which temporal and facial cues carry signal.
- Quantify calibration, uncertainty, and failure modes rather than reporting only aggregate accuracy.

## Repository

- [RESEARCH.md](RESEARCH.md) — research thesis, hypotheses, and validation criteria.
- [EXPERIMENTS.md](EXPERIMENTS.md) — experimental plan and evaluation protocol.

This repository is intentionally research-only. Product and interface prototypes are not part of the current Lucent work.
