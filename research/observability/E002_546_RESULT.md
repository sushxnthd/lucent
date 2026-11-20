# E002-546 RESULT | The reference camera is not an oracle

Date: 2026-10-30. Primary E002-371 kernel. [Frozen protocol](E002_546_FROZEN.md) committed at `5ecb02b` **before** executable implementation. Evidence tier: **source-qualified high-rate human-data candidates and exact hypothetical instrument/sampling falsification**. Not a human empirical measurement.

## Decisive reference-instrument counterexample

A high-rate reference video can itself miss a genuine threshold crossing. In the frozen idealized model, aperture is 0.9 at both ends of a 10-ms interval, reaches 0 at 5 ms, and crosses the 0.2 closure threshold. The triangular trajectory has constructed speed magnitude 180 normalized-aperture units/s. This is an adversarial mathematical trajectory, **not an independently measured human velocity ceiling**.

The closure is at or below 0.2 for exactly `1/450 s = 2.222... ms`. With instantaneous periodic frames and uniformly random phase, the exact chance of at least one threshold-positive reference frame is `min(1, fps/450)`:

| Nominal reference fps | Detects crossing, uniform phase | Misses crossing, uniform phase | Adversarial phase can miss |
|---:|---:|---:|---|
| 30 | 1/15 = 6.67% | 14/15 = 93.33% | Yes |
| 100 | 2/9 = 22.22% | 7/9 = 77.78% | Yes |
| 200 | 4/9 = 44.44% | 5/9 = 55.56% | Yes |
| 240 | 8/15 = 53.33% | 7/15 = 46.67% | Yes |
| 500 | 1 = 100% | 0 | No, **only under this exact synthetic model** |

At 100 fps, phase zero samples the open endpoints (aperture 0.9), missing the closed midpoint. At 200 fps, phase 2.5 ms samples apertures 0.45 and 0.45, again missing the closure threshold. A different 200-fps phase (0 ms) captures the closed midpoint. Thus an apparently negative 100/200-fps reference is not a complete continuous-time negative label. Real exposure integration, anatomical uncertainty and timing error only add complications not covered by this idealized calculation. These are **not** estimates of real-world miss rates.

## New public-source qualification

Two independently described human-data candidates were identified, but both are access-gated:

- [Silesian5, original research page](https://www.blinkingmatters.com/research): 100-fps Basler camera, 5 people, 300 blinks, 58,884 annotated frames after conversion; video access requires approval and license agreement. Author notes imprecise original blink intervals and codec truncation. Suitable for observed-positive falsification and nuisance tests after permission, **not** unquestioned closure-negative labels.
- [OpenEDS, original 2019 paper](https://arxiv.org/abs/1905.03702): 200-Hz eye-facing video capture across 152 people, short sequences; available upon request. Segmentation and eye-region images do not by themselves establish continuous-time lid closure absence. Requires visibility and usage-rights qualification.

Neither source's videos were obtained or analyzed. No dataset rights were bypassed. This is not another metadata audit: the candidate-rate result directly changes **which reference labels are scientifically admissible** in the E002-371 held-out experiment.

## Reproducibility and scientific decision

[Exact rational Python executable](e002_546_reference_alias.py) contains prespecified assertions for five rates, constructed velocity, phase counterexamples, invalid phases and exact geometry. [Independent Node.js oracle](e002_546_independent.cjs) uses separate arithmetic and checks the same five exact rates and geometric witnesses. [Hosted workflow](../../.github/workflows/e002-546-reference-alias.yml) executes both. CI success must be verified separately; do not infer it from workflow creation.

**Decision:** positive high-rate frames can serve as witnesses to falsify a low-rate exclusion; negative high-rate frames cannot certify no hidden closure without additional coverage assumptions. This is a measurement-science *validity boundary*, not a novel sampling theorem or physiological result. Do not claim a verified human blink miss rate, a validated E002-371 speed ceiling, or a consumer-grade closure detector.

## Next decisive experiment

Acquire authorized Silesian5/OpenEDS data only with permission, and use observed positives for one-sided falsification. Separately obtain photodiode-authenticated physical shutter response and independently bounded continuous-time eyelid dynamics from a sufficiently fast reference/auxiliary instrument. Freeze participant-disjoint predictions before examining held-out labels, including exposure integration and geometry, brightness, blur, gaze, glasses, missingness and clock errors. If access cannot be obtained, execute the already frozen local S01 two-rater handoff and physical optical experiment rather than more synthetic tuning.

**Evidence still missing:** physical shutter captures 0; independent human anatomical ratings 0; certified continuous-time human velocity ceilings 0; participant-disjoint physical predictions 0. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. No Hush edits or merges.
