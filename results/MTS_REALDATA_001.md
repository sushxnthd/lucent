# MTS-REALDATA-001: Ultra-Short Pre-Stimulus Ocular State

**Status:** completed public-data analysis.

**Primary preregistered personalization hypothesis:** **not supported.**

**Exploratory temporal-locality result:** a 2-second pre-stimulus eyelid window predicted immediate within-person vigilance variation more strongly than 5-, 15-, 30-, or 60-second windows under the same feature/model family.

## Source

This analysis uses the public eyelid-distance sequences and PVT reaction-time logs released with:

Q. Massoz, J. G. Verly, M. Van Droogenbroeck,  
*Multi-Timescale Drowsiness Characterization Based on a Video of a Driver's Face.*  
Sensors 18(9):2801, 2018.  
https://doi.org/10.3390/s18092801

Source repository: https://github.com/QMassoz/mts-drowsiness

Lucent does not redistribute the underlying participant data.

## Frozen design

The full plan was committed before the result was run:

[experiments/registrations/MTS_REALDATA_001.md](../experiments/registrations/MTS_REALDATA_001.md)

Key choices:

- 28 usable subjects from the authors' LOSO cohort;
- PVT1 used only as a chronologically earlier reference session;
- PVT2/PVT3 used for held-forward evaluation;
- ocular features taken strictly **before** each PVT stimulus;
- target = within-person standardized reciprocal reaction speed;
- durations fixed in advance at 2, 5, 15, 30, and 60 seconds;
- StandardScaler + Ridge(\(\alpha=10\));
- strict leave-one-subject-out population training;
- no hyperparameter search;
- primary duration = 5 seconds;
- primary test = personalized 5 s vs population-only 5 s.

## Full duration results

Macro-\(r\) is the Fisher-z-averaged within-subject Pearson correlation across held-out subjects.

| Window | Population macro-r | Personalized macro-r | Samples |
| ---: | ---: | ---: | ---: |
| **2 s** | **0.2742** | **0.2841** | 4,958 |
| 5 s | 0.2033 | 0.2097 | 4,938 |
| 15 s | 0.1399 | 0.1511 | 4,848 |
| 30 s | 0.1177 | 0.1199 | 4,730 |
| 60 s | 0.0909 | 0.1224 | 4,480 |

Pooled correlations showed the same broad pattern:

| Window | Population pooled-r | Personalized pooled-r |
| ---: | ---: | ---: |
| **2 s** | **0.2325** | **0.2518** |
| 5 s | 0.1711 | 0.1831 |
| 15 s | 0.1227 | 0.1316 |
| 30 s | 0.1019 | 0.1294 |
| 60 s | 0.1055 | 0.1102 |

## Preregistered primary result: null

At the preregistered 5-second duration:

\[
r_{\mathrm{personal}} - r_{\mathrm{population}}
=
+0.0064.
\]

Paired subject bootstrap, \(B=10{,}000\):

\[
95\%\ \mathrm{CI}
=
[-0.0169,\ +0.0295].
\]

The interval crosses zero.

Therefore **MTS-REALDATA-001 does not provide confirmatory support for the claim that the chosen PVT1 personalization transform improves five-second vigilance prediction**.

This null result is retained because the repository's purpose is to make claims harder to fool.

## Exploratory result: temporal locality

After the preregistered result had been observed, we added explicitly labeled paired duration contrasts.

These are **post-hoc exploratory analyses**, not the preregistered primary test.

### Population-normalized condition

| Contrast | Macro-r difference | Paired bootstrap 95% CI |
| --- | ---: | ---: |
| 2 s − 5 s | **+0.0709** | **[+0.0424, +0.1010]** |
| 2 s − 15 s | **+0.1343** | **[+0.0858, +0.1842]** |
| 2 s − 30 s | **+0.1565** | **[+0.1058, +0.2053]** |
| 2 s − 60 s | **+0.1833** | **[+0.1249, +0.2432]** |

### Personalized condition

| Contrast | Macro-r difference | Paired bootstrap 95% CI |
| --- | ---: | ---: |
| 2 s − 5 s | **+0.0744** | **[+0.0459, +0.1023]** |
| 2 s − 15 s | **+0.1330** | **[+0.0938, +0.1736]** |
| 2 s − 30 s | **+0.1642** | **[+0.1224, +0.2050]** |
| 2 s − 60 s | **+0.1617** | **[+0.1099, +0.2146]** |

All eight exploratory paired intervals exclude zero.

## Why this is different from the original paper's timescale result

Massoz et al. reported increasing classification accuracy at longer timescales.

That is **not the same analysis**.

Their target changed with timescale:

- the short branch represented near-instantaneous reaction behavior;
- longer branches used reaction-time summaries over correspondingly longer intervals.

MTS-REALDATA-001 instead keeps the target fixed:

> **the immediate next within-person PVT reaction-speed deviation**

and changes only how far backward the ocular window reaches.

Under that fixed immediate target, adding older eyelid history reduced held-out predictive correlation in this simple model.

The result therefore does not contradict the original paper. It isolates a different question: **how local in time is the ocular information relevant to the next vigilance response?**

## Temporal-locality interpretation

One plausible interpretation is **state dilution**.

If the ocular state relevant to an imminent reaction changes on a short timescale, averaging features over 15–60 seconds mixes the current state with increasingly stale observations.

For a transient target, more history is therefore not guaranteed to mean more information.

This motivates a new Lucent design rule:

> **When the target is immediate functional state, spend sensing budget on the most state-proximal seconds rather than indiscriminately averaging a longer past.**

A mathematical statement of this idea is given in [docs/TEMPORAL_LOCALITY.md](../docs/TEMPORAL_LOCALITY.md).

## What this result establishes

Within this public dataset and frozen model family:

- pre-stimulus eyelid dynamics contain modest held-out information about immediate within-person PVT performance;
- the strongest tested passive window was the shortest tested window, **2 seconds**;
- the advantage over every longer tested window was consistent under paired subject bootstrap;
- the chosen simple personalization transform did **not** produce a significant 5-second improvement.

## What it does not establish

It does not show that:

- two seconds is universally optimal;
- a phone can diagnose fatigue in two seconds;
- eyelid distance alone is sufficient for useful real-world deployment;
- APST-5 active probing has been validated in humans;
- the exploratory 2-second result will replicate on a new cohort.

## Next falsification target

The strongest next experiment is now sharper:

1. reproduce the **2-second temporal-locality effect** on a genuinely independent cohort;
2. compare passive 2 s against **concurrent active pupil + gaze probing** at 2–3 s;
3. test whether active probing adds held-out behavioral-state information beyond the passive eyelid signal;
4. only then claim empirical temporal compression.

The public-data result moves Lucent from a purely simulated timing argument to a real-data observation that **very recent ocular behavior can carry more information about immediate performance than a much longer passive history**.
