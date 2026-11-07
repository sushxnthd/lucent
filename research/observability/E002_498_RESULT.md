# E002-498 | Participant-level speed-envelope calibration gate: implementation result

Date: 2026-10-28. Primary E002-371 human-validation workstream. This is **human-study preregistration and claim-control engineering**, not an observed physiological result or a new theorem.

## Decisive evidence gap

The existing 20×13 S01 anatomical-review packet is an operational pilot, not a population-calibration cohort. No independent anatomical ratings or physically authenticated camera/shutter timing are available. The E002-493 image-motion proxy remains falsified under jitter and temporal subsampling. The high-speed voluntary-blink literature reports measured velocities but does not provide a universal hard eyelid-speed limit (https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/). The 1,000-Hz GazeBase eye-tracker data contain gaze/pupil information and parser blink labels, not continuous-time certified eyelid speed bounds (https://doi.org/10.1038/s41597-021-00959-y).

A high frame rate **alone** cannot certify a continuous-time upper velocity between samples without a physical/smoothness assumption. Consequently, no finite-difference measurement or published group mean can be substituted for the physical speed premise of E002-371.

## Frozen new experimental criterion

E002_498_FROZEN.md preregisters a two-rater anatomical pilot, independent optical timebase and exposure calibration, continuous-time speed-envelope certification, participant-disjoint held-out predictions and explicit nuisance/abstention criteria. For genuinely independent, identically distributed participant-level *certified upper bounds*, the known distribution-free maximum-order-statistic tolerance relation gives confidence at least `1-p^n` for coverage `p`. This is **statistical population coverage**, not a deterministic bound on all humans.

Independent arithmetic cross-check, without any human data:

| Target population coverage | Confidence target | Minimum independent participants | Confidence one fewer | Confidence at threshold |
| --- | --- | ---: | ---: | ---: |
| 95% | 95% | 59 | 94.8953% | 95.1505% |
| 99% | 95% | 299 | 94.9963% | 95.0464% |

The count is **distinct independently sampled people**, not blinks, video frames, or repeated visits. The result depends on exchangeability and individually certified upper envelopes; neither is established by the present S01 dataset. The sample-size arithmetic is a planning constraint, not evidence that these participants have been studied.

## Persisted implementation

- `e002_498_velocity_evidence_gate.py`: dependency-free aggregate-only evidence gate. Rejects wrong sample units, missing timing/shutter/geometry/anatomy/continuous-time-envelope provenance, incomplete geometry/brightness/missingness/blur/gaze/glasses/sampling/clock/shutter nuisance inventory, non-disjoint holdout, mismatched populations, nonfinite speed, invalid probabilities and individual-record payloads.
- `test_e002_498_velocity_evidence_gate.py`: 18 synthetic adversarial test methods covering both exact n thresholds, every critical evidence category, hard-claim rejection and privacy.
- `.github/workflows/e002_498_velocity_evidence_gate.yml`: hosted Python tests plus an independently written Node.js order-statistic boundary check.
- Independent JS arithmetic computed exact threshold confidence values above; **this is not human validation**.

The only passing result possible from a fully self-attested *synthetic* aggregate is `STATISTICAL_ENVELOPE_RESEARCH_ONLY`. It **never** sets physical hidden-closure certification or product release to true. No actual human aggregate is submitted or certified. CI status should be checked against the exact final commit; a queued run is not a pass.

## Kill / continue

If a real independently authenticated upper velocity cannot be certified between high-rate samples, stop the deterministic hidden-closure claim even if many human videos are acquired. If the calibrated sample cannot meet participant-level independence, the distribution-free population claim is unavailable. No external review, participant-disjoint held-out falsification, or calibrated product exists.

**E002-371 physical validation:** NOT ESTABLISHED. **Human anatomical labels:** 0. **Authenticated camera/shutter calibration:** 0. **Held-out physical prediction:** 0. **Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`.

Next substantive work: obtain two independent S01 anatomical review sheets and independent physical timing; do not substitute more mathematical rehearsal for either. Hush PR #45 and existing Lucent hourly automation remain unchanged.


## Hosted verification (2026-10-28 00:45 UTC)

[GitHub Actions run 40610676412](https://github.com/sushxnthd/lucent/actions/runs/40610676412) **completed successfully** on exact implementation/test/workflow commit `28b5a64420aaec74b80b7072fd8dfadb3143fd87`. Hosted Python executed **18/18 adversarial tests successfully**; the independently written Node.js boundary check printed `INDEPENDENT_ORDER_STATISTIC_BOUNDARIES_PASS`. This verifies software behavior and known sample-size arithmetic across two runtimes. It does **not** validate a physical camera, any human upper eyelid speed, the exchangeability assumption, or any E002-371 hidden-closure prediction. No product release.
