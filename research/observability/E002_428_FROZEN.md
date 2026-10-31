# E002-428 — frozen participant-level velocity-tail calibration and power gate

Date: 2026-10-25. Primary kernel: E002-371 physical shutter-gap/velocity observability. Evidence tier at freeze: **published independent human observations + planned synthetic statistical verification; no newly accessed individual human data**. Existing branch and draft PR #26 only.

## New empirical constraint, not an individual-level dataset
Navascues-Cornago, Maldonado-Codina, Morgan & Read, *The Ocular Surface* 40 (2026), 22–30, DOI 10.1016/j.jtos.2026.01.003, filmed spontaneous blinks in 20 people and reflex blinks in 10 additional people at **500 fps**, then compared 250/100/50/25-fps decimations. The peer-reviewed abstract reports that maximum closing/opening velocities were markedly underestimated below 250 fps, particularly for reflex blinks; 250 fps is recommended for comprehensive blink-dynamics assessment. This is a direct independent warning that **ordinary-camera secant maxima are not defensible velocity ceilings**. No individual trajectories or raw videos have been obtained; aggregate conclusions must not be relabeled Lucent validation. Source: https://pubmed.ncbi.nlm.nih.gov/41565104/

Kwon et al. (2013), DOI 10.1098/rsif.2013.0227, 25 volunteers at 600 fps, manually assessed aperture at 5-ms increments; reported 243 +/- 9 mm/s mean peak closing speed and compared a previous 427 +/- 30 mm/s group mean. Neither average, observed maximum, nor uncertainty around a mean is a hard physiological bound. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/

## Preregistered new calculation and failure controls
For a velocity ceiling **V frozen using training participants only**, define one Bernoulli violation per *independent held-out participant*: any independently measured valid closing/opening peak speed exceeding V across the frozen behavior/task/nuisance coverage. Use all relevant held-out trials per participant; never count frames or correlated blinks as independent Bernoulli draws. Under an explicit IID participant-sampling assumption within each predeclared stratum, use a one-sided exact binomial upper confidence bound p_U satisfying P_{p_U}(X<=k)=alpha for k<n, where k of n participants violate V and alpha=0.05. If k=0, p_U=1-alpha^(1/n). If k=n, p_U=1. The confidence statement is about **population probability of violating V under sampling assumptions**, not an almost-sure physiological speed limit and not a camera false-certificate rate.

Frozen sanity gates at 95% confidence:
- k=0,n=8: p_U ~31.234%; k=0,n=25: ~11.293%; k=0,n=100: ~2.951%; k=0,n=299: ~0.997%.
- At least 299 independent zero-violation held-out participants are required to obtain p_U <1% at 95% confidence under this model; no finite n converts a probabilistic bound into a deterministic bound.
- If V was chosen after examining held-out peaks, or participant independence/behavior coverage is unsupported, **reject statistical certification** rather than reporting a misleading confidence limit.
- If a peak is unmeasurable owing to clock, geometry, blur, gaze, glasses, missingness, shutter or rater disagreement, record **unresolved participant**. Never treat unresolved as nonviolations; compute conservative sensitivity by treating unresolved as violations, and block a narrow bound if the interval spans the target risk.
- Report participant-level counts and all predeclared nuisance/device/task strata. Do not claim simultaneous 95% coverage across many strata without multiplicity adjustment.
- Independently verify the exact binomial inversion against a separately implemented oracle and test k=0, k=n, monotonicity, unresolved extremes, invalid inputs and frozen-ceiling provenance.

## Decisive product consequences
The **sharp deterministic E002-371/E002-421/422 law remains conditional on a genuine hard V**, calibrated shutter and aperture. A 95% participant-level tail bound **cannot** be inserted as V to generate an unconditional no-hidden-closure certificate. If a future product reports probabilistic, population-calibrated risk, it requires prospective independent human validation of the *complete camera prediction pipeline* and must distinguish population-tail uncertainty from individual-interval conditional uncertainty. Current physical output stays `ABSTAIN_UNCALIBRATED` for hidden closure, blink duration, PERCLOS and fatigue.

## Human study and access gate
Do not continue dataset archaeology. Seek authorized 400-fps FaceBase traces or separately consented >=500-fps physical eyelid recordings, independently registered anatomical aperture, two blinded annotators, externally calibrated shutter/clock, and separate spontaneous/reflex and nuisance/device strata. Freeze V on training people; score unseen people and cameras prospectively with E002-426 sealed predictions and E002-427 adapter. The 2026 paper's authors may be asked for a compliant data-access or independent replication pathway; no contact is assumed. If individual data remain unavailable, deliver only the synthetic exact-binomial verification and a concrete recruitment/sample-size specification.

No claim of novel binomial statistics or novel human physiology. This artifact is an empirically motivated study-power and claim-calibration gate, not physical E002-371 validation.
