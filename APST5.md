# APST-5: Active Personalized State Tomography in Five Seconds

## Thesis

A smartphone can use its display as a controlled perturbation source and its front camera as a response sensor.

The core hypothesis is:

> A five-second **active** scan can recover more identifiable information about current human state than an equally short passive observation because the known stimulus exposes latent dynamics that passive video leaves entangled.

Personalization can then act as a prior rather than forcing every scan to identify a person from scratch.

## System view

Let:

- \(x_t\): latent physiological / functional state;
- \(u_t\): known display stimulus;
- \(y_t\): camera observations of pupil, eye, and facial response;
- \(h_i\): longitudinal history for person \(i\);
- \(d_i\): device and environment nuisance.

A generic model is:

\[
x_{t+1}=f_\theta(x_t,u_t,h_i)+w_t
\]

\[
y_t=g_\phi(x_t,u_t,d_i)+v_t
\]

with posterior:

\[
p(x_T\mid y_{0:T},u_{0:T},h_i).
\]

The five-second experiment itself is a design variable:

\[
u^*=\arg\max_u \mathbb{E}[I(X;Y\mid U=u,H_i)]-\lambda C(u).
\]

## Why this may work

The pupil is not only a camera-visible feature. It is a dynamical system driven by known visual input and modulated by autonomic / cognitive state.

Relevant prior work establishes separate pieces:

- screen-evoked pupil light reflex can be measured reliably and has reported associations with need for recovery;
- pupil responses to rapid stimuli can be modeled with subject-specific system-identification methods;
- cognitive/arousal modulation depends strongly on luminance;
- smartphone cameras can measure pupil dynamics;
- passive five-second face video already carries some drowsiness information;
- active ocular probing has been used for impairment detection;
- generic information-theoretic experimental design can choose stimuli that identify model parameters efficiently.

The novelty target is therefore **not** "the phone can see the pupil" or "light changes pupil size."

It is the joint design of an **ultra-short, information-optimized smartphone probe for subject-relative state inference**.

## Computational result APST5-SIM-001

The first in-silico experiment asks whether stimulus timing matters when the following are fixed:

- total scan length: 5 s;
- segment length: 0.5 s;
- first segment: low luminance;
- exactly three high-luminance segments;
- identical low/high levels for every candidate;
- identical total high-luminance exposure.

The surrogate pupil model contains:

- baseline diameter;
- luminance-response gain;
- response latency;
- constriction time constant;
- dilation time constant;
- additive measurement noise.

A Bayesian D-optimal criterion measures information about the four dynamic parameters while treating baseline diameter as nuisance.

All \(\binom{9}{3}=84\) equal-exposure probes are evaluated on a design population. The selected probe is then evaluated on 500 fresh parameter draws never used for selection.

### Result

Best probe:

\`\`\`text
low | HIGH | HIGH | low | low | low | low | low | HIGH | low
\`\`\`

Held-out expected information gain:

- optimized: **11.987 nats**
- best contiguous high block: **11.687 nats**
- evenly spaced high blocks: **10.646 nats**

The optimized timing is not just "use more light"; total high exposure is exactly matched.

Relative to the best contiguous pulse, the log-determinant difference corresponds to an approximately **1.82x smaller posterior uncertainty volume** under the surrogate.

## Interpretation

The result suggests a concrete mechanism for temporal compression:

1. an early perturbation identifies fast constriction / gain behavior;
2. a recovery interval exposes slower redilation dynamics;
3. a later perturbation tests the partially recovered system again;
4. the timing pattern separates parameters better than one contiguous pulse with the same exposure.

This interpretation remains a model-based hypothesis until measured in humans.

## Breakthrough test

The strong APST-5 claim requires a human study comparing:

1. passive 5 s;
2. fixed active 5 s;
3. optimized active 5 s;
4. longer passive windows;
5. optimized active 5 s + longitudinal personal prior.

Primary targets should be kept separate:

- psychomotor vigilance / reaction-time performance;
- subjective state sleepiness;
- pupil/autonomic response parameters;
- experimentally manipulated cognitive load as a secondary domain.

A useful compression metric for target \(k\) is:

\[
TCR_k=
\frac{P_k(\mathrm{active5,personalized})-P_k(\mathrm{context})}
{P_k(\mathrm{long\ passive})-P_k(\mathrm{context})}.
\]

The numerator must come from held-out people and devices.

## Kill conditions

APST-5 should be narrowed or rejected if:

- active probing does not beat passive five seconds;
- optimized probing does not beat a fixed active probe under matched exposure;
- gains disappear on unseen participants;
- the probe mainly identifies person or device rather than transient state;
- personalization needs frequent fresh labels to remain useful;
- apparent multi-state performance is one latent factor relabeled several times;
- a frozen fresh-cohort replication fails.

## Safety and comfort constraints

Future human optimization must constrain:

- maximum display luminance;
- total luminous exposure;
- transition magnitude / frequency;
- photosensitivity-related exclusions;
- screen-to-eye distance;
- ambient illumination.

The in-silico optimizer is a research tool, not a human-use stimulus prescription.
