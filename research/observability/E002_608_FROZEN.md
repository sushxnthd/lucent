# E002-608 | Frozen exposure-averaged endpoint transfer and release gate

Date: 2026-11-02. Parent E002-371; research branch `research/observability-human-boundary`; draft PR #26. This is a **conditional optical measurement model** and falsification of an unsafe product interpretation, **not** human validation or a claim of priority.

## Predeclared question and exact model

Does applying the point-sample E002-371 bound to **exposure-averaged** anatomical apertures falsely exclude hidden closure? Can a conservative, independently calibrated exposure-aware gate avoid that error?

Assume a continuous normalized anatomical aperture `a(t)` in [0,1], with global Lipschitz speed `|a(t)-a(s)| <= V |t-s|`, and threshold `tau`. Two disjoint, non-overlapping, uniform boxcar exposures `[sL,bL]` and `[sR,bR]` satisfy `bL <= sR`. Let `g=sR-bL`, `eL=bL-sL`, `eR=bR-sR`, and exposure averages `mL,mR`. No optical-to-anatomical conversion is presumed.

For any hidden closure `a(t*) <= tau` with `t* in [bL,sR]`, the Lipschitz envelope implies
`mL <= tau + V (t* - (sL+bL)/2)` and
`mR <= tau + V ((sR+bR)/2 - t*)`.
Therefore **hidden closure requires** `mL+mR-2*tau <= V*(g+(eL+eR)/2)`.
The strict reverse inequality is a **sufficient exclusion certificate**, not a general equivalence. This is a shutter-aware *model-level* inequality. For measured intervals use lower confidence/uncertainty endpoints `mL_lo,mR_lo` and upper physical budgets `V_hi,g_hi,eL_hi,eR_hi`. Dimensionless margin `R=(mL_lo+mR_lo-2*tau)/(V_hi*(g_hi+(eL_hi+eR_hi)/2))` is reportable only for positive denominator. Equality must **ABSTAIN**, not certify. Do not infer a velocity ceiling from sampled finite differences.

## Frozen adversarial witnesses

1. Let `tau=.2`, `V=.02 /ms`, exposures `[-20,0]` and `[10,30]` ms, hidden closure `t*=5 ms`, and `a(t)=.2+.02*|t-5|` over these windows and the gap. This remains within [0,1] on [-20,30]. Exact averages `mL=mR=.5`. The **naive point-endpoint** test compares `.6 > .2` and incorrectly excludes. The **shutter-aware** test compares `.6 > .6` (false) and must abstain. Independently calculate both boxcar integrals in a separate Node.js implementation.
2. Constant-open control `a(t)=.6` yields `mL=mR=.6`, shutter-aware margin `.8 > .6` and conditional exclusion.
3. Missing independent shutter/clock, eyelid-to-average radiometry, anatomical geometry, continuous-time velocity provenance, or any nuisance flag must ABSTAIN, never exclude.
4. Increasing any uncertainty budget (larger V/g/exposure, lower measured aperture) cannot turn ABSTAIN into EXCLUDE. Exact equality cannot EXCLUDE.
5. Any overlapping/negative-duration exposure, nonfinite input, out-of-range aperture, unsupported observation operator, or missing evidence digest must be rejected or abstained. No caller-declared `verified=true` alone authenticates evidence.

## Implementable instrument and physical boundary

Build a pure-Python JSON-lines conditional classifier with explicit calibration fields and nuisance flags, plus independent Node.js witness replay and Python regression tests. Accept *only* precomputed conservative interval bounds from an external calibration custodian, not images or video. Require named, nonempty SHA-256 digests for independent clock/shutter, linear-aperture response, geometry, and velocity evidence; these digests are **references**, not proof of authenticity. Return `MODEL_EXCLUDE_CONDITIONAL` only with all model prerequisites and no nuisance flags; never `human-validated` or `production-safe`. Record a dimensionless ratio and strict margin when defined.

The release gate remains `ABSTAIN_UNCALIBRATED` and `BLOCKED` even if a conditional synthetic fixture passes. Physical promotion requires independent measured shutter windows, measured sensor/geometry transfer, externally defensible velocity ceiling, blinded high-rate human closure annotations, preregistered participant-disjoint predictions, and external review. Preserve negative results and no private human images in GitHub.

Freeze this protocol before implementing or running the witness code.