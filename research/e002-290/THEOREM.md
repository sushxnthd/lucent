# Measurement equation, exact reduced-model boundary, and ten-field kernel

**1 Signal/reference.** RGB apparent pupil/iris ratio plus iris-scale, eyelid-aperture, eye/reference luminance and gaze marker; target independently synchronized high-rate pupil diameter and anatomical eyelid aperture. No paired human measurement used in this run.

**2 Frontier.** Scharf & Friedlander (1994) established matched-subspace detectors; Wang, Chern & Alexa (2019) established the pupil/iris projective invariant. Novelty of the generic mathematics is rejected.

**3 Metric.** `d_inf=min_theta ||s-N theta||_inf` and signed separation margin `|a|*d_inf-2eta`; optimal linear nuisance-annihilating witness `w` satisfies `N^T w=0`, `||w||_1<=1`.

**4 Strongest nuisance.** Pupil-specific optical magnification caused by corneal refraction/gaze/glasses. It can be collinear with the physiological pupil feature. Secondary: aperture, scale, pose, brightness, rolling shutter, clock error and missingness.

**5 Generative model.** Pixel level: `Y_k(x)=Q_k[b_k(x)+(g_k(x)/T_k) integral_{E_k}(h_k * {L_t A_t S(H_t,r_iris,k_t*r_pupil(t),gaze_t,glasses_t)})(x) dt]+epsilon_k(x)`. Local feature-level approximation around an independently calibrated baseline: `z=z0+a*s+N*theta+e`, `||e||_inf<=eta`. The theorem is exact for the reduced affine model, NOT the nonlinear pixel model.

**6 Falsification.** A nuisance-only holdout produces a positive certificate, a reference-confirmed event above the predeclared boundary is missed, or calibrated residuals exceed eta. Exact counterexample without gaze: `s=(5/3)*(n_aperture-n_gaze)`; unbounded optical column `s` yields another collision.

**7 Boundary.** For H0 `S0={N theta+e:||e||_inf<=eta}` and H1 `S1={a*s+N theta+e:||e||_inf<=eta}`, intersection iff `|a|*d_inf<=2eta`. This follows from differences of infinity-norm balls and linear programming duality. With a separate optical nuisance `u_i in [-b,b]` in each hypothesis, intersection iff `max(0,|a|-2b)*d_inf<=2eta`. Equality is ambiguous. For unbounded optical nuisance, intersection exists for every amplitude.

**8 Untouched human.** None. Frozen future test in HUMAN_FROZEN_GATE.md.

**9 Publication threshold.** Prospective RGB/reference participant/device/lighting/gaze/glasses holdout, independent nuisance and noise calibration, unseen predicted boundary crossing, stronger baselines, external replication and prior-art differentiation. Not met.

**10 Product.** Reject uncalibrated rapid pupil-waveform and five-second fatigue claims. Investigate calibrated pupil/iris certificate only with independently validated positive margin; otherwise abstain. Blink geometry is an alternative requiring a separate human gate.

**Important:** Feature channels are normalized dimensionlessly by an illustrative convention. Reweighting channels changes d_inf and the numerical boundary. No physiological magnitude or probability of error can be inferred from the synthetic thresholds. Unrestricted optical collinearity is a feature-level impossibility, not a theorem about all RGB pixels.