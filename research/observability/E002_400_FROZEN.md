# E002-400 — frozen optical-integration noncommutation falsification

Frozen before executing the E002-400 instrument or inspecting numerical outputs (2026-10-23). This experiment is a **synthetic optical measurement falsification**, not a human-camera measurement.

## Question
E002-399's cone certificate assumes that an aperture number inferred from a camera exposure is an interval around the *physical aperture exposure mean*. Does a known monotone static aperture-to-intensity transfer f justify that substitution? Test the failure of inverse(mean(f(x))) = mean(x) under shutter integration, and require a quantitative optical-mean error before E002-398 human landmark packets can issue a physical certificate.

## Predeclared model and witness
Physical normalized aperture x(t) = 0.199 + |t - 0.1| on [-0.05,0.25] seconds. Speed upper V=1 normalized/s, closure threshold theta=0.2; true physical crossing at t=0.1. Reference centers t={0,0.2} s, uniform exposures e=0.1 s, zero clock error. Sensor response f(x)=exp(120*(x-0.299)), and a naive optical pipeline reports inverse_f(mean_shutter(f(x))) as though it were mean_shutter(x). Treat all numerical operations as ideal, so quantization, segmentation and camera noise cannot explain the failure.

## Frozen predictions
H1: Naively passing the two optical-inverse readings as exact physical aperture means to E002-399 with the speed V=1 and fully asserted Boolean calibration gates yields **CONFIRMED_NO_CROSSING**, a false certificate because min x = 0.199 < theta.
H2: Passing exact physical aperture shutter means to the same certificate yields **UNRESOLVED**, not false no-crossing.
H3: Correcting the optical readings by the quantitative noncommutation bound B=K V^2 e^2/(24m), where f' >= m > 0 and |f''| <= K over the independently bounded physical aperture domain, removes the false certificate (UNRESOLVED or other non-no-crossing state).
H4: An independent numerical quadrature oracle reproduces both optical readings and true physical means to within 1e-6.
H5: For 500 seeded random piecewise-linear trajectories with |x'|<=V=1, x in [0,1], e=0.1, and f(x)=x+0.5*x^2 (m=1,K=1), the absolute optical-inversion bias is bounded by B=1/2400. An independent analytic segment-integral oracle agrees with the numerical computation.
H6: Identity optical response produces zero noncommutation bias.
H7: The human-annotation bridge fails closed when no independently supported quantitative optical exposure-mean error bound is supplied, even if legacy Boolean gates are all asserted; a nonnegative finite bound may be propagated conservatively, but no flag can itself validate the provenance.

## Proof obligation
For T uniform over exposure, X=x(T), use Taylor's theorem and monotone inverse:
|f^{-1}(E f(X))-E X| <= (K/(2m)) Var(X) <= K V^2 e^2/(24m).
The last step follows from Var(X)=0.5 E[(X-X')^2] and |x(t)-x(s)|<=V|t-s|. This is an established Jensen/Taylor bound, not a novelty claim. A static transfer curve alone does not make shutter integration commute with nonlinear inversion.

## Controls and limitations
Keep shutter/exposure, speed and clocks exact in the primary counterexample. The optical transfer is an intentionally severe, mathematically admissible nuisance, **not a model fitted to real eyes or cameras**. Do not claim human false-certificate rates, natural prevalence or new physiological laws. Keep the existing E002-399 results and E002-371 theorem unchanged. Commit the negative result even if hypotheses fail. Product must abstain for physical claims without quantitative independently calibrated optical mapping and independent human aperture/velocity validation.
