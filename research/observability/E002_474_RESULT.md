# E002-474 RESULT — published cohort tail invalidates the conservative 240-fps pilot assumption

Date: 2026-10-27. **Evidence tier:** post-hoc comparison of two *already published* human-speed statistics with the previously frozen E002-472 instrument model, independently recalculated using exact rational arithmetic. This is **not** a new human experiment, a physical shutter measurement, or an independent physiological hard cap. [Analysis frozen before implementation](E002_474_FROZEN.md), commit `c3e81e8509aada0fb88d6ae51d914f17dfb6c686`.

## The consequential comparison

The E002-472 handoff preferred a **240-fps / 1-ms exposure** acquisition pilot, under illustrative speeds of 200 mm/s and a conservative symmetric shutter model. E002-473 found it conditionally feasible against a **243-mm/s published mean of peak voluntary closing speeds** (Kwon et al., 2013, https://doi.org/10.1098/rsif.2013.0227). But E002-459's checksum-linked 2026 human cohort already contained a **567.103928-mm/s calibration sample closing peak** (12 participants, 1,657 calibration blinks; source DOI https://doi.org/10.3758/s13428-026-02984-4). The two numbers describe different cohorts/statistics. Neither is a hard bound.

At the *same* fixed 1.0-mm endpoint margin, 0.1-mm uncertainty, 0.1-ms camera clock error, 0.2-ms reference exposure and 0.1-ms reference clock error, the existing E002-472 **conservative symmetric sufficient exclusion criterion** gives:

| Hypothetical camera | Critical symmetric speed (mm/s) | 243-mm/s mean-peak stress | 567.104-mm/s sample-peak stress | Strict required margin at 567.104 mm/s |
| --- | ---: | --- | --- | ---: |
| 30 fps / 4 ms | 50.657 | NOT SUPPORTED | NOT SUPPORTED | >10.176 mm |
| 240 fps / 1 ms | 369.863 | Conditionally feasible | **NOT SUPPORTED** | >1.480 mm |
| 300 fps / 1 ms | 446.281 | Conditionally feasible | **NOT SUPPORTED** | >1.244 mm |
| 480 fps / 1 ms | 646.707 | Conditionally feasible | Conditionally feasible | >0.889 mm |
| 600 fps / 1 ms | 760.563 | Conditionally feasible | Conditionally feasible | >0.771 mm |

These are model sensitivity calculations, **not** evidence that a real 480-fps camera is calibrated or that a 567-mm/s physiological speed cap is valid. The 2026 maximum is a finite-sample estimate and could be exceeded by unseen people. Even 480/1 does not authorize a physical no-closure claim.

**Model distinction is essential:** E002-460's *different, much stronger* assumption of known linear shutter-averaged **anatomical aperture in millimetres**, with separate closing/opening hypothetical caps 567.104/274.616 mm/s, yields a 5.404789-ms critical centroid gap, which conditionally excludes a dark-gap crossing at 240 fps (4.166667 ms). The conservative E002-472 failure does **not** prove a physical crossing exists or that 240 fps is intrinsically incapable. Real RGB pixel/landmark observations are not authenticated linear aperture averages; E002-455 previously demonstrated a proxy-specificity failure. The product cannot select the favorable model without independently proving its observation assumptions.

## Reproducibility and falsification

- [Executable post-hoc comparison](e002_474_cohort_tail_design.py) reads only the committed E002-459 deidentified aggregate with source SHA256 `6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43`. It imports the published-mean descriptor from E002-473 and checks every row against the **actual** E002-472 evaluator.
- [Ten adversarial regression tests](test_e002_474_cohort_tail_design.py) cover all frozen model flips, monotonicity, strict equality, source tampering, finite arithmetic and refusal of physical release. [Dedicated CI](../../.github/workflows/e002_474_cohort_tail_design.yml) is configured to run them. **Hosted success is not claimed until checked.**
- An independent local exact-rational calculation reproduces critical speeds 369.8630137 (240 fps), 446.2809917 (300 fps), 646.7065868 (480 fps) and strict margins 1.47995289, 1.24365959, 0.88921963 mm for the 2026 closing-peak stress. This verifies arithmetic, **not** the repository CI run.
- The 2013 voluntary mean and 2026 per-blink sample peak are not comparable population tail estimates. This is a deliberate **stress scenario**, not a new cross-cohort physiology inference. No S21/S22 holdout, raw video, participant rows or physical instrument was accessed.

## Product and experiment decision

**Do not market 240-fps/1-ms at 1-mm margin as a general-purpose conservative hidden-closure exclusion pilot.** It remains an appropriate *timing-calibration/acquisition pilot* if independently timed hardware can be obtained. A faster illustrative 480-fps/1-ms setting survives this particular conservative sensitivity calculation but cannot replace independent physical calibration, blinded anatomical human reference or a defensible cap. The next scientific action must be physical optical phase scan and moving-aperture acquisition, not another reanalysis of this same 17-person velocity table.

E002-371 remains **PHYSICAL_VALIDATION_NOT_ESTABLISHED**. Physical hidden-closure guarantees, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. PR #26 remains draft and unmerged; Hush PR #45 is independent.
