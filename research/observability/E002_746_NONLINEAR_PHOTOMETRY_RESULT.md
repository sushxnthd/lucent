# E002-746 | Nonlinear photometric response falsifies brightness-as-aperture exclusion

**Evidence tier T1 (synthetic only).** Seed 746; 20,000 independently sampled feasible endpoint/velocity/time configurations. Executed locally with Python 3 before persistence. Reproduce: `python research/observability/e002_746_nonlinear_photometry.py`.

## Frozen generator and outcome

Physical aperture endpoints a0,a1 in [0.05,1], V in [5,20] normalized aperture/s, gap 0.005–0.11 s (extended when necessary to satisfy endpoint Lipschitz feasibility). A hidden zero-aperture trajectory is possible exactly when a0+a1 <= V*gap. Camera intensity is nonlinear B=a^gamma with independently unknown gamma sampled in [0.55,2.2]. The *naive* classifier wrongly substitutes B for a. The *bounded-response* comparator uses the smallest physically possible aperture over gamma in the stipulated range as each endpoint lower bound. No claim that this gamma interval is valid for real cameras.

## Executed output

```json
{"conservative_exclusions":8191,"false_conservative":0,"false_naive":353,"hidden_closures":5645,"naive_exclusions":12386,"total":20000}
```

Thus 353/12,386 naive exclusions were false (2.85% in this generator). The conservative comparator had zero false exclusions in 8,191 exclusions, **by construction under the assumed response-family and hard V bound**, not empirical validation. The naive and conservative rules are not calibrated real-world estimators. A hidden closure here means *a mathematically feasible continuous trajectory*, not an observed blink. The generator does not model sensor noise, optical scattering, rolling shutter, color processing, or exposure integration; adding them can only require additional calibrated uncertainty or abstention.

## Product and next physical falsifier

Never feed normalized RGB intensity directly into E002-371 as eyelid aperture. Independently calibrate aperture-to-intensity mapping per device, illumination, gaze and exposure mode, with interval inversion and a held-out optical shutter/photodiode ground truth. If the response family or timing cannot be bounded, ABSTAIN_UNCALIBRATED. This result does not lift production BLOCKED. Prioritize executing E002-744 physical acquisition rather than more analytic variants.
