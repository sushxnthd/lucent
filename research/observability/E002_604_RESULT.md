# E002-604 | Shutter integration can conceal a true full closure at every phase

Date: 2026-11-02. Parent E002-371. Evidence tier: **SYNTHETIC_PHYSICAL_MEASUREMENT_MODEL_ONLY**. [Precommitted protocol](E002_604_FROZEN.md) at `da9180b` precedes code and results.

## Question
Previous E002-595/596 phase-index audits treat sampled frames as instantaneous observations. A camera integrates light during an exposure. Can the *measured exposure-average* stay unambiguously open even when the true underlying aperture reaches zero? Yes, in a simple idealized global-shutter oracle.

## Instrument and exact law
Let normalized anatomical aperture be `a(t)=1-max(0,1-2|t|/w)`. This is a symmetric triangular closure reaching zero at `t=0` with duration `w=10 ms` and assumed Lipschitz ceiling `2/w=200 aperture units/s`. A hypothetical ideal global-shutter camera returns the average `y(c)=integral_{c-E/2}^{c+E/2}a(t)dt/E`. The exact minimum over all shutter centers is

```
min_c y(c) = E/(2w)           if E <= w
           = 1 - w/(2E)      if E >= w.
```

The integrated aperture can remain above a closure decision threshold even when the true aperture reaches zero. This is an exposure-integration ambiguity, **not** an empirical estimate of human eyelid velocity.

## Local falsification results
Python piecewise-analytic integration and a separately written JavaScript breakpoint/trapezoid integrator agreed on all precommitted minima and on 10,000 deterministic phase positions per condition.

| Exposure E | Exact minimum averaged aperture | Independent JS |
|---|---:|---:|
| 2 ms | 0.10 | 0.10 |
| 5 ms | 0.25 | 0.25 |
| 10 ms | 0.50 | 0.50 |
| 20 ms | 0.75 | 0.75 |

With closure decision threshold `y <= 0.2`:

| Hypothetical camera | Exposure | Phases missing true closure: shutter average | Phases missing: instantaneous point sample |
|---|---:|---:|---:|
| 30 fps | 20 ms | 100% | 94% |
| 95 fps | 5 ms | 100% | 81% |
| 95 fps | 2 ms | 81% | 81% |

These percentages are exhaustive grid fractions over 10,000 phase positions of one *constructed* trajectory, not probabilities of real blinks. The 30/95-fps exposure durations are assumptions, **not** verified metadata for LPW or any phone camera. The 95-fps 2-ms example is a sensitivity control.

## Independent validation and reproducibility
- [Python executable](e002_604_shutter_alias.py): direct antiderivative of triangular deficit, deterministic 10,000-phase sweep and asserted predictions.
- [Independent JavaScript replay](e002_604_shutter_alias_independent.js): geometric trapezoid integration across breakpoints and independent phase enumeration.
- Run from `research/observability`: `python e002_604_shutter_alias.py` and `node e002_604_shutter_alias_independent.js`.
- At initial report commit, **local** execution passed; hosted CI remains unverified until an exact-head workflow run is checked.

## Dataset and priority boundary
Fresh source review identified [Silesian5](https://www.blinkingmatters.com/research) (Basler 100 fps, five subjects, 300 blink events, framewise fully-closed flags) as a stronger *event-labeled* external test than LPW pupil-center labels. Access to the converted video requires a signed license and researcher permission; no Silesian5 frames were obtained or tested. [OpenEDS](https://arxiv.org/abs/1905.03702) describes 200-Hz eye-facing sequences, but access is by request and its published segmentation labels are not a continuous eyelid-margin ground truth. [RT-BENE](https://open.qcr.ai/dataset/rt_bene_dataset/) has expert open/closed/uncertain image labels, but these alone do not establish high-speed temporal sampling or a velocity ceiling. No claim of priority for the integration law is made; camera exposure integration is standard measurement physics. The scientific value here is a concrete falsifier of a potential **Lucent product inference**.

## Product consequence and missing evidence
An observed high exposure-average cannot certify that an eye was never closed during the shutter interval, even under ideal geometry and noiseless anatomical measurement. E002-371's point-observation certification must be **disabled** whenever actual shutter timing and the observation operator are not independently calibrated. Do not extrapolate these synthetic miss fractions to human blink performance.

This experiment does not address rolling shutter, gamma, sensor noise, blur, occlusion, glasses, gaze, missing frames, registration, timestamp errors or anatomical uncertainty. Their absence strengthens the impossibility witness but does not provide a real-camera validation. No independent human anatomical rater, calibrated shutter or clock, physiologically justified continuous-time velocity bound, or held-out physical closure prediction was obtained. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
