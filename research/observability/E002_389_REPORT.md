# E002-389 — Joint exposure-integral observability certificate (2026-10-23)

**Evidence tier:** deterministic synthetic instrument and linear-programming proof certificate, conditional on physical aperture, exposure timing, error and speed assumptions. **No new human data, physical camera experiment, or publication-level novelty.** Protocol frozen before evaluation at commit `f99879796d70add9ca0e4c8da66d250c8a9a6c0f`.

## Question
Can a series of **actual exposure means**, treated jointly, certify no hidden eyelid-aperture threshold crossing when independent exposure-by-exposure Lipschitz envelopes cannot?

Let a:[0,T] -> [0,1] be V-Lipschitz. Each calibrated exposure measures y_i with |y_i - (1/|I_i|) integral_{I_i} a(t)dt| <= epsilon_i. The correct observability question is the infimum of a(t) over all trajectories satisfying **all** measurements, not an aperture proxy assigned to frame centers.

## Conservative continuum-to-LP reduction
On grid spacing h, linearly interpolate the unknown true node values to b(t). For any V-Lipschitz a, |a(t)-b(t)| <= Vh/2. Thus the true exposure constraints imply |mean_I b-y_i| <= epsilon_i + Vh/2. The exact piecewise-linear exposure means are linear in the node values. For each target grid node, minimize b_j by LP subject to 0<=b_j<=1 and |b_{j+1}-b_j|<=Vh. The **minimum of all node-wise LP optima minus Vh/2** is a sound lower bound for a(t) anywhere in the target interval, provided the target endpoints lie on the grid. The LP is sharp *within the relaxed discretized model*, not necessarily sharp for continuous signals. The extra Vh/2 allowances make the continuum result conservative.

This proof uses only deterministic Lipschitz interpolation; it does not make a statistical coverage claim.

## Frozen instrument and observed results
V=60/s; threshold=0.2; h=1 ms; target t in [20,80] ms. Exposure windows [10,30], [40,60], [70,90] ms. High observations y=0.96 with error <=0.005. Lower-middle observation y=0.50. Four preregistered configurations:

| Condition | Independent pointwise lower | Joint continuum-safe lower | Decision |
|---|---:|---:|---|
| Outer exposures only | -0.845 | -0.030 | ABSTAIN |
| All three high | 0.055 | **0.246** | **CERTIFY no threshold crossing** |
| Middle lowered to 0.50 | -0.165 | -0.030 | ABSTAIN |
| All high, error inflated to 0.20 | -0.140 | -0.030 | ABSTAIN |

All five frozen predictions passed. **The strict gain is 0.246 > 0.2 despite a standalone Lipschitz exposure envelope of 0.055 < 0.2.** Negative lower bounds are unclipped mathematical relaxation outputs; physical aperture remains nonnegative.

A constructive outer-only counterexample is a(t)=0.96-max(0,0.77-60|t-0.05|). It reaches aperture 0.19 at 50 ms, is 60/s-Lipschitz and has exactly 0.96 mean in both outer exposures. It is a strict threshold crossing, not merely a touch. The third exposure rules out such a crossing in the calibrated model.

## Independent verification
An independently coded LP matrix generator reproduced the node-wise optimum at each worst-case target node. Dual and primal objectives matched within 1e-7, with stationarity and inequality residuals <1e-7. Independent trapezoidal integration checked every reported witness exposure mean. An explicit crossing witness satisfied the *original*, not inflated, outer exposure constraints. The local check performed 18 assertions/check groups, including four primal-dual comparisons.

## Product consequence
If and only if an independent physical aperture response, worst-case optical-error envelope, per-exposure clock/timing, independently valid speed bound and all relevant nuisance assumptions are qualified, Lucent may issue a **conditional no-threshold-crossing certificate** over a specified interval using the joint integral LP. If any assumption is missing or the conservative lower bound <=threshold, return ABSTAIN. Never substitute RGB intensity or H.264 pixel means for physical aperture exposure means without independent transfer validation. This is a **newly tested synthesis of established convex feasibility methods**, not a claimed new theorem or clinical device.

## Focused primary-literature priority check (not exhaustive)
- Juditsky and Nemirovski (2018), *Near-optimality of linear recovery from indirect observations*, Mathematical Statistics and Learning, DOI 10.4171/MSL/1-2-2, studies convex-constrained recovery from indirect linear observations. The general optimization framework is prior art; no claim of inventing convex recovery or a new universal information law is warranted.
- Kwon et al. (2013), *High-speed camera characterization of voluntary eye blinking kinematics*, J. R. Soc. Interface, https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/ , reports high-speed blink kinematics, but not the synchronized ordinary-camera/optical-calibration validation needed here.
- Godfrey et al. (2019), *Analysis of Spontaneous Eyelid Blink Dynamics Using a 240 Frames per Second Smartphone Camera*, Ophthalmic Plast Reconstr Surg, DOI 10.1097/IOP.0000000000001356, reports 240-fps human acquisition. Published summary statistics do not constitute an accessible held-out raw video cohort.

The possible contribution is **application-specific calibrated decision logic and a falsifiable observability boundary**, not a new general LP technique. A thorough novelty review remains open.

## Critical limitations
These observations are synthetic. V=60/s is hypothetical and not a population-validated human bound. Real shutter functions need not be rectangular. RGB rendering can be non-injective under gaze, glare, glasses, blur, geometry, gain, missingness and rolling shutter. The model assumes valid independent deterministic error bounds. The 1-ms discretization incurs a 0.03 aperture penalty, and solver floating-point tolerances require engineering margins. Human synchronized RGB/high-speed validation and priority review remain open. See the earlier 60-participant protocol and E002-388 for codec falsification. This run did not use Hush resources.
