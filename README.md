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


## Third computational result: concurrent multimodal compression

APST5-SIM-003 asks whether a short scan can probe **pupil + smooth-pursuit state information concurrently** instead of spending the same time on pupil dynamics alone.

Across an 80-cell held-out sensitivity grid spanning pursuit-effect strength, response slowing, and gaze noise:

| Scan | Cells beating optimized 5 s pupil-only | Median information ratio |
| --- | ---: | ---: |
| 2 s concurrent pupil + pursuit | 60/80 | **1.157x** |
| 3 s concurrent pupil + pursuit | 72/80 | **1.238x** |

This is a model-based sensitivity result, not human validation.

Full result: [results/APST5_SIMULATION_003.md](results/APST5_SIMULATION_003.md)

## First public human-data result: temporal locality

MTS-REALDATA-001 uses public eyelid-distance and PVT reaction-time data from Massoz et al. with a frozen leave-one-subject-out analysis.

The preregistered personalization hypothesis at 5 seconds was **not supported**:

\[
\Delta r = +0.0064,\qquad 95\%\ \mathrm{CI}=[-0.0169,+0.0295].
\]

That null result is retained.

However, the exploratory duration analysis produced a stronger observation: the **2-second pre-stimulus window** predicted immediate within-person reaction-speed variation better than every longer tested window under the same feature/model family.

| Passive ocular window | Population macro-r |
| ---: | ---: |
| **2 s** | **0.2742** |
| 5 s | 0.2033 |
| 15 s | 0.1399 |
| 30 s | 0.1177 |
| 60 s | 0.0909 |

The paired 2 s − 5 s macro-r difference was **+0.0709**, with bootstrap 95% CI **[+0.0424,+0.1010]**.

This is exploratory and dataset-specific, but it gives Lucent its first real-data evidence for a **temporal-locality principle**: for an immediate functional target, older ocular history may dilute the most state-proximal signal.

Full result: [results/MTS_REALDATA_001.md](results/MTS_REALDATA_001.md)

## Fourth computational result: redundancy stress test

APST5-SIM-004 removes the clean additive-information assumption from the multimodal result.

Let \(\kappa\) be the fraction of the weaker channel that remains genuinely incremental after overlap with the stronger channel.

For the **3-second concurrent scan**:

| Incremental fraction \(\kappa\) | Cells beating 5 s pupil-only | Median ratio |
| ---: | ---: | ---: |
| 1.00 | 72/80 | **1.238x** |
| 0.75 | 72/80 | **1.176x** |
| 0.50 | 63/80 | **1.112x** |
| 0.25 | 55/80 | **1.048x** |
| 0.00 | 37/80 | 0.983x |

The 3-second design remains above the 5-second pupil-only comparator in the **median** even when only 25% of the weaker channel is allowed to count as incremental information.

This makes **3 seconds** the more robust empirical target under the current model family.

Full result: [results/APST5_SIMULATION_004.md](results/APST5_SIMULATION_004.md)

## Empirical result: temporal-scale audit

Lucent's strongest public-human-data result is a **preregistered target-history crossover with explicit failed replications**, not a universal duration rule.

In **MTS-TARGET-SMOOTHING-001**, the human dataset, ocular signal, feature family, Ridge model, LOSO protocol, and event intersection were held fixed while only the behavioral target horizon was changed.

| Target support | 2 s sensor | 5 s | 15 s | 30 s | 60 s |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 s | **0.2700** | 0.1975 | 0.1199 | 0.0968 | 0.0744 |
| 60 s | 0.1559 | 0.1607 | 0.1712 | 0.1953 | **0.2042** |

The preregistered long-vs-short interaction was **+0.2439**, with paired-subject bootstrap 95% CI **[+0.1647,+0.3191]** across 28 subjects.

A separate preregistered nuisance audit gave every duration model the same time-on-task, squared time-on-task, and session-identity covariates. The crossover remained significant:

- adjusted interaction: **+0.2056**
- 95% CI: **[+0.1328,+0.2749]**

But the directional interaction failed to replicate twice:

| Replication | Interaction | 95% CI | Decision |
| --- | ---: | ---: | --- |
| Martin independent PVT / pupil cohort | **-0.0264** | [-0.0815,+0.0281] | not supported |
| CogBeacon / facial landmarks | **-0.0645** | [-0.1665,+0.0313] | not supported |

The current conclusion is intentionally narrower:

> **sensor-history length and behavioral target horizon are separate design axes, and their interaction can reverse the preferred sensing window in a specific signal × target × protocol system. The sign is not universal.**

