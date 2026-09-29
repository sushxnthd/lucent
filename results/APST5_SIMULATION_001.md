# APST5-SIM-001: Equal-Exposure Active Probe Design

**Status:** reproduced computational result; human validation not yet performed.

## Question

Under a fixed five-second scan and identical total high-luminance exposure, can stimulus timing change how well a short pupil response identifies its underlying dynamics?

## Model

The experiment uses a deliberately simple delayed asymmetric pupil-response surrogate with five parameters:

1. baseline pupil diameter;
2. luminance-response gain;
3. response latency;
4. constriction time constant;
5. dilation time constant.

Baseline diameter is treated as nuisance. The Bayesian design objective measures local information gain about the four dynamic parameters.

The simulator is literature-inspired rather than claimed as a validated biological digital twin.

## Constraint

Every candidate:

- lasts 5.0 s;
- uses 0.5 s segments;
- starts low;
- contains exactly three high-luminance segments;
- uses exactly the same low and high levels;
- therefore has exactly the same total high-luminance exposure.

There are:

\[
\binom{9}{3}=84
\]

candidate timing patterns.

## Design / test separation

The probe is selected using 32 synthetic parameter draws.

The chosen sequence is then evaluated on **500 fresh draws** sampled from a wider parameter distribution with a different random seed.

This prevents reporting the same simulated population used for optimization.

## Selected design

High segments:

\`\`\`text
(1, 2, 8)
\`\`\`

Timeline:

\`\`\`text
segment        0    1    2    3    4    5    6    7    8    9
time (s)       0   .5  1.0  1.5  2.0  2.5  3.0  3.5  4.0  4.5
stimulus      low HIGH HIGH  low  low  low  low  low HIGH  low
\`\`\`

The normalized luminance mapping used by the surrogate corresponds approximately to:

\`\`\`text
[1.7, 153.5, 153.5, 1.7, 1.7, 1.7, 1.7, 1.7, 153.5, 1.7] cd/m^2
\`\`\`

These are simulation levels, not a human-use recommendation.

## Held-out result

| Probe | Mean IG | SD | P10 | Median | P90 |
| --- | ---: | ---: | ---: | ---: | ---: |
| optimized split pulse | **11.987** | 0.840 | 10.915 | 11.956 | 13.036 |
| best contiguous pulse | 11.687 | 0.886 | 10.582 | 11.657 | 12.751 |
| evenly spaced | 10.646 | 0.910 | 9.496 | 10.586 | 11.730 |

The best contiguous design used high segments (4, 5, 6).

### Relative effect

Optimized vs best contiguous:

- expected information gain: **+2.57%**;
- log-determinant difference: **0.301 nats**;
- corresponding posterior covariance-volume ratio: approximately **1.82x** in favor of the optimized sequence.

Optimized vs evenly spaced:

- expected information gain: **+12.60%**.

## Interpretation

The result is more interesting than "brighter is better" because the high-luminance dose is matched exactly.

The winning pattern suggests that, under the surrogate, a useful short experiment may need:

1. an early excitation;
2. enough recovery time for slow dynamics to become visible;
3. a late re-excitation that probes the partially recovered system.

That structure separates dynamic parameters better than placing the entire exposure in one block.

## What this result does not show

It does not show that:

- the same sequence is optimal for real pupils;
- 153.5 cd/m² is the right or safe human stimulus;
- pupil dynamics alone reveal fatigue;
- five seconds is sufficient for a usable product;
- the surrogate's parameter prior matches the population.

## Next falsification experiment

A human pilot should compare at minimum:

1. passive 5 s;
2. matched-exposure contiguous active probe;
3. matched-exposure split active probe;
4. paired psychomotor / state-sleepiness targets.

The split-pulse advantage is a **pre-registered prediction**. If it disappears on real hardware or real people, the current model-design result has failed to transfer.

## Reproduction

\`\`\`bash
pip install -e ".[dev]"
python experiments/active_probe_design.py
\`\`\`

The random seeds and parameter bounds are committed in the experiment code.
