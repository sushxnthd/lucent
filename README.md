# Lucent

> **Ultra-short active sensing of fatigue and cognitive-performance state with ordinary phone hardware.**

[![research-ci](https://github.com/sushxnthd/lucent/actions/workflows/ci.yml/badge.svg)](https://github.com/sushxnthd/lucent/actions/workflows/ci.yml)
[![public-realdata](https://github.com/sushxnthd/lucent/actions/workflows/realdata.yml/badge.svg)](https://github.com/sushxnthd/lucent/actions/workflows/realdata.yml)

Lucent is a research program asking a narrow question:

> **How much state information can a phone recover in roughly 2–5 seconds if it actively designs the measurement instead of merely watching a face?**

The display is treated as a controlled experimental input. The front camera is the response sensor. Longitudinal history is treated as prior information about the person rather than forcing every scan to start from zero.

Lucent grew out of [Somno](https://sushxnthd.github.io/somno/), where repeated explicit tests exposed the central product problem: a measurement can be scientifically useful and still fail in practice if people have to stop and perform it every day.

This repository is intentionally **research-only**. It contains hypotheses, mathematical models, public-data analyses, simulation experiments, failure criteria, preregistrations, and reproducible code. It contains no product UI.

## Evidence ledger

| ID | Evidence layer | Main result | Status |
| --- | --- | --- | --- |
| [APST5-SIM-001](results/APST5_SIMULATION_001.md) | in-silico experimental design | equal-exposure stimulus timing improved pupil-system identifiability; optimized probe +2.57% vs best contiguous pulse | **reproduced** |
| [APST5-SIM-002](results/APST5_SIMULATION_002.md) | in-silico state design | 2 s + tighter nuisance prior exceeded 5 s population measurement in 10/10 held-out synthetic replications | **reproduced** |
| [APST5-SIM-003](results/APST5_SIMULATION_003.md) | multimodal sensitivity analysis | 3 s concurrent pupil+pursuit beat 5 s pupil-only in 72/80 uncertainty-grid cells; median 1.238x | **reproduced** |
| [APST5-SIM-004](results/APST5_SIMULATION_004.md) | redundancy stress test | at only 25% incremental weaker-channel information, 3 s still beat 5 s in 55/80 cells; median 1.048x | **reproduced** |
| [MTS-REALDATA-001](results/MTS_REALDATA_001.md) | public human ocular + PVT data | 2 s pre-stimulus eyelid features were stronger than 5–60 s for the same immediate RT target; personalization primary was null | **mixed / exploratory positive** |

The important distinction is deliberate:

**The computational active-sensing results are not human validation.**

The public human-data result is real-data evidence for **temporal locality of passive ocular state**, not evidence that APST-5 active probing already works in people.

See [CLAIM_LEDGER.md](docs/CLAIM_LEDGER.md) for the exact claim boundary.

## The current architecture: APST-5

**APST-5 = Active Personalized State Tomography in Five Seconds.**

Let:

- x(t): latent physiological / functional state;
- u(t): known screen stimulus;
- y(t): camera-visible ocular / facial response;
- h(i): longitudinal history for person i;
- d(i): device and environment nuisance.

The measurement problem is:

[
p(x_T \mid y_{0:T}, u_{0:T}, h_i)
]

and the probe itself is a design variable:

[
u^*
=
\arg\max_u
\mathbb{E}[I(X;Y\mid U=u,H_i)]
-
\lambda C(u).
]

C(u) represents duration, exposure, transition, comfort, and hardware constraints.

The current direction is **concurrent multimodal probing**: use the same few seconds to elicit pupil dynamics and controlled gaze/pursuit dynamics rather than running those tests serially.

## The strongest real-data observation so far

[MTS-REALDATA-001](results/MTS_REALDATA_001.md) re-analyzed public eyelid-distance + Psychomotor Vigilance Test data from 28 usable subjects under strict leave-one-subject-out evaluation.

The target was kept fixed: **the immediate next within-person PVT reaction-speed deviation**.

| Pre-stimulus window | Population macro-r | Personalized macro-r |
| ---: | ---: | ---: |
| **2 s** | **0.2742** | **0.2841** |
| 5 s | 0.2033 | 0.2097 |
| 15 s | 0.1399 | 0.1511 |
| 30 s | 0.1177 | 0.1199 |
| 60 s | 0.0909 | 0.1224 |

The preregistered personalization comparison at 5 s was **null**:

[
\Delta r = +0.0064,qquad
95\%\ CI=[-0.0169,+0.0295].
]

After that primary result was observed, explicitly post-hoc paired duration contrasts found:

[
r_{2s}-r_{5s}=+0.0709,
qquad
95\%\ CI=[+0.0424,+0.1010]
]

in the population-normalized condition, with the 2 s advantage also present against 15, 30, and 60 s.

That is an exploratory result requiring independent replication. It nevertheless gives Lucent a concrete empirical design clue: **for an immediate functional target, stale history can dilute state-proximal ocular information.**

See [Temporal Locality Principle](docs/TEMPORAL_LOCALITY.md).

## Why 3 seconds is now the stronger active target

APST5-SIM-003 and APST5-SIM-004 ask whether pupil and smooth-pursuit information can be acquired **concurrently**.

Five-second pupil-only comparator:

[
IG=0.392970	ext{ nats}.
]

For a 3 s concurrent scan:

- additive envelope: **72/80** grid cells beat the 5 s comparator; median **1.238x**;
- 50% incremental weaker-channel information: **63/80** wins; median **1.112x**;
- 25% incremental weaker-channel information: **55/80** wins; median **1.048x**.

So the present model family no longer points to “five seconds” as sacred. It points to a more general target:

> **maximize state information density per second.**

Three seconds is currently the most defensible next empirical active-probe duration because its modeled advantage survives substantial cross-channel redundancy.

## Research progression

~~~text
Somno
  |
  | explicit testing exposes friction
  v
passive ultra-short sensing
  |
  | MTS-REALDATA-001: recent 2 s > longer passive history
  v
APST-5 active probing
  |
  +--> SIM-001: optimize stimulus timing
  |
  +--> SIM-002: use personal history to cancel stable nuisance
  |
  +--> SIM-003: probe pupil + pursuit concurrently
  |
  +--> SIM-004: stress-test cross-channel redundancy
  v
commodity-phone observability
  v
preregistered paired human study
  v
unseen-person + unseen-device replication
~~~

## What would count as the breakthrough?

A strong empirical claim requires all of the following:

1. an ordinary phone executes the active probe with usable timing fidelity;
2. concurrent active 2–5 s sensing beats passive sensing at the same duration;
3. optimized active probing beats a matched fixed active probe;
4. the signal predicts a paired behavioral target on unseen people;
5. the gain survives device/environment shifts;
6. the result reproduces on a fresh cohort with a frozen analysis.

Until then, Lucent is a **breakthrough candidate with converging design evidence**, not a validated two-second fatigue detector.

## Reproduce

Install:

~~~bash
git clone https://github.com/sushxnthd/lucent.git
cd lucent
python -m venv .venv
pip install -e ".[dev]"
pytest
~~~

Core computational results:

~~~bash
python experiments/active_probe_design.py
python experiments/personalization_compression.py
python experiments/multimodal_compression.py
python experiments/multimodal_redundancy.py
~~~

Public human-data result:

~~~bash
python experiments/inspect_mts_data.py
python experiments/mts_realdata_baseline_compression.py
~~~

The public-data workflow downloads the source data from the original Massoz et al. repository at run time; participant data are not copied into Lucent.

## Research map

| Path | Purpose |
| --- | --- |
| [APST5.md](APST5.md) | active-probing thesis |
| [RESEARCH.md](RESEARCH.md) | hypotheses and evidence ladder |
| [ROADMAP.md](ROADMAP.md) | remaining empirical gates |
| [REFERENCES.md](REFERENCES.md) | closest prior art |
| [docs/CLAIM_LEDGER.md](docs/CLAIM_LEDGER.md) | exact supported / unsupported claims |
| [docs/BASELINE_COMPRESSION.md](docs/BASELINE_COMPRESSION.md) | personalization-as-sensing-time derivation |
| [docs/MULTIMODAL_INFORMATION.md](docs/MULTIMODAL_INFORMATION.md) | concurrent-channel information model |
| [docs/MULTIMODAL_COMPRESSION.md](docs/MULTIMODAL_COMPRESSION.md) | prior-art boundary for short combined ocular screens |
| [docs/TEMPORAL_LOCALITY.md](docs/TEMPORAL_LOCALITY.md) | why more historical sensor data can hurt an immediate target |
| [docs/FAILURE_MODES.md](docs/FAILURE_MODES.md) | shortcut / leakage threat model |
| [experiments/registrations/MTS_REALDATA_001.md](experiments/registrations/MTS_REALDATA_001.md) | frozen public-data preregistration |
| [results/](results/) | complete positive and null results |

## Research rules

- **Perturb, do not merely observe.**
- **Keep the target fixed when comparing measurement durations.**
- **Match exposure before comparing active probes.**
- **Split by person before reporting generalization.**
- **Optimize on one population, evaluate on another.**
- **Treat personal history as prior information, never future leakage.**
- **Publish null results.**
- **Do not turn a simulation into a biological claim.**