This is consistent with recent theory arguing that label construction and latent temporal dynamics jointly determine the useful observation span. Lucent's contribution is the controlled empirical factorization, preregistration, nuisance audit, and retained replication failures—not the generic claim that temporal scale matters.

Replication/falsification synthesis: [TEMPORAL-SCALE-AUDIT-001](results/TEMPORAL_SCALE_AUDIT_001.md)

Original crossover: [MTS-TARGET-SMOOTHING-001](results/MTS_TARGET_SMOOTHING_001.md)

Nuisance audit: [MTS-TEMPORAL-ALIGNMENT-NUISANCE-001](results/MTS_TEMPORAL_ALIGNMENT_NUISANCE_001.md)

Independent PVT replication: [MARTIN-PVT-TARGET-ALIGNMENT-001](results/MARTIN_PVT_TARGET_ALIGNMENT_001.md)

CogBeacon interaction replication: [COGBEACON-TARGET-ALIGNMENT-001](results/COGBEACON_TARGET_ALIGNMENT_001.md)

Related-work boundary: [docs/TEMPORAL_ALIGNMENT_RELATED_WORK.md](docs/TEMPORAL_ALIGNMENT_RELATED_WORK.md)

## Camera-robust observability stress test

APST5-SIM-005 asks a narrower engineering question before the phone pilot:

> if the delayed pupil-response surrogate is approximately right, does ordinary phone-camera sampling destroy the matched-exposure split-vs-contiguous timing signal?

The search modeled 60/30/24 FPS cameras, timestamp jitter, frame drops, and increasing fractional-pupil observation noise. Probe selection maximized the **10th-percentile** separation ratio on a design population, then evaluation used 500 fresh synthetic people.

| Sequence | Held-out P10 separation S | Median S | Cells with S > 1.25 |
| --- | ---: | ---: | ---: |
| robust search winner (1,2,9) | **11.590** | 26.291 | 100% |
| frozen E002 (1,2,8) | **11.272** | 25.822 | 100% |
| evenly spaced (2,5,8) | 6.791 | 15.486 | 100% |

Even in the predeclared stressed 24 FPS / jitter / dropout / noise scenario, the frozen E002 sequence retained P10 S = **9.062**.

This strongly reduces one model-level failure mode: **camera cadence alone should not erase the predicted split-vs-contiguous waveform difference under the committed surrogate**.

It does **not** clear E002. Real RGB pupil extraction may be much noisier or systematically biased, and real pupils may violate the surrogate.

Full result: [APST5-SIM-005](results/APST5_SIMULATION_005.md)

## Human-calibrated active-response bridge

The next audit replaced the hand-specified pupil surrogate with **public human controlled-luminance data**.

### Confirmatory test: failed

APST5-HUMAN-PRF-001 estimated participant-specific empirical pupil step responses from the PsPM-AOB_UW EyeLink dataset, searched all 84 equal-exposure timings on a design half, and evaluated on held-out participants.

The preregistered single-kernel model **did not support** the frozen E002 sequence:

- held-out P10 separation \(S\): **0.824**
- held-out median \(S\): **1.059**
- participants with \(S>1.25\): **27.3%**

That negative result is retained.

### Secondary asymmetry test

A predeclared post-primary analysis then modeled **brightening and darkening with separate human response kernels**. This is secondary evidence, not a confirmatory rescue.

The design-set search selected **exactly the already frozen E002 timing (1,2,8)**.

| Human-calibrated directional model | Held-out P10 S | Median S | S>1.25 |
| --- | ---: | ---: | ---: |
| **frozen E002 (1,2,8)** | **1.264** | **1.836** | **90.9%** |
| SIM-005 (1,2,9) | 1.238 | 1.844 | 81.8% |
| evenly spaced (2,5,8) | 1.099 | 1.543 | 72.7% |

A separate held-out adequacy audit found positive pooled two-transition \(R^2\) for **17/22 participants**, with median participant pooled \(R^2=0.3147\). Sampling the frozen E002 waveform at 50, 30, and 24 Hz left its held-out P10 separation essentially unchanged (**1.264, 1.263, 1.263**).

### Independent lower-cost video-eye-tracker bridge

EHINGER-DEVICE-TRANSFER-001 then used concurrent EyeLink 1000 and Pupil Labs recordings from an independent public controlled-luminance dataset.

With blocks 1–3 used for participant-specific device calibration and blocks 4–6 held out:

- **15/15** participants had held-out cross-device waveform \(r>0.70\);
- Fisher-z macro-\(r\): **0.9974**
- participant-bootstrap 95% CI: **[0.9948,0.9987]**
- median held-out NRMSE: **0.0217**

