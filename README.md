# Lucent

> **Can a phone actively probe your state in five seconds instead of passively staring at your face?**

[![CI](https://github.com/sushxnthd/lucent/actions/workflows/ci.yml/badge.svg)](https://github.com/sushxnthd/lucent/actions/workflows/ci.yml)

Lucent is a research program for **ultra-short active human-state sensing** with hardware people already own.

The current research direction is **APST-5: Active Personalized State Tomography in Five Seconds**.

Instead of treating the front camera as a passive observer, the phone display becomes a controlled experimental input. During an approximately five-second scan, the screen emits a known luminance / visual sequence while the front camera records ocular and facial dynamics. The response is analyzed relative to a person's baseline and paired behavioral measurements.

Lucent grew out of [Somno](https://sushxnthd.github.io/somno/), which made the original product problem obvious: useful measurement loses value when people have to repeatedly stop, wear something, or perform a long explicit test.

This repository contains the research program, simulation code, validation rules, and results. It intentionally contains no app UI.

## APST-5

Let latent state be \(x_t\), display input \(u_t\), camera observations \(y_t\), personal history \(h_i\), and device/environment nuisance \(d_i\):

\`\`\`text
display probe u(t) ──> pupil / eye / facial dynamics ──> camera y(t)
        │                                               │
        └──────────── known perturbation ───────────────┘
                              │
                              v
               subject-relative state inference
\`\`\`

The research objective is not simply to fit a predictor. It is to choose the **probe itself** so that a strict time budget reveals as much identifiable state information as possible.

A generic design objective is:

\[
u^* = \arg\max_u \; \mathbb{E}[I(X;Y \mid U=u,H_i)] - \lambda C(u)
\]

where \(C(u)\) represents display-energy, comfort, and transition constraints.

See [APST5.md](APST5.md).

## First computational result

We implemented a literature-inspired delayed, asymmetric pupil-response surrogate and asked a deliberately constrained question:

> With the same five-second window and the same total high-luminance exposure, does **when** the phone perturbs the visual system change how much we can identify about its dynamics?

The design space contained 84 equal-exposure probes. Probe selection was performed on one synthetic parameter population and evaluated on **500 fresh held-out parameter draws**.

| Five-second probe | Held-out expected information gain |
| --- | ---: |
| optimized equal-exposure probe | **11.99 nats** |
| best contiguous pulse | 11.69 nats |
| evenly spaced pulses | 10.65 nats |

The optimized probe used two early high-luminance blocks and one late block:

\`\`\`text
time (s)     0    .5   1.0  1.5  2.0  2.5  3.0  3.5  4.0  4.5
display      low  HIGH HIGH low  low  low  low  low  HIGH low
\`\`\`

Under the surrogate model, that design produced:

- **+2.57% expected information gain** over the best contiguous equal-exposure pulse;
- **+12.60%** over an evenly spaced equal-exposure probe;
- an approximately **1.82x reduction in posterior uncertainty volume** relative to the best contiguous pulse.

This is an **in-silico experimental-design result, not human validation**. Its value is that it gives APST-5 a falsifiable first prediction: stimulus timing should matter even when duration and exposure are held fixed.

Reproduce it with:

\`\`\`bash
pip install -e ".[dev]"
python experiments/active_probe_design.py
\`\`\`

Full result: [results/APST5_SIMULATION_001.md](results/APST5_SIMULATION_001.md)


## Second computational result: personalization buys sensing time

APST5-SIM-002 changes the design question from "how much can five seconds see?" to:

> **how short can the scan become once Lucent already knows the stable person-specific nuisance dynamics?**

Using nuisance-projected Fisher information, the experiment separates transient state information from stable person/device parameters. A longitudinal personal baseline enters as nuisance prior precision.

In the held-out surrogate experiment:

| Condition | Held-out state information |
| --- | ---: |
| optimized 5 s, population nuisance prior | **0.3402 nats** |
| optimized 2 s, population prior | 0.2745 |
| optimized 2 s, nuisance SD reduced 15% | **0.3424** |
| optimized 2 s, nuisance SD reduced 25% | **0.4023** |
| optimized 2 s, nuisance SD reduced 50% | **0.6405** |

The 25%-tighter baseline case was then frozen and evaluated over **10 additional held-out synthetic populations**. The 2-second condition beat the 5-second population condition in **10/10 replications**, with a mean information ratio of **1.175x**.

This suggests a stronger Lucent architecture:

\[
\text{short active response} + \text{longitudinal personal prior}
\rightarrow
\text{state deviation}
\]

rather than re-estimating a person from scratch on every scan.

See [APST5-SIM-002](results/APST5_SIMULATION_002.md) and the [baseline compression derivation](docs/BASELINE_COMPRESSION.md).

## Why active probing is different

Passive five-second face-video drowsiness inference is already prior art. Smartphone pupillometry is prior art. Controlled screen-evoked pupil responses are prior art. Active ocular probing is also prior art.

The specific open gap Lucent targets is the **combination**:

1. ordinary smartphone;
2. approximately five seconds;
3. display-controlled perturbation;
4. synchronized camera response;
5. information-optimized probe design;
6. subject-relative / longitudinal priors;
7. state inference evaluated against behavioral targets;
8. strict unseen-participant and unseen-device testing.

Our literature search has not located a paper that establishes that full combination. That is a novelty hypothesis, not a patentability or priority claim.

## What would count as a real breakthrough?

Not a simulation score.

The strong version of the claim survives only if active five-second probing:

1. beats passive five seconds;
2. beats a conventional fixed active probe under matched exposure;
3. predicts paired behavioral state on participants never seen during training;
4. survives device and environment shifts;
5. benefits from personalization without requiring constant new labels;
6. reproduces on a fresh cohort.

The repo is structured to make those claims harder to fake.

## Research map

| Path | Purpose |
| --- | --- |
| [APST5.md](APST5.md) | active-probing thesis and breakthrough test |
| [RESEARCH.md](RESEARCH.md) | hypotheses, state targets, falsification criteria |
| [EXPERIMENTS.md](EXPERIMENTS.md) | leakage-resistant human validation program |
| [ROADMAP.md](ROADMAP.md) | staged path from simulation to fresh-cohort replication |
| [REFERENCES.md](REFERENCES.md) | closest prior art and measurement literature |
| [docs/PREREGISTRATION_TEMPLATE.md](docs/PREREGISTRATION_TEMPLATE.md) | freeze confirmatory analyses before final holdout |
| [docs/FAILURE_MODES.md](docs/FAILURE_MODES.md) | shortcut and false-positive threat model |
| [docs/POSITIONING.md](docs/POSITIONING.md) | boundary versus ordinary drowsiness classification |
| [docs/OPEN_QUESTIONS.md](docs/OPEN_QUESTIONS.md) | questions that can kill or narrow the thesis |
| [src/lucent/active_probe.py](src/lucent/active_probe.py) | pupil surrogate + information-design utilities |
| [experiments/active_probe_design.py](experiments/active_probe_design.py) | reproducible APST-5 design experiment |
| [results/APST5_SIMULATION_001.md](results/APST5_SIMULATION_001.md) | equal-exposure active-probe result |
| [results/APST5_SIMULATION_002.md](results/APST5_SIMULATION_002.md) | personalization / temporal-compression result |
| [docs/BASELINE_COMPRESSION.md](docs/BASELINE_COMPRESSION.md) | nuisance-projection derivation and design principle |

## Research principles

- **Perturb, don't merely observe.**
- **Match exposure before comparing probes.**
- **Optimize on one population, report on another.**
- **Split by person before reporting human performance.**
- **Baselines before bigger models.**
- **Ablations before explanations.**
- **Negative results are results.**
- **Product claims come after replication.**

## Status

**Two converging computational results; biological validation pending.**

The current result supports the research strategy that an actively designed five-second scan may be more informative than a conventional fixed probe under the same time and exposure budget. It does **not** yet establish that Lucent can estimate fatigue or cognitive performance in humans.

That is the next experiment.
