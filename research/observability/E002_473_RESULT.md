# E002-473 RESULT — published human blink speeds stress the proposed camera design

**Date:** 2026-10-27. **Evidence tier:** published human cohort statistics from primary peer-reviewed literature, plus an independent arithmetic stress test of Lucent's existing E002-472/E002-456 *conditional* model. **No new raw human video, new anatomical annotations, physical shutter calibration, or independently established physiological hard cap.** [Prospectively frozen protocol](E002_473_FROZEN.md) was committed first at `08dbc1c0106461fc77d939ceec0cd659917deb92`.

## New external human evidence and interpretation

Kwon et al. (2013), *Journal of the Royal Society Interface* 10:20130227, https://doi.org/10.1098/rsif.2013.0227 , directly imaged 25 volunteers at **600 fps** using a Phantom camera and measured palpebral aperture at 5-ms analysis increments. Their **243 ± 9 mm/s** figure is the mean of individual *peak voluntary closing-aperture speeds* (authors' SEM). This is a real published human measurement, not a sample maximum, not a deterministic upper bound, and not a validated camera-shutter model.

A separate 2019 240-fps spontaneous-blink study, PMID 30893187, https://pubmed.ncbi.nlm.nih.gov/30893187/ , reports a **93 mm/s mean closure velocity** and a **40–160 mm/s observed range** in ten volunteers. It is not a matched estimate of the same peak-voluntary aperture-speed quantity.

Kwon's Table 1 secondarily reports a **427 ± 30 mm/s** 1997 search-coil mean peak in eight adults aged 40–49 (Sun et al., *IOVS* 38:92–99, https://pubmed.ncbi.nlm.nih.gov/?term=Sun+Barker+Chuke+Age-related+changes+human+blinks+1997 ). This is a **coil-marker modality**, not directly interchangeable with an optically measured palpebral aperture. The original 1997 primary article has **not** been independently checked for this number. Use 427 only as a cross-modality stress scenario, not as a hard bound or as a direct biological counterexample to the optical model. Kwon discusses coil mass and geometric mismatch explicitly.

## Prespecified design predictions verified by independent arithmetic

Frozen assumptions: uniform symmetric shutter; both endpoint apertures 1.0 mm above closure threshold; 0.1-mm endpoint uncertainty; 0.1-ms ordinary clock error; 0.2-ms reference exposure and 0.1-ms reference clock error. The existing E002-472 **sufficient**, not necessary, criterion gives
`Vcrit = 900 / [w/4 + (1000/fps + 0.2)/2]` mm/s.
For a chosen velocity stress V, the strict required aperture margin is
`m > 0.1 + V*[w/4 + (1000/fps + 0.2)/2]/1000` mm.
The dimensionless sensitivity `V/Vcrit` must be **strictly less than 1** and shutter/reference dark-gap support must independently exist.

| Camera assumption | Critical speed | V=243 mm/s (optical mean peak) | V=427 mm/s (coil stress only) |
|---|---:|---|---|
| 30 fps, 4-ms exposure | 50.6567 mm/s | **NOT SUPPORTED**; margin >4.4173 mm needed | **NOT SUPPORTED**; margin >7.68637 mm needed |
| 240 fps, 1-ms exposure | 369.8630 mm/s | conditionally feasible; margin >0.6913 mm | **NOT SUPPORTED**; margin >1.13903 mm needed |
| 300 fps, 1-ms exposure | 446.2810 mm/s | conditionally feasible; margin >0.59005 mm | conditionally feasible; margin >0.96112 mm |

Across all **12** prespecified literature-statistic stress scenarios (V=93,160,243,427 for each of three designs), **7** are conditionally feasible and **5** not supported. No row is a physical exclusion certificate. The 300-fps example is a hypothetical *design target*, not evidence of a calibrated camera or human hard cap.

The 30-fps / 4-ms 1-mm-margin configuration is rejected even against the published **243 mm/s mean peak** stress scenario, which is roughly 4.80 times its conditional critical speed. This is stronger external physiological context than the earlier E002-472 purely hypothetical 100-mm/s sensitivity. The 240-fps / 1-ms configuration is **not universally safe** merely because its critical speed exceeds the 2013 mean peak; the coil scenario exceeds its threshold, and neither statistic is a universal cap.

**Product consequence:** forbid any marketing or runtime rule equating nominal fps, population mean blink speed, a sample maximum, or published SEM with a deterministic no-hidden-closure certificate. A candidate instrument configuration may only be called *conditionally model-feasible*; the released product remains `ABSTAIN_UNCALIBRATED`. A camera with a faster nominal frame rate can still fail due to exposure width, reference support, geometry or clock uncertainty.

## Reproduction, adversarial checks and limitations

- [Executable grid](e002_473_literature_stress.py) uses Python `Fraction` for independent rational calculations, cross-checks E002-472, and emits machine-readable 12-row results without raw human measurements.
- [Ten adversarial tests](test_e002_473_literature_stress.py) include four frozen decisions, strict boundary and margin arithmetic, literature modality mismatch, fail-closed physical release, missing dark-gap, dimensionless-ratio consistency, and **all twelve actual E002-456 evaluator comparisons**.
- An independent JavaScript recomputation of all twelve configurations yielded **7 feasible / 5 unsupported**, with matching critical speeds and margins. This verifies the arithmetic only, not execution of the repository test suite.
- [Hosted workflow](../../.github/workflows/e002_473_literature_stress.yml) was committed for independent CI; **hosted pass is not claimed until the run is checked**. The E002-455 optical-proxy specificity failure remains in force and is not rehabilitated by this result.
- Published values differ in voluntary/spontaneous stimulus, measurement apparatus, geometry and statistic (mean, peak, range). A cohort mean, observed range, SEM, or empirical sample maximum cannot be promoted to a universal Lipschitz speed bound. This stress test does not identify any participant's actual eyelid speed.

## Next decisive gate

Acquire independently timed optical shutter calibration and moving-aperture ground truth as already specified in [E002-472 physical handoff](E002_472_PHYSICAL_HANDOFF.md), then collect consented, blinded, participant-disjoint human anatomical reference. Without that, E002-371 is **not physically validated**, and hidden closure, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. Do not merge PR #26 or deploy. Hush PR #45 is independent and untouched.
