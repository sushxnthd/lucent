# E002-498 | Frozen participant-level speed-envelope evidence gate

Date: 2026-10-28. Primary E002-371 human-validation kernel. Freeze before implementing the gate or observing any new human eyelid-velocity data. **This is a human-study design and product-claim falsification gate, not physical validation or a novelty claim.**

## Why the existing human evidence cannot close E002-371

E002-496 produced a technically valid blinded S01 image packet; E002-497's offline viewer passed hosted software tests. There are **zero** independent anatomical ratings, **zero** independently calibrated camera clocks/shutters, and **zero** independently certified participant-level *upper* bounds on true peak eyelid velocity. E002-493 falsified the motion-event selector under jitter and stride-2 sampling. The observed speed of an eyelid between two frames is a **lower** bound on a possible intervening peak speed, not an upper bound. An instrument with an unbounded inter-frame acceleration cannot turn a finite sequence of sampled positions into a hard continuous-time speed ceiling.

The published 600-fps voluntary-blink study (https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/) reports group peak closing speed 243 ± 9 mm/s. This is an empirical reported statistic, **not** a universal upper limit and not an independent bound on a new user's eyelid speed. GazeBase (https://doi.org/10.1038/s41597-021-00959-y) offers 1,000-Hz pupil/gaze traces and parser blink labels, but its missing samples can arise from failure to detect the pupil or corneal reflection; it does not provide certified continuous-time upper eyelid velocity. Neither source alone licenses the physical E002-371 product claim.

## New statistical distinction and exact preregistered criterion

Let `U_i` be an **independently certified continuous-time upper bound** on the maximum normalized eyelid speed of participant `i` over the prespecified protocol. This requires an authenticated physical timebase, calibrated geometry, exposure/shutter bounds, landmark uncertainty, and a justified between-sample speed envelope (for example, an independently established acceleration bound). Merely taking the maximum finite difference is NOT `U_i`.

If `U_1,...,U_n` are exchangeable, independently sampled **participants** from a clearly defined target population, the maximum `M=max(U_i)` is a one-sided, distribution-free population tolerance bound: for target population coverage `p`, the probability that `M` covers at least a fraction `p` of the population is at least `1-p^n`. The proof is the order-statistic identity for a continuous distribution, with a conservative inequality for ties. It is **not** a hard bound for all humans and says nothing about untested populations, settings, or devices.

Freeze two evidence tiers, neither sufficient alone for release:
- Pilot statistical envelope: target population coverage `p=0.95` at confidence `0.95`, requiring at least **59 independent participants**, *not* 59 blinks or 59 frames.
- Stronger statistical envelope: `p=0.99` at confidence `0.95`, requiring at least **299 independent participants**.
- These numbers apply only after all `U_i` are independently certified and exchangeability/participant independence are defensible. If a subgroup, device, gaze condition, glasses condition or exposure regime breaks exchangeability, calibrate that stratum separately or abstain.
- No finite `n` supports a deterministic population-wide speed ceiling without a separate physical assumption.

## Decisive human experiment (frozen before recruitment or annotations)

1. **S01 pilot only.** Obtain two truly independent, blinded raters using E002-492/497 on the already frozen 20×13 S01 native frames. Report dual-measurable fraction, disagreements and abstentions; never convert AVI frame numbers to seconds. The packet alone cannot estimate population speed or certify a hidden-closure boundary.
2. **Physical acquisition.** Record voluntary and natural blinks using a high-frame-rate device with an **independently observed optical time reference** in the same field of view. Validate the optical reference against a second time standard and measure clock drift/jitter, rolling shutter and exposure window. Camera nominal fps and container PTS are not acceptable substitutes. Obtain consent, minimize collection of identifiable imagery, and store raw frames locally. No forced sleep deprivation or medical claims.
3. **Reference geometry.** Calibrate an in-plane length reference and iris/eyelid geometry for each session; record gaze, head pose, glasses, blur, occlusion, brightness and missing frames. Use two blinded anatomical annotators, adjudicating disagreement by interval intersection. Where geometry is invalid, mark abstention rather than interpolating through unknown anatomy.
4. **Continuous-time envelope.** Independently bound maximum speed *between* samples. If a justified acceleration/smoothness certificate cannot be obtained, report only observed finite-difference speeds and set `certified_upper_envelope=false`. The statistical gate must fail closed.
5. **Participant-disjoint prediction.** Freeze a target population and nuisance strata; calibrate on distinct participants. For each held-out participant, freeze the physical shutter-gap/velocity predictions before examining the high-rate reference. Downsample with measured shutter/exposure, clock error and rolling-shutter timing. Score false exclusion of hidden closures, abstention coverage and nuisance failures. A single false exclusion under certified assumptions falsifies the corresponding deterministic physical claim; preserve the counterexample. Do not tune on held-out participants.
6. **Stopping rules.** No anatomical agreement or no authenticated clock: stop at measurement feasibility. No certified between-frame upper velocity: reject any hard hidden-closure exclusion. No participant-disjoint evidence: reject generalization. Any unmeasured nuisance: abstain. External independent reproduction and review are required before any release claim.

## Implementation acceptance criteria

- A dependency-free executable accepts only **aggregate, provenance-attested** calibration fields, never individual human frames/ratings.
- Exact participant-count threshold from `ceil(log(1-confidence)/log(p))`; reject frames/blinks as sample units, duplicate/invalid input, unverified timing, shutter, geometry, between-sample upper-envelope, independent annotation, nuisance strata or participant-disjoint holdout.
- Never turn a sample maximum or the 600-fps paper's group statistic into a universal speed bound.
- Even a passing statistical envelope is **RESEARCH_ONLY**, not a physical hidden-closure certificate, fatigue estimate or product release. Physical E002-371 testing must independently pass.
- Synthetic fixtures and adversarial tests must cover the n=58/59 and n=298/299 boundaries, unit confusion, invalid floats, missing provenance and population mismatch.

## Evidence / release

No new human annotations or instrument observations were obtained in this freeze. The contribution is a falsifiable **human validation sample-size and product-claim gate**, not a new mathematical theorem. E002-371 remains physically unvalidated; all physical hidden-closure, blink-duration, PERCLOS, fatigue and medical claims `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Preserve S01/S21-S31 separation and the rejected E002-491 proxy. No changes to Hush or the hourly workflow.
