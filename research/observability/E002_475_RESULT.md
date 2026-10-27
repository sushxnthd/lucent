# E002-475 RESULT — participant-level tail calibration cannot support a hard physiological speed cap

Date: 2026-10-27. **Evidence tier:** independently reproduced classical distribution-free order statistics plus adversarial synthetic checks, applied only to E002-459's *already published* calibration sample size. **No new human images, anatomical trajectories, timing calibration or physical acquisitions.** Frozen protocol committed before code at `cb4545c35887ea5b3389d435f3c62e1ea2ed9b41`.

## Falsified shortcut and quantitative boundary

E002-474 showed that the 2026 published **567.104-mm/s recorded closing-speed sample maximum** changes the nominal 240-fps design decision relative to a 243-mm/s cohort mean. But treating this sample maximum as a universal hard physiological cap is invalid even if the underlying recorded speed proxies were measured perfectly. Under the *optimistic* assumption of iid, continuous **participant-level maxima** from a stable population, the calibration maximum from **12 participants** has the following exact, unconditional properties:

| Statistical question | Exact answer | Interpretation |
| --- | ---: | --- |
| One future participant's proxy maximum does not exceed the 12-person calibration maximum | **12/13 = 92.31%** | Marginal prediction over repeated calibration/future sampling, not a 92.31%-confidence guarantee for the observed cap |
| All eight future participants' proxy maxima do not exceed that calibration maximum | **12/20 = 60.00%** | Joint marginal prediction under exchangeability |
| Confidence that the calibration maximum covers >=95% of the participant-proxy population | **1 - 0.95^12 = 45.96%** | Not 95%-confidence tolerance coverage |
| Independent calibration participants required for 95% population content with 95% confidence using a maximum | **59** | Classical one-sided Wilks tolerance limit; 58 fails |
| Independent calibration participants required for >=95% marginal joint coverage of eight future participants using a maximum | **152** | 151 fails; this is not a 95%-confidence tolerance statement |

Proof: For iid continuous participant-level proxy maxima, the global maximum among n calibration and m future observations is equally likely to occupy any of n+m ranks. The probability that it belongs to the calibration set is **n/(n+m)**. For a continuous CDF F, **F(max calibration) ~ Beta(n,1)**; hence P[F(max calibration) >= p] = **1 - p^n**. These are **standard order-statistic results, not new theorems**. Ties require appropriate conservative interpretation. Importantly, these are **unconditional** rank statements, not bounds on future values conditional on the realized training maximum.

## Independent verification and adversarial control

- The standalone Python implementation [e002_475_tail_calibration.py](e002_475_tail_calibration.py) uses exact fractions, high-precision decimal tolerance arithmetic, a separate exhaustive 120-permutation n=3/m=2 check, and seeded synthetic trials. **12 local Python regression tests passed.** The script rejects substitution of the **1,657 calibration blinks** for the 12 independent participants.
- An independent [JavaScript replay](e002_475_independent_replay.cjs), with no Python imports, reproduced all boundary integers, 72/120 successful permutations, and 45.963991% 12-person tolerance confidence. Local replay passed.
- A 25,000-trial iid Uniform(0,1) synthetic test gave **0.60204** joint eight-person coverage, within the frozen 0.02 tolerance of 0.6. An explicit **nonexchangeable** calibration Uniform(0,1) / future Uniform(2,3) control gave **0/25,000** coverage. These are synthetic sanity checks, not estimates of human failure rates.
- Dedicated hosted CI runs the Python suite, executable JSON output and independent JavaScript replay. **Do not claim hosted success until the workflow has completed.** The [aggregate](E002_475_AGGREGATE.json) contains no raw human rows.

## Priority and scientific scope

The relevant statistical principle predates Lucent: S. S. Wilks, *Determination of Sample Sizes for Setting Tolerance Limits* (1941), https://doi.org/10.1214/aoms/1177731788 ; NIST's tolerance-limit overview https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/tolelimi.htm ; and Minitab's nonparametric tolerance formulas https://support.minitab.com/minitab/help-and-how-to/quality-and-process-improvement/quality-tools/how-to/tolerance-intervals-nonnormal-distribution/methods-and-formulas/tolerance-intervals/ . **Novelty is not claimed for the rank or tolerance law.** This run contributes a claim-sensitive quantitative *failure gate* for the existing Lucent instrument design.

The published 2026 human study measured **per-blink peak speed proxies**. The rank laws do not establish their correspondence to continuous anatomical velocity, nor do they cover illumination, gaze, blur, glasses, geometry, clock errors, acquisition rates, distribution shift or individual rare motion. Even a 59-person iid proxy tolerance result would **not** provide the deterministic pointwise speed cap required by E002-371. Calibration participants are 12, not 1,657; the five held-out participants and S21/S22 remain sealed/not reopened.

## Product consequence and next external gate

**Reject every product pathway that promotes a finite participant sample maximum, even from a nominal 480-fps design, to a universal no-hidden-closure certificate.** If future physical and human validation establishes exchangeable measurement conditions, Lucent could eventually offer **qualified population-risk or empirical-coverage statements**, clearly separated from deterministic physical exclusion. For now the physical product remains `ABSTAIN_UNCALIBRATED` and the research tool may only display hypothetical conditional design sensitivities.

Do not reanalyse the 17-person speed CSV again. The next decisive scientific acquisition is the already specified independently timed optical-phase scan, moving-aperture ground truth and blinded anatomical reference study in [E002-472 handoff](E002_472_PHYSICAL_HANDOFF.md). If no physical instrument is accessible, preserve this as a **bounded theoretical/synthetic validation substitute**, not completion of the human-validation gate.
