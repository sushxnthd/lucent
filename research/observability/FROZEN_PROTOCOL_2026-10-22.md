# Frozen E002-372 human-to-instrument validation protocol (2026-10-22)

## Active question
Can an independently bounded normalized eyelid-aperture speed certify whether a threshold closure is possible in an unobserved ordinary-RGB shutter gap?

**Signal/reference:** exposure-integrated RGB eye-aperture evidence (30/60 Hz emulation from high-speed frames) versus native high-frame-rate human eyelid-aperture trace. Emulation is *not* paired native-camera validation.

**Frontier:** sampling/shutter observability, eyelid blink kinematics and PERCLOS. Previous E002-371 conditional Lipschitz bound is a model theorem, not human evidence. Do not claim novelty of Lipschitz envelopes.

## Generative model
For normalized aperture a(t) in [0,1], |da/dt|<=V, and closure threshold theta, native camera measurement is
Y_{i,p}=Q{ (1/w_i) integral_{t_i}^{t_i+w_i} [g_i R_p(a(t),gaze(t),glasses,blur)+b_i]dt + eta_{i,p} }.
Timestamp uncertainty is bounded by u_i. Missing/occluded frames carry no aperture constraint. The geometry-normalized proxy is upper-lid/lower-lid separation divided by independently measured iris or canthal scale; pupil size is not used.

For a completely unobserved interval of length H with exact aperture endpoints a0,a1 and feasible |a1-a0|<=VH, a hidden a(t)<=theta is possible iff
H >= ((a0-theta)_+ +(a1-theta)_+)/V,
subject to endpoints and equality semantics. The maximal duration strictly below theta is bounded by
max(0,H-((a0-theta)_+ +(a1-theta)_+)/V).
At the boundary, a zero-duration touch is possible, not a positive-duration closure. For uncertain endpoints a0 in [l0,h0], a1 in [l1,h1], use the least costly feasible endpoints, not point estimates.

## Predeclared synthetic/human protocol
1. Search at most two distinct public high-speed human blink paths; require acquisition frame rate, raw frame timestamps or calibrated constant cadence, visible lids, usage permission, independent participants.
2. Before scoring held-out people, split by participant (if available), freeze theta=0.2 and derive conservative V from training people using high-fps aperture and frame-spacing/error intervals. Do NOT use held-out speeds to set V. Report exceedance rate of the assumed bound on holdout.
3. For each native sequence, pre-register 30 Hz, 10 ms exposure and 60 Hz, 5 ms exposure virtual-camera schedules, multiple shutter phases, and independent reference annotations of blink intervals. Synthesize only after locking thresholds.
4. Evaluate *one-sided certification*: whenever the endpoint-speed law rules out a hidden closure, measure false-exclusion rate against native reference. Report coverage/abstention, Wilson intervals, per-participant failures. A law with a violated speed bound is not a valid certificate.
5. Adversarial controls: geometry-only, brightness-only, missingness-only, blur, gaze, glasses, timing +/-1 frame and temporally smoothed constant-aperture baselines. No black-box primary estimator.
6. Freeze unseen prediction from train participants: bins immediately below/above Hcrit=((a0-theta)_++(a1-theta)_+)/V; below predicts zero missed closures **only when V is independently certified**, above predicts *possible* missed closure, not that one must occur.
7. Primary failure: any human hidden closure in a certified-impossible gap with verified reference and satisfied speed assumption. Otherwise evaluate empirical utility via certification rate and uncertainty.
8. Product: allow only bounded closure evidence and abstention; reject exact PERCLOS, rapid pupil waveform and five-second fatigue inference absent further validation.

## Publication gate
Exact theorem + independent checker + native-human reference evaluation + unseen participant/device boundary prediction + confound stress + priority audit + documented failures. High-speed-video-to-virtual-camera tests are an instrument validation substitute, not proof of real RGB performance.

## Evidence ledger
Status: protocol frozen; no held-out human outcomes inspected. E002-371 conditional theorem reported; speed bounds not yet empirically established.
