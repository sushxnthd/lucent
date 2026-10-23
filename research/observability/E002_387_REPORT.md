# E002-387 — finite-exposure reference labels can miss physical threshold crossings

**Status:** prospective synthetic-instrument falsification, not human validation. Protocol frozen in E002_387_FROZEN.md at commit ef0f640a5941246fe9d3e26df07ca7d0e91f7965 before evaluation. This is the E002-371 observability kernel.

## Experimental question
Can 240-fps video be used as unquestioned ground truth for a physical eyelid threshold crossing? **No.** Exposure integration can remove a threshold excursion even if the physical aperture crosses the threshold. Nominal frame rate is insufficient to establish reference adequacy.

## Frozen instrument and results
Physical aperture a(t)=min(1,h+V|t-t0|), V=40/s, theta=.2, minima h in {.17,.185,.195}. Durations are 1.5, .75, .25 ms. Evaluate 10,000 deterministic onset phases per configuration, 240 and 960 fps, 0/.5/2/4 ms exposures when exposure <= frame period. Each reference measurement is the exact continuous-time exposure mean. Reference reports crossing only if a sample mean is strictly below theta.

| h | Physical excursion | 240 fps point | 240 fps 0.5ms | 240 fps 2ms | 240 fps 4ms | 960 fps point | 960 fps 0.5ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0.17 | 1.5 ms | 36.00% | 36.00% | 33.94% | 0.00% | 100.00% | 100.00% |
| 0.185 | 0.75 ms | 18.00% | 18.00% | 0.00% | 0.00% | 72.00% | 72.00% |
| 0.195 | 0.25 ms | 6.00% | 0.00% | 0.00% | 0.00% | 24.00% | 0.00% |

All percentages are exact fractions of the frozen phase grid, not human detection rates. Independent adaptive-quadrature checks: 150 configurations; maximum absolute difference 1.39e-15. Six independent point-phase-law checks passed. P1 (point sampling p=min(1,D*f)), P2 (240 fps / 4 ms misses all three), P3 (960 fps / 0.5 ms detects all 1.5-ms but none of 0.25-ms excursions), and P4 (fail-closed negative-reference qualifier) passed.

## Sharp exposure-erasure condition
For an unsaturated symmetric triangular aperture valley, the smallest possible exposure-averaged aperture is h+V*e/4. Define Lambda=V*e/[4*(theta-h)]. If Lambda>=1, **no** shutter exposure can report a strict threshold crossing regardless of sample phase or FPS. This is a conditional boxcar-convolution identity, not a new physiological theorem. For h=.17 and V=40/s, any exposure e>=3ms erases the threshold excursion under this strict label rule.

## Scientific limitation
This synthetic trajectory represents a **submillisecond-to-millisecond threshold excursion, not a complete human blink**. It does not establish human speed bounds, camera optical calibration, reference annotation quality or field reliability. Geometry, gaze, glasses, missingness, blur, illumination, RGB nonlinearities and clock error were NOT physically validated. The earlier E002-386 risk-control result remains separate.

## Product and human-validation consequence
A high-speed reference's negative label is not automatically evidence of no physical threshold crossing. Require independently measured reference exposure and timestamp bounds, calibrated optical-to-aperture response, and a speed/acceleration envelope that makes missed crossings impossible; otherwise label REFERENCE_UNRESOLVED and abstain. No hard no-hidden-closure, PERCLOS or five-second fatigue diagnosis is justified.

## Primary literature / data access
Espinosa et al. (PLOS ONE 2018, DOI 10.1371/journal.pone.0196125) recorded 26 subjects at 240 fps; their linked University of Alicante data repository did not yield accessible raw continuous recordings in this run. Silesian5 100-fps videos require signed permission (blinkingmatters.com/research). mEBAL2 includes RGB/NIR/EEG but is license-gated and its ordinary RGB is not a high-speed physical reference. Two targeted dataset searches were completed; this run used the stipulated synthetic fallback. These references are context, not independent replication.

## Reproduction
Run `python research/observability/e002_387_reference_aliasing.py` with numpy and scipy. The deterministic output is `e002_387_results.json`. The detailed 60-participant paired-camera protocol is in E002_387_HUMAN_STUDY.md. The full SVG figure and archive are available in the associated run artifact.
