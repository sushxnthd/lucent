# Lucent Evidence Ledger

This file separates what Lucent has **demonstrated**, what is **secondary/exploratory**, what exists only **in simulation**, and what remains **open**.

A result does not move up an evidence tier because it is numerically large.

| Claim | Evidence | Evaluation | Status | Allowed wording |
| --- | --- | --- | --- | --- |
| equal-exposure probe timing changes information under the APST pupil surrogate | APST5-SIM-001 | held-out synthetic parameter population | **model-supported** | timing matters under the committed surrogate |
| tighter personal nuisance priors can compress modeled sensing time | APST5-SIM-002 | 10 held-out synthetic populations | **model-supported** | personalization can buy modeled sensing time |
| concurrent pupil+pursuit can outperform longer pupil-only scans in the surrogate family | APST5-SIM-003/004 | held-out sensitivity grid + redundancy stress test | **model-supported** | multimodal compression is plausible under tested model assumptions |
| frozen E002 timing survives modeled 24/30/60 FPS sampling, jitter, drops, and noise | APST5-SIM-005 | 500 held-out synthetic people × camera scenarios | **model-supported** | camera cadence alone should not erase the surrogate waveform |
| short vs long passive ocular history can reverse when the target horizon changes | MTS-TARGET-SMOOTHING-001 | preregistered public-human within-dataset manipulation | **supported in one dataset** | a large target-history crossover occurs in Massoz PVT data |
| the Massoz crossover is only trivial time-on-task/session leakage | MTS-TEMPORAL-ALIGNMENT-NUISANCE-001 | preregistered nuisance audit | **not supported by tested nuisance model** | the crossover survives the frozen time/session adjustment |
| the same positive temporal-alignment interaction generalizes | Martin PVT + CogBeacon | preregistered independent replications | **not supported** | interaction sign is not universal |
| one symmetric signed human pupil kernel makes E002 distinguishable | APST5-HUMAN-PRF-001 | preregistered participant-held-out public-human test | **not supported** | the confirmatory human-calibrated E002 model failed |
| separate brightening/darkening human kernels favor frozen E002 timing | APST5-HUMAN-PRF-001 secondary | frozen post-primary design/test analysis | **secondary support** | directional asymmetry is a promising explanation, not confirmatory proof |
| directional human kernels predict unseen complete two-transition trials | APST5-HUMAN-PRF adequacy | held-out repeated transitions | **mixed/moderate secondary support** | 17/22 pooled R2 positive; model remains imperfect |
| controlled-luminance waveforms transfer from EyeLink to Pupil Labs | EHINGER-DEVICE-TRANSFER-001 | preregistered blocks 1–3 calibration, 4–6 held out | **supported** | a dedicated lower-cost video eye tracker preserves the concurrent waveform |
| person-specific response deviations transfer across EyeLink/Pupil Labs | EHINGER secondary specificity | leave-one-person-out residual + 10k mismatched permutations | **secondary support** | person-specific residual structure transfers in this laboratory dataset |
| ordinary RGB phone can resolve E002 split-vs-contiguous pupil dynamics | E002 | frozen prospective phone pilot | **open** | no positive biological phone claim yet |
| any RGB-phone E002 difference is biological rather than camera exposure/segmentation | E002 photometric audit | pre-data negative controls | **open** | must pass brightness/geometry specificity audit |
| E002 dynamics predict vigilance, fatigue, or cognitive performance | later paired human study | not run | **open** | no state-validity claim |
| active five-second phone probing beats passive five seconds | later paired human study | not run | **open** | core breakthrough claim remains untested |
| result generalizes to unseen devices and fresh cohort | phases 4–5 | not run | **open** | no deployment/generalization claim |

## Evidence tiers

### Confirmatory / preregistered

The primary hypothesis, data split, metric, and decision rule were frozen before the relevant outcome was computed.

A failed confirmatory result remains failed even if a later secondary analysis is positive.

### Secondary

The analysis was specified only after an earlier result or after inspecting part of the data structure. It can explain, narrow, or generate a stronger next experiment; it cannot retroactively satisfy a failed primary criterion.

### Model-supported

The result is internally reproducible under explicit assumptions but has not crossed the required human/hardware validation boundary.

### Open

The repo contains a protocol or implementation, but the empirical evidence needed for the claim does not yet exist.

## Current strongest evidence chain

[
	ext{optimized active timing in simulation}
ightarrow
	ext{human luminance-response dynamics}
ightarrow
	ext{dedicated video-eye-tracker transfer}
ightarrow
oxed{	ext{ordinary RGB phone E002}}
ightarrow
oxed{	ext{paired state validity}}
]

The first three links have evidence with different strengths and caveats.

The final two links are still open. They are the reason Lucent is not described as a validated fatigue or cognitive-state measurement system.
