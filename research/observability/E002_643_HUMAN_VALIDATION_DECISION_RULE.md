# E002-643 | Human validation decision rule and recruitment feasibility (2026-11-04 UTC)

**Evidence tier:** prospective human-validation design, not observed human evidence. Complements E002-642; does not change E002-371 or authorize product claims.

## Predeclared endpoint and unit of inference

Primary endpoint is a *false exclusion*: a blinded, independently adjudicated reference closure occurs inside an ordinary-camera blind interval for which the frozen algorithm issued EXCLUDE. Reachable/abstained intervals are not counted as correct closure predictions. Evaluate only intervals with independently authenticated aperture/velocity/clock certificates; report the number rejected before scoring. Record all adjudication disagreements, not just consensus positives.

**Independence matters.** Multiple windows from one person cannot be treated as independent Bernoulli evidence. The primary analysis samples one predeclared eligible EXCLUDE window per participant (if available), with participant-level independence assumed and documented. A secondary all-window analysis uses participant-cluster resampling and is explicitly exploratory; no per-frame binomial confidence claims.

For n independent eligible participants and zero false exclusions, the exact one-sided 95% upper bound on the participant-level false-exclusion probability is 1 - 0.05^(1/n). This is *conditional on eligibility and sampling*, not a guarantee for all people, cameras or conditions.

| Independent eligible participants with zero false exclusions | One-sided exact 95% upper bound |
| ---: | ---: |
| 30 | 9.50% |
| 60 | 4.87% |
| 100 | 2.95% |
| 299 | 1.00% |
| 598 | 0.50% |

**Crucial feasibility constraint:** recruiting 60 people does not give n=60 unless 60 produce an eligible, frozen EXCLUDE window. Coverage must be reported with the recruitment denominator and participant strata. If exclusions are rare, the protocol may not be statistically feasible; report this as a negative product finding, not as a safety success.

## Blinded collection and challenge design

1. Enrol consenting adults under appropriate ethics/privacy review; publish exclusion criteria before capture. Split participants by identity into calibration, development and locked test groups. No test participant may contribute calibration clips.
2. Record independent high-rate reference video, target video and physical LED timing trace in one session. Archive raw acquisition metadata, hashes, actual exposure start/end times, clock-offset uncertainty, geometry calibration and annotator assignments; an asserted FPS field alone is insufficient.
3. Before looking at reference annotations, freeze participant IDs, target-window definitions, conservative aperture lower bounds, closure-threshold upper bound, continuous-time velocity certificates, nuisance strata, software commit, and EXCLUDE/ABSTAIN decisions. A signed immutable manifest must link the calibration session; a boolean YES is not proof.
4. Two independent blinded raters label full reference windows for eyelid aperture/closure with explicit uncertain/occluded states. Disagreement goes to a third adjudicator blinded to the prediction. Do not infer absence of closure from an unobserved short dwell; mark unresolvable cases INDETERMINATE and remove them from the primary evaluable denominator while separately reporting their rate.
5. Preassign lighting, glasses, gaze/head pose, blur, compression, missing-frame and clock-jitter strata. For every stratum report recruitment, eligible exclusions, adjudicable reference windows, false exclusions, abstentions and uncertified trials. Any false exclusion triggers a release blocker and an investigation, even if a confidence interval looks acceptable.
6. **Locked decision:** no calibrated exclusion feature is released on zero-failure counts alone. Require independently audited timing, geometry, continuous-time physiological bounds, threshold certificates, blinded adjudication and prespecified acceptable failure probability plus sufficient participant-level power. If these conditions are absent, preserve ABSTAIN_UNCALIBRATED / BLOCKED.

## Instrument-first fallback

If human recordings cannot be acquired, perform a *real* optical shutter/LED bench test: a programmable LED with measured on/off transitions and an independent photodiode/oscilloscope time base, imaged by the actual target camera under multiple exposures and rolling-shutter rows. Estimate conservative maximum unseen interval including clock error, dropped frames, exposure and scanline drift. Archive raw traces and scripts. This validates only the **instrument timing premise**, not eyelid velocities, anatomical closure or human predictions.

## Falsification and stop conditions

- A reference-confirmed closure during an EXCLUDE window falsifies the applicable certified model, calibration or implementation: stop exclusion claims.
- Any calibration inferred only from sampled finite differences is not a hard continuous-time bound: abstain.
- If independently calibrated bounds yield virtually no eligible exclusions, stop optimizing exclusion and report the observability limit as the product result.
- No physiological or production claims are supported by this protocol alone.

**Current counts:** 0 new human reference recordings, 0 eligible independently certified human EXCLUDE windows, 0 real photodiode/shutter traces, 0 held-out participant predictions. Hush unchanged.