Because a generic stimulus-locked waveform could inflate that result, a secondary negative control subtracted leave-one-person-out group waveforms. Same-person residual dynamics still transferred across devices:

- residual macro-\(r\): **+0.8910**
- mismatched-person null median: **-0.0551**
- null 95% interval: **[-0.1941,+0.0846]**
- empirical \(p=0.000100\)

This closes part of the model-to-hardware gap, but **Pupil Labs is a dedicated eye tracker, not an ordinary RGB phone camera**. E002 remains open.

Full synthesis: [APST5-HUMAN-CALIBRATION-001](results/APST5_HUMAN_CALIBRATION_001.md)

## Why active probing is different

Passive five-second face-video drowsiness inference is already prior art. Smartphone pupillometry is prior art. Controlled screen-evoked pupil responses are prior art. Active ocular probing is also prior art.

The broader idea that a **structured active perturbation can make wearable physiology more informative** is also prior art: Truslow et al. (2026) reported that a one-minute Apple Watch mindful-breathing perturbation improved HRV discrimination across seven cardiometabolic targets while passive timing/sleep contexts did not.

Lucent therefore does not claim novelty for active perturbation as a general principle.

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
| [results/APST5_SIMULATION_003.md](results/APST5_SIMULATION_003.md) | concurrent pupil + pursuit temporal-compression result |
| [results/APST5_SIMULATION_004.md](results/APST5_SIMULATION_004.md) | multimodal redundancy stress test |
| [results/APST5_HUMAN_CALIBRATION_001.md](results/APST5_HUMAN_CALIBRATION_001.md) | public-human active-response and device-transfer synthesis |
| [results/APST5_HUMAN_PRF_001.md](results/APST5_HUMAN_PRF_001.md) | failed preregistered human-calibrated probe test |
| [results/APST5_HUMAN_PRF_001_SECONDARY.md](results/APST5_HUMAN_PRF_001_SECONDARY.md) | secondary directional human-response result |
| [results/EHINGER_DEVICE_TRANSFER_001.md](results/EHINGER_DEVICE_TRANSFER_001.md) | preregistered lower-cost eye-tracker transfer result |
| [results/MTS_REALDATA_001.md](results/MTS_REALDATA_001.md) | public human-data temporal-locality analysis |
| [results/MTS_TARGET_SMOOTHING_001.md](results/MTS_TARGET_SMOOTHING_001.md) | preregistered direct Temporal Alignment test |
| [results/TEMPORAL_ALIGNMENT_001.md](results/TEMPORAL_ALIGNMENT_001.md) | synthesis across direct manipulation + independent boundary datasets |
| [results/ADHD_REALDATA_001.md](results/ADHD_REALDATA_001.md) | preregistered independent duration reversal |
| [results/COGBEACON_TARGET_ALIGNMENT_001.md](results/COGBEACON_TARGET_ALIGNMENT_001.md) | preregistered failed cross-task interaction replication |
| [results/MARTIN_PVT_TARGET_ALIGNMENT_001.md](results/MARTIN_PVT_TARGET_ALIGNMENT_001.md) | preregistered failed independent PVT interaction replication |
| [results/MTS_TEMPORAL_ALIGNMENT_NUISANCE_001.md](results/MTS_TEMPORAL_ALIGNMENT_NUISANCE_001.md) | preregistered time-on-task/session nuisance audit |
| [results/TEMPORAL_SCALE_AUDIT_001.md](results/TEMPORAL_SCALE_AUDIT_001.md) | replication and falsification synthesis |
| [docs/TEMPORAL_ALIGNMENT_RELATED_WORK.md](docs/TEMPORAL_ALIGNMENT_RELATED_WORK.md) | closest prior art and conservative novelty boundary |
| [docs/BASELINE_COMPRESSION.md](docs/BASELINE_COMPRESSION.md) | nuisance-projection derivation and design principle |
| [docs/MULTIMODAL_COMPRESSION.md](docs/MULTIMODAL_COMPRESSION.md) | closest 30–45 s ocular screens and the open ~5 s compression target |

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

**Five simulation/stress-test results, a mixed preregistered temporal-scale replication record, a failed confirmatory human active-response test with a positive directional secondary, and a preregistered cross-device pupil-waveform transfer result; ordinary-RGB-phone validation is still pending.**

The current evidence now reaches beyond simulation: human controlled-luminance data show that brightening/darkening asymmetry materially changes probe ranking, and an independent lower-cost dedicated video eye tracker preserves luminance-evoked and person-specific pupil dynamics relative to EyeLink. The confirmatory human E002 model still failed, and none of this establishes ordinary RGB-phone observability or state prediction. **The next decisive step remains the frozen synchronized E002 phone capture study.**
