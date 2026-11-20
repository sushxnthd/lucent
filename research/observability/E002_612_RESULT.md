# E002-612 | Sampling faster can worsen a *certified* velocity envelope when anatomical measurement error dominates

Date: 2026-11-02. Parent: E002-371, E002-611. Evidence tier: preregistered exact-rational synthetic instrument-design falsification; **not human data**. [Frozen protocol](E002_612_FROZEN.md) committed first at `dca8232f160cc1d21d44522e3761a5d8b716ae12`.

## Scientific finding and proof

A finite set of high-rate eyelid position samples cannot, on its own, certify any finite continuous-time upper eyelid velocity. For any sampling interval of length d, the smooth bounded-aperture function `a(t)=a0+c*sin(2*pi*k*t/d)`, with `0<c<min(a0,A-a0)` and integer k, matches the same endpoint positions for every k while attaining derivative magnitude `2*pi*k*c/d`, which is unbounded as k increases. Thus a measured 240-fps or 1000-fps **peak** velocity cannot be substituted for E002-371's assumed hard continuous-time velocity cap.

A useful *conditional* bound becomes possible only if a **separate** acceleration ceiling `|a''(t)|<=M` is defended and instantaneous anatomical aperture samples `z_i` have independent error radii `eps_i` and true time intervals `d_i in [dlo_i,dhi_i]`:

    sup_[ti,ti+1] |a'(t)| <= (|z_i+1-z_i|+eps_i+eps_i+1)/dlo_i + M*dhi_i/2.

Proof: the mean of the derivative is the true endpoint secant. For any point in the interval, its derivative differs from that mean by at most `M*(t^2+(d-t)^2)/(2*d) <= M*d/2`; the endpoint difference is bounded by the measured difference plus both errors. Apply the lower time bound to the secant term and upper time bound to the acceleration term. For exact times and endpoints this is sharp: `a(t)=a(0)+s*t+(M/2)*t*(t-d)` attains `|s|+M*d/2` at an endpoint. With adversarial endpoint measurement errors of opposite signs, the full error term is also attainable.

**This is an elementary derivative/Lipschitz consequence, not a novel biological theorem.** A measured finite set of accelerations is not itself an independently certified hard acceleration ceiling; the instrument cannot self-authenticate `M`. Exposure-averaged camera measurements are **not instantaneous point samples**. They must not be passed into this formula without an independently justified optical reduction, or the instrument must abstain. A bound on one observed span is not transportable to a different person, session or future unseen closure.

## Preregistered synthetic results

Stationary nominal measured positions, equal independent point error +/-0.1 mm, illustrative **unverified** acceleration ceiling M=5000 mm/s^2, exact frame interval 1/f. Then the conditional envelope is `U(f)=2*epsilon*f+M/(2*f)`:

| Frame rate | Conditional upper speed, mm/s |
|---:|---:|
| 30 Hz | 89.333333 |
| 120 Hz | 44.833333 |
| 240 Hz | 58.416667 |
| 1000 Hz | 202.500000 |

For the stipulated stationary/noise model, increasing frame rate from 120 to 1000 Hz makes the worst-case bound **4.52 times less informative**, despite more samples. The analytic optimum is `f*=sqrt(M/(4*epsilon))`, approximately 111.8 Hz for this purely hypothetical case. This is a **noise/regularity tradeoff**, not a prescription for real camera frame rate or a claim about actual human motion. For nonstationary measurements, the observed secant term also changes. Exact 12-row grid uses errors {0.05,0.1,0.5} mm and rates {30,120,240,1000} Hz.

## Verification and failure controls

- 17 Python adversarial tests passed locally, including four frozen exact rate predictions, an attaining quadratic construction, interval-clock widening, noise/acceleration monotonicity, nonfinite values, missingness, 11 nuisance flags, and refusal of exposure averages.
- Independently written JavaScript BigInt rational arithmetic reproduced the four critical rate predictions and the sharpness construction locally.
- GitHub Actions workflow committed; hosted outcome must be checked separately and is not claimed as passed at report creation.
- The JSON entry point emits only `CONDITIONAL_OBSERVED_SPAN_VELOCITY_BOUND` with `human_speed_certified=false` when all caller-supplied evidence flags pass. Missing physical evidence forces `ABSTAIN_UNCALIBRATED`. **Flags and digests are not independent authentication.**
- This experiment provides **zero human recordings, zero blinded rater pairs, zero independently measured physical shutter timings, zero independently defended acceleration ceilings, zero held-out physical predictions**.

Reproduce from repository root:

    python -m unittest discover -s research/observability -p 'test_e002_612_velocity_envelope.py' -v
    node research/observability/e002_612_independent.cjs
    python research/observability/e002_612_velocity_envelope.py --grid

See [physical/human validation protocol](E002_612_HUMAN_PROTOCOL.md). Existing E002-611 published human mean and peak velocities remain descriptive, not hard ceilings. E002-612 closes one **instrument-identifiability gap** but does not empirically validate E002-371.

## Product consequence and next run

A future product cannot increase frame rate and assume that this alone improves a deterministic no-hidden-closure certificate; noise bounds, independently justified regularity, shutter integration and timing all matter. Until human anatomy, velocity/acceleration premises and optical shutter/clock are physically validated, **product ABSTAIN_UNCALIBRATED; release BLOCKED**. Stop further synthetic refinement of this kernel. Next substantive primary work must collect independent physical or human anatomical evidence or document an honest inability to obtain it. Hush branch/PR #45 untouched.
