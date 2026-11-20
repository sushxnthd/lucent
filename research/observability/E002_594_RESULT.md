# E002-594 | Finite high-speed frames do not certify continuous-time eyelid velocity

Date: 2026-11-02. Primary E002-371 kernel. **Evidence tier: exact mathematical falsification and synthetic software instrument only.** The local synthetic cases were explored before the GitHub reproduction freeze, so this is not a preregistered human experiment. [Frozen reproduction and future physical handoff](E002_594_FROZEN.md).

## New falsification and sharp conditional bridge

E002-593's robust shutter-gap classifier uses a *hard* continuous-time eyelid speed ceiling V. Replacing V with the largest difference between consecutive high-speed anatomical labels is invalid, even if the labels and frame timestamps are exact. For any sampling interval h, the smooth bounded-aperture functions

a_k(t) = 1/2 + (1/20) sin(2 pi k t/h), k=1,2,...

have identical aperture 1/2 at every sampled multiple of h, while their peak speed is (pi k)/(10h), unbounded as k grows. This is a **nonphysiological mathematical counterexample**: it proves that finite samples alone cannot supply a deterministic hard velocity ceiling. It does not assert that real human eyelids achieve such speeds.

A defensible *conditional* bridge is possible if the independently authenticated physical model supplies |a''(t)| <= A throughout each interval, a(t) is differentiable with Lipschitz derivative, the sample times are exactly h apart, and each observed anatomical aperture y_i has certified error <= epsilon. Then for all t in the covered intervals:

**|a'(t)| <= V_upper = max_i [(|y_(i+1)-y_i| + 2 epsilon)/h + A h/2].**

Equivalently, the dimensionless per-frame speed allowance is **V_upper h = max_i |Delta y_i| + 2 epsilon + A h^2/2**. Proof: a' at any point differs from its interval mean (a(t_(i+1))-a(t_i))/h by at most (A/h) integral |t-s| ds <= Ah/2. The true secant differs from the observed secant by at most 2 epsilon/h. The endpoint derivative of a quadratic with constant acceleration -A and opposite-sign endpoint errors attains the bound for an isolated interval. Multiple adjacent intervals can tighten it; the displayed formula remains conservative, not globally optimal.

## Independently reproduced exact synthetic cases

| Fixture | Input | Exact outcome |
|---|---|---|
| Flat observed endpoints | h=10 ms, A=200 aperture/s², epsilon=0 | V_upper=1 aperture/s |
| Noisy flat observed endpoints | Same h,A, epsilon=0.002 | V_upper=1.4 aperture/s |
| Attaining quadratic | a(t)=0.498+1.4t-100t² | a(0)=0.498, a(0.01)=0.502, initial speed 1.4/s |
| Nonflat exact endpoints | y0=0.4, y1=0.5, epsilon=0 | V_upper=11/s |
| Missing physical premise | Any missing provenance flag | ABSTAIN_UNCALIBRATED |

The independent Python Fraction instrument passed **7 tests** locally, including all six missing-premise abstentions, invalid input, exact sharpness and nonflat controls. Separately implemented JavaScript BigInt arithmetic reproduced 1, 7/5, 249/500, 251/500 and 11 exactly, with a high-frequency counterexample family. The two implementations do not read one another's outputs. [Python](e002_594_velocity_bridge.py) · [Independent JavaScript](e002_594_independent_replay.cjs) · [Hosted workflow](../../.github/workflows/e002_594_velocity_bridge.yml). **Hosted CI conclusion has not yet been independently verified.**

## Scientific and product consequence

The common shortcut 'maximum observed frame-to-frame speed is a physiological upper speed limit' is invalid. Even a high-speed reference video does not solve E002-371's velocity premise without a hard independent acceleration/velocity envelope and authenticated frame timing, anatomy and error. The software's provenance booleans are **not** a physical attestation mechanism: forged booleans can produce a model-conditional number. No unreviewed code should turn that number into a physical exclusion.

The hard acceleration premise is itself an unresolved empirical/biomechanical question. Fitting acceleration from the same sampled frames cannot establish a universal hard bound; a calibrated per-subject reference sequence does not automatically transfer to unseen participants, gaze, eyewear, lighting or camera conditions. This is a measurement-design result, not a new physiological law.

**Next physical experiment:** synchronized high-speed reference and ordinary camera with independent optical shutter/clock measurements, two blinded anatomical raters, independently justified dynamical bounds, calibrated geometry/error, predeclared nuisance strata and participant-disjoint unseen-condition predictions. Apply E002-371's strict gap exclusion only when every premise is independently verified; count reference-confirmed closure during any predicted exclusion as a falsification. Without hard acceleration or velocity evidence, return ABSTAIN_UNCALIBRATED. No actual high-speed human labels, independent rater pairs, shutter captures, acceleration/velocity certificates or held-out physical predictions were obtained here.

**Lucent release BLOCKED; PR #26 stays draft and unmerged.** Hush branch and PR #45 were not modified during this primary run.
