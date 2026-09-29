# Multimodal Compression: Why APST-5 Should Probe More Than the Pupil

A second Lucent literature search focused specifically on ultra-short combined ocular tests.

## Closest precedent

The closest located fatigue-screening precedent is not five seconds.

**Mulligan, Díaz-Piedra & Di Stasi (2017)** evaluated a **30-second** automated oculomotor test that measured:

- saccadic peak velocity;
- pupil diameter;
- pupil-light-reflex latency;
- pupil-light-reflex amplitude.

https://doi.org/10.1167/17.10.1153

A related sleep-deprivation study by Rowland et al. used a **45-second** automated oculomotor test and reported:

- increased latency to pupil constriction;
- decreased saccadic velocity;
- correlations between those changes, sleepiness, and driving impairment.

The closest smartphone literature generally validates the required modalities separately.

**Lai et al. (2020)** showed smartphone-camera measurement of saccade latency, but reliable mean-latency estimation required many measurements rather than an ultra-short state scan.

https://doi.org/10.1109/JBHI.2019.2913846

**Podolak et al. (2019)** used a 0.8-second light stimulus with a five-second PLR recording window, but performed multiple trials and targeted concussion rather than fatigue/cognitive state.

https://doi.org/10.1177/2325967119S00155

**Bruce et al. (2025)** reported useful test-retest reliability for a phone PLR app with two trials, including high latency reliability, but did not establish an integrated fatigue-state classifier.

https://doi.org/10.1123/ijatt.2024-0085

## Search result

The literature search did **not** locate a validated approximately five-second test that jointly:

1. controls luminance / color to elicit pupil dynamics;
2. controls spatial targets to elicit saccade or pursuit dynamics;
3. records both through an ordinary smartphone;
4. optimizes the sequence for state separability;
5. conditions inference on a personal longitudinal baseline.

That is narrower than claiming that combined ocular fatigue measurement is new. It is not.

The research gap is **temporal compression + smartphone implementation + active sequence design + longitudinal nuisance cancellation**.

## Why combine channels?

Fatigue does not have one universal ocular signature.

Different studies report sensitivity in different components:

- constriction latency;
- pupil diameter;
- constriction / redilation dynamics;
- saccadic peak velocity;
- pursuit gain;
- direction / speed noise;
- blink and eyelid dynamics.

This argues against betting the entire five-second budget on one response family.

The APST-5 extension should therefore treat the screen as a **multi-input experimental instrument**:

\[
u_t = (L_t,\ C_t,\ q_t),
\]

where:

- \(L_t\) is luminance / chromatic drive;
- \(C_t\) is spatial target location or motion;
- \(q_t\) is task instruction / response context.

The observation can contain:

\[
y_t = (p_t,\ g_t,\ e_t,\ f_t),
\]

where:

- \(p_t\): pupil dynamics;
- \(g_t\): gaze / saccade dynamics;
- \(e_t\): eyelid / blink dynamics;
- \(f_t\): optional facial dynamics.

The experimental-design problem is then to choose a sequence that maximizes **state information after nuisance projection**, not to maximize the accuracy of any one biomarker.

## Falsifiable compression target

The strongest immediate target is:

> reproduce or exceed the state information of a substantially longer combined ocular screen with a five-second, baseline-conditioned, smartphone-native active sequence.

That requires human data. The repository does not claim this has been achieved.

The literature review only establishes that the compression target appears to remain open.
