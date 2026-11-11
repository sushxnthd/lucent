# E002-538 RESULT | A sharp acceleration-only shutter-gap law, and why sampled velocities cannot certify it

Date: 2026-10-30. Primary E002-371 kernel; existing `research/observability-human-boundary` branch and draft PR #26. **Evidence tier: exact deterministic model analysis and executable synthetic falsification. No new human eyelid ratings, camera captures, photodiode timing, or independently certified physiological acceleration envelope.** Frozen protocol: [E002_538_FROZEN.md](E002_538_FROZEN.md).

## Scientific finding and proof

Let `a:[0,D] -> [0,1]` be a twice-differentiable **pointwise normalized anatomical aperture**, with `a(0)=b0>c`, `a(D)=b1>c` and a *hard* continuous-time acceleration envelope `|a''(t)|<=A`. No first-derivative/velocity bound is assumed. Define the chord `ell(t)=b0+(b1-b0)t/D`.

**Sharp interpolation bound:** For every `t` in `[0,D]`,

`a(t) >= L(t) := ell(t) - (A/2)t(D-t)`.

Proof: `a''<=A` implies `(a-L)''<=0`; the function `a-L` is concave with zero endpoints, so `a-L>=0` throughout. The quadratic `a=L` attains equality and has `a''=A`. For `A>0`, the minimizer is `t*=clamp(D/2-(b1-b0)/(A D),0,D)`; for `A=0` it is the lower endpoint. Thus `min L>c` excludes **every** hidden threshold crossing, while `min L<=c` admits a crossing/touching trajectory satisfying the same acceleration limit and physical range: continuously reduce the quadratic curvature from A to the first value at which its minimum equals c. All intermediate parabolas remain between their endpoint maximum and the positive threshold. **Equality is not an exclusion.**

The critical acceleration is `Acrit=2*(sqrt(b0-c)+sqrt(b1-c))^2/D^2`. This follows by minimizing the curvature needed to touch c over interior t. For equal endpoints b0=b1=b, `Acrit=8*(b-c)/D^2` and the dimensionless boundary is

`Q = A D^2 / [8(b-c)]`.

`Q<1` excludes crossing *only under the stated physical assumptions*; `Q>=1` does not. Doubling D multiplies Q by four. This is a classical bounded-curvature interpolation principle applied to Lucent's observability question, **not a claim of priority over interpolation theory**. Its scientific value here is an independently falsifiable acquisition/physiology requirement and an exact abstention boundary.

## Frozen executed results

All A values below are **hypothetical normalized aperture accelerations**, not measured human limits. D is a hypothetical fully unobserved pointwise aperture gap, **not** a verified smartphone shutter gap.

| Hypothetical endpoints, gap and acceleration | Exact Q | Exact minimum of sharp lower envelope | Conditional geometry |
|---|---:|---:|---|
| b0=b1=0.9; c=0.2; D=1/30 s; A=3000 s^-2 | 25/42 | 29/60 | No hidden crossing |
| Same, A=5040 s^-2 | 1 | 1/5 | Touching is feasible; abstain |
| Same, A=6000 s^-2 | 25/21 | 1/15 | Crossing feasible |
| Same, D=1/240 s; A=6000 s^-2 | 25/1344 | 1703/1920 | No hidden crossing |
| b0=0.8, b1=0.9; c=0.2; D=1/30 s; A=6000 s^-2 | asymmetric; Q inapplicable | 191/12000 at t=97/6000 s | Crossing feasible |

The asymmetric critical A is approximately **4673.07 s^-2**, not the equal-endpoint formula. A concrete physical-range witness for the asymmetric A=6000 example is the sharp quadratic L itself: all values remain within [0,1], its minimum is 191/12000 (<0.2), and its second derivative is exactly +6000 s^-2. The equal-endpoint A=6000 witness likewise stays in [0,1]. An independently written Node BigInt checker verified all four exact equal-endpoint Q values and decisions.

**Sampled-velocity alias:** The smooth synthetic path `a(t)=b-(b-c)sin^2(pi*t/D)` has aperture b and velocity zero at both sampled endpoints but reaches c halfway between them. Its peak absolute acceleration is `2(b-c)pi^2/D^2` (approximately **12435.70 s^-2** for b=0.9, c=0.2, D=1/30 s). Thus even **exact sampled endpoint velocities** do not supply a continuous-time hard speed/acceleration ceiling. This is a counterexample, not a physiological blink.

## Nuisance attacks, verification and limits

Seventeen Python adversarial tests passed locally, including exact threshold equality, asymmetric geometry, bounded-curvature witnesses, invalid anatomy, source-provenance refusal, sampled-velocity aliasing, clock-gap inflation, a missing-frame gap, exposure-average/raw-pixel misuse, and explicit production abstention. The independent Node BigInt replay passed all four frozen symmetric cases. A dedicated hosted CI workflow was committed; **hosted verification was not confirmed at initial report creation**. No real-camera, blur, gaze, glasses or lighting robustness was established by these mathematical tests. The E002-533 real-codec photometry failure and E002-534/535 rejected image-return proxy remain separate negative evidence; they cannot be promoted into anatomical ground truth.

**Crucial identifiability limitation:** a finite high-speed sequence cannot certify a hard bound on continuous-time acceleration without an additional independently defensible smoothness/physical model. Sampled second differences are not a substitute. Exposure-integrated pixel brightness is not pointwise anatomical aperture, and nominal FPS is not an authenticated maximum unseen interval. If any of those are absent, the only defensible output is abstention.

The executable refuses non-pointwise endpoints, sampled or cohort acceleration, absent physical attestations, missingness/clock uncertainty and unverified nuisance envelopes. Even a hypothetical fully attested input yields only `CONDITIONAL_BOUND_ONLY`, never a physical/product certificate. **Lucent stays `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.**

## Concrete human/instrument study handoff

Use the existing E002-483 12/12 design only as a feasibility pilot, not a 95% participant-level statistical certificate (E002-537). Independently capture a photodiode/LED timing channel and high-frame-rate native anatomical video while ordinary-camera captures run simultaneously. Pre-register a per-frame upper bound on unobserved **pointwise** gap including exposure integration, rolling-shutter rows, clock drift and missing frames; do not infer pointwise endpoints from average brightness. Obtain two blinded anatomical raters for upper/lower lid landmarks, reference uncertainty, and disagreements. Prespecify independent participant/session-specific acceleration modeling and explain what physical assumption could justify a *continuous-time* hard envelope. If no such envelope is credible, restrict analysis to probabilistic participant-level risk with abstention, not deterministic exclusion.

Before viewing held-out participants, freeze the predicted threshold-crossing status using both E002-371's speed law (only if independently defensible) and this acceleration law, then compare to native-frame reference labels under held-out gaze, glasses, brightness, blur, sampling and clock-error strata. Record unknown labels as unknown. Report failures, per-participant uncertainty and coverage, not only overall accuracy. The fastest useful next evidence is **actual physical timing plus blinded anatomy**, not another synthetic threshold adjustment.

**Evidence inventory:** new blinded anatomical ratings 0; authenticated physical shutter studies 0; certified continuous-time human acceleration ceilings 0; participant-disjoint physical predictions 0. Hush PR #45 not modified.
