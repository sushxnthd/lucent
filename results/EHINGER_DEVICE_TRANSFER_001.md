# EHINGER-DEVICE-TRANSFER-001: Concurrent Lower-Cost Eye-Tracker Transfer

**Status:** completed preregistered public-human cross-device analysis.

**Primary waveform-preservation criterion:** **SUPPORTED**.

## Frozen design

Concurrent EyeLink 1000 and Pupil Labs measurements from the public Ehinger et al. controlled-luminance task.

- usable participants: **15**
- calibration blocks: **1–3**
- held-out blocks: **4–6**
- fixed post-onset window: **0–2.8 s**
- per-participant calibration: EyeLink = a + b × Pupil Labs, fit only on blocks 1–3

## Participant-level held-out results

| participant | calibrated r | uncalibrated r | NRMSE | late-amplitude r | nonzero-luminance r |
| --- | ---: | ---: | ---: | ---: | ---: |
| VP1 | **0.9977** | 0.9977 | 0.0316 | 0.9992 | 0.9946 |
| VP11 | **0.9987** | 0.9987 | 0.0166 | 0.9989 | 0.9953 |
| VP12 | **0.9936** | 0.9936 | 0.0376 | 0.9977 | 0.9669 |
| VP14 | **0.9981** | 0.9981 | 0.0205 | 0.9995 | 0.9962 |
| VP15 | **0.9994** | 0.9994 | 0.0121 | 0.9996 | 0.9984 |
| VP19 | **0.9957** | 0.9957 | 0.0301 | 0.9959 | 0.9848 |
| VP2 | **0.9998** | 0.9998 | 0.0367 | 0.9998 | 0.9993 |
| VP20 | **0.9981** | 0.9981 | 0.0195 | 0.9984 | 0.9926 |
| VP22 | **0.9366** | 0.9366 | 0.1128 | 0.9470 | 0.8149 |
| VP23 | **0.9986** | 0.9986 | 0.0189 | 0.9993 | 0.9947 |
| VP24 | **0.9984** | 0.9984 | 0.0173 | 0.9991 | 0.9943 |
| VP25 | **0.9807** | 0.9807 | 0.0665 | 0.9829 | 0.9441 |
| VP26 | **0.9991** | 0.9991 | 0.0143 | 0.9996 | 0.9969 |
| VP3 | **0.9979** | 0.9979 | 0.0217 | 0.9986 | 0.9910 |
| VP4 | **0.9934** | 0.9934 | 0.0390 | 0.9955 | 0.9719 |

## Preregistered aggregate

- Fisher-z macro-r: **0.9974**
- participant bootstrap 95% CI: **[0.9948, 0.9987]**
- participants with held-out r > 0.70: **100.0% (15/15)**
- median held-out NRMSE: **0.0217**

Frozen support requires CI lower bound >0.70 and >=80% of participants with individual held-out r>0.70.

**Decision: supported.**

## Per-luminance secondary agreement

| luminance code | macro calibrated r |
| ---: | ---: |
| 0 | 0.9943 |
| 64 | 0.9869 |
| 128 | 0.9927 |
| 192 | 0.9957 |
| 255 | 0.9970 |

## Secondary summaries

- median participant late-response amplitude correlation: **0.9989**
- macro-r restricted to nonzero luminance codes: **0.9914**
- macro uncalibrated waveform r: **0.9974**

## Interpretation

After a simple participant-specific affine calibration learned only on the first three blocks, the lower-cost Pupil Labs system preserved the concurrent EyeLink luminance-evoked waveform structure in held-out blocks under the frozen criterion.

## Claim boundary

Pupil Labs is a dedicated video eye tracker, not an ordinary RGB smartphone front camera. This result therefore cannot clear Lucent E002 or establish phone-based pupil observability.
