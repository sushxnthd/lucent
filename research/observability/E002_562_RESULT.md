# E002-562 RESULT | Sealed 400-to-30-Hz one-sided reference replay

Date: 2026-10-31. Primary E002-371 kernel. [Frozen before code](E002_562_FROZEN.md). Evidence tier: **synthetic 400-Hz anatomical-aperture traces, real executable, local adversarial tests, primary-literature human-source constraints**. No original FaceBase/Synapse human sequences accessed or analyzed; no physical shutter or hard human velocity ceiling measured.

## The decision this experiment tests

A high-rate positive anatomical observation can falsify a predeclared ordinary-camera hidden-closure exclusion. A high-rate negative sample cannot prove continuous-time absence. The new two-stage executable makes that asymmetry operational: `predict` refuses reference-positive labels and SHA256-seals participant-disjoint, 13-phase 30-Hz ideal-point predictions; `adjudicate` subsequently accepts positive witness timestamps and counts only strictly interior candidate contradictions, including uncertainty margins. A hash seal detects unintentional changes, **not** adversarial post-hoc manipulation, independent provenance or pre-registration with a trusted timestamp.

Eight synthetic 400-Hz participant traces (four held out by the E002-550 SHA256 split) each contain a Lipschitz triangular closure reaching normalized aperture zero at 12.5 ms. The actual continuous-time maximum speed is 80/s. We compared the correct stipulated hard ceiling to an invalid understated 10/s ceiling. Threshold was 0.2, aperture error zero, declared clock error zero; 1.25 ms quantization uncertainty was added to each endpoint.

| Frozen synthetic control | Correct hard V=80/s | Incorrect hard V=10/s |
|---|---:|---:|
| Held-out participants | 4 | 4 |
| 30-Hz phase offsets | 13 | 13 |
| Evaluated intervals | 1,512 | 1,512 |
| Conditional exclusions | 0 | 1,484 |
| Abstentions / inconsistent intervals | 1,512 | 28 |
| Candidate excluded gaps containing witnessed closure | 0 | 8 |
| Held-out participants with candidate contradiction | 0 | 4 |
| Independently verified human contradictions | 0 | 0 |

**Negative result:** the correct 80/s ceiling makes this 30-Hz ideal-point experiment entirely uninformative for closure exclusion; it abstains on every gap. The falsely optimistic 10/s ceiling yields high apparent coverage but eight candidate contradictions. These are constructed trials, not population rates or evidence of actual human velocity bounds. They illustrate how a velocity ceiling that is too small can make a safety-style exclusion look useful while being wrong.

For two maximally open instantaneous endpoints (a=b=1), negligible aperture error and closure threshold theta, the dimensionless exclusion feasibility ratio is `Lambda = V*(d+2u)/(2*(1-theta))`. When Lambda >= 1, even perfectly open endpoints cannot exclude hidden closure under the stipulated Lipschitz model. With V=80/s, d about 1/30 s, u=1.25 ms and theta=.2, Lambda is about 1.79. This is a conditional algebraic consequence, **not** an independently established human law.

## Primary human evidence changes interpretation

Kim et al., *PNAS* 2025, DOI [10.1073/pnas.2508058122](https://doi.org/10.1073/pnas.2508058122), measured 3D eyelid-margin trajectories at **400 frames/s**, with 120-fps companion video and hardware synchronization. The paper reports behavior-specific two-dimensional motion, reflexive blink faster than other behaviors, and incomplete average spontaneous closure. Its FaceBase original-motion record [88-28BJ](https://doi.org/10.25550/88-28BJ) is the proper prospective source; the published supplementary MP4s are edited reconstructions, not original 400-Hz sensor reference. The study's **blink-behavior labels must not be substituted for anatomically confirmed complete closure**, and its sampled velocities do not certify a universal continuous-time ceiling. An independent 150-fps Phantom dataset is described by [Guttmann-Flury et al., Scientific Data 2025](https://doi.org/10.1038/s41597-025-04861-9), but its original synchronized files are also not in hand.

## Reproduction and deliberate failure tests

```bash
cd research/observability
python -m unittest -v test_e002_562_replay.py
python e002_562_replay.py predict --input PRIVATE_MARKER_APERTURES.json --output PRIVATE_SEALED_PREDICTIONS.json
python e002_562_replay.py adjudicate --prediction PRIVATE_SEALED_PREDICTIONS.json --witness PRIVATE_BLINDED_POSITIVES.json --output aggregate.json
```

**11/11 local adversarial tests passed**: valid hard V, understated V, absent V, unverified point exposure, blur nuisance, reference-label leakage, duplicate IDs, nonmonotone sensor time, modified prediction, mismatched source, duplicate witness, all-open reference censorship, and nonfinite aperture (some assertions share test methods). Hosted CI outcome is to be checked separately.

The script enforces syntactic separation of reference positives, the fixed eight-person split and strict timestamp containment. It cannot authenticate a supplied certificate flag, true camera acquisition time, human rater independence or sensor originality. It cannot turn 400-Hz negative frames into continuous-time absence. The generated prediction file contains private opaque participant identifiers; keep it off GitHub. Publish only the aggregate report after external verification.

## Next decisive human experiment and release gate

Obtain authorized original FaceBase 400-Hz 3D tracks, original participant/trial IDs, original sensor timing and fixed facial reference markers. Privately convert to normalized local upper/lower anatomical aperture without moving denominators or pooled 2D paths. Freeze participant split and hard kinematic/geometry/clock/shutter certificates independently; if any cannot be established, the executable must abstain. Seal all 30-Hz counterfactual predictions **before** revealing withheld anatomical positives. Obtain independent blinded anatomical ratings and provenance review for every candidate. Repeat under real synchronized 30-Hz camera exposures, since the ideal-point counterfactual does not model boxcar, rolling shutter or nonuniform shutter kernels. Report all participant/behavior/nuisance strata and abstentions, including negatives.

**Product consequence:** at a conservatively large independently certified motion ceiling, 30-Hz closure-negative coverage can collapse to zero. Lucent should present `ABSTAIN_UNCALIBRATED`, not an inferred negative blink or fatigue measurement. Production remains `BLOCKED`.

**Evidence counters:** authenticated physical shutter captures 0; independently blinded human rater pairs 0; independently certified human continuous-time velocity ceilings 0; participant-disjoint physical predictions 0. The 8 synthetic candidate contradictions in the understated-V control are not human evidence.
