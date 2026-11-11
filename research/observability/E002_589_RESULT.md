# E002-589 | Full-duty exposure integration can hide a synthetic closure

**Freeze:** [E002_589_FROZEN.md](E002_589_FROZEN.md), commits 3b26f7b and pre-execution arithmetic correction 5bf8559. **Evidence tier:** exact synthetic observation-operator falsification, NOT human or physical camera evidence. Primary kernel E002-371. The initial freeze had a threshold-interval arithmetic typo corrected before code implementation; the unchanged rational knots determine the witness.

## Result

A fully exposed, known-timing, linear, 100%-duty-cycle ideal aperture-integrating sensor cannot necessarily distinguish an always-open trajectory from a trajectory containing complete closure. This attacks an overstrong product inference ("no shutter gaps means all closures were observed"), NOT the conditional E002-371 velocity theorem.

Let u denote one normalized frame period, with full-period measurement Y = integral_0^1 a(u) du and closed threshold tau = 1/5. World O has a(u)=1/2 always. World C has a continuous piecewise-linear trajectory through knots (0,1/2), (1/8,1/2), (1/4,0), (3/8,1/2), (5/8,1/2), (3/4,1), (7/8,1/2), (1,1/2), repeated periodically. Both worlds have known matching instantaneous frame-boundary apertures 1/2, a shared valid speed ceiling |da/du| <= 4, normalized aperture in [0,1], exact exposure clocks and no uncovered time.

**24/24 full-frame exposure averages match exactly at 1/2.** Yet World C reaches a=0 at u=1/4 and is closed (a <= 1/5) on [1/5,3/10], a duration of 1/10 frame; World O never closes. Repeating the witness yields identical 24-frame measurements and distinct underlying closure histories. These are 24 constructed periods, NOT independent human observations.

| Prospective instrument measurement | Open world | Closure world |
|---|---:|---:|
| Each full-frame average, 24 frames | 1/2 | 1/2 |
| First half-frame average | 1/2 | **3/8** |
| Second half-frame average | 1/2 | **5/8** |
| Half-frame at phase 1/4 | 1/2 | **1/2** (discriminator fails) |
| Full-frame shifted by 1/8 | 1/2 | 1/2 |
| Pre-integration square-response full-frame average | 1/4 | **7/24** |
| Post-integration gain 3/2 and offset 1/8 | 7/8 | 7/8 |

Reducing the positive-bump peak from 1 to 9/10 changes the closure world's full-frame mean from 1/2 to **39/80**, breaking equality. A known pre-integration nonlinearity also breaks this particular witness. Thus this is NOT an impossibility theorem for every camera imaging operator. It proves non-identifiability for the specified idealized full-duty linear integration operator. A short exposure discriminates the constructed pair at some phases, but not all.

## Dimensionless velocity guard and physical relevance

The constructed closure world has max |da/du| = 4, i.e. V*T=4. If independently authenticated instantaneous frame-boundary apertures equal 1/2 and a hard bound V*T < 3/5 holds, the elementary two-endpoint Lipschitz envelope implies a(t) > 1/5 everywhere, excluding closure. Equality can touch the threshold. At 30 fps, this witness has maximum speed 120 normalized-aperture units/second and a closed interval lasting 3.33 ms. **No claim is made that human eyelids achieve this speed or repeat this pattern.** Real cameras do not directly supply perfect instantaneous aperture endpoints, and a velocity bound inferred solely from sampled frames is not a certified continuous-time physiological ceiling.

## Reproducibility and verification

- [Python exact-rational simulator](e002_589_full_duty_aliasing.py): piecewise-linear and squared integration, 24 frames, half-window/phase controls, threshold, speed and perturbation checks. Executed locally: **PASS**.
- [Independent JavaScript BigInt replay](e002_589_independent_replay.cjs): separate rational integration, no Python-generated data input. Executed locally: **PASS**.
- [Hosted CI workflow](../../.github/workflows/e002_589_full_duty_aliasing.yml) committed. Do not claim hosted E002-589 success without inspecting its run.
- Previous [E002-588 hosted run #41309998788](https://github.com/sushxnthd/lucent/actions/runs/41309998788) was checked and concluded **success**, including Python and independent Node checks.

## Product consequence and next decisive experiment

**Reject** the inference that 100% shutter duty or optical coverage alone makes exposure-integrated brightness an anatomical no-hidden-closure certificate. Keep calibrated exposure integration and instantaneous anatomical aperture evidence separate. Require a validated image-formation operator, measured shutter/clock/geometry, independently justified hard velocity ceiling and held-out physical closure tests. Unknown pre-integration response, gaze, glasses, geometry, illumination, blur, rolling shutter and missingness remain separate abstention triggers; their absence in this idealized construction is intentional.

The immediate physical validation path is E002-585's consented synchronized high-speed/ordinary-camera capture with photodiode timing and two blinded anatomical raters. Preregister a subset comparing full-exposure and short-exposure/phase-shifted captures against held-out high-speed closure truth. Record actual sensor response, rolling-row support, clock drift and nuisance flags, and evaluate E002-371 predictions participant-disjoint. This run collected **zero** new human rater pairs, **zero** physical shutter captures and **zero** certified physiological speed bounds. Further synthetic refinements do not substitute for acquisition.

**Lucent:** ABSTAIN_UNCALIBRATED, release BLOCKED. Hush not modified.
