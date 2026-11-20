# E002-564 RESULT | A cohort-mean inequality strengthens the human velocity lower-bound challenge, but does not certify an upper bound

Date: 2026-10-31. Frozen before implementation: [E002_564_FROZEN.md](E002_564_FROZEN.md), commit `0c551fa`. E002-371 primary kernel. Evidence tier: **published human cohort summaries + exact mathematics + independent local replay**, not newly annotated human sequences, original participant trajectories, calibrated shutter/clock or universal physiology.

## Primary empirical constraint

Kwon et al. (2013, https://doi.org/10.1098/rsif.2013.0227) report, for the **same 25 volunteers**, a mean peak closing velocity of **243 mm/s** and a mean initial palpebral aperture of **9.83 mm** (Table 1). Let each individual's measured peak speed be `v_i >= 0` and initial aperture be `a_i > 0`. If every `v_i/a_i < (sum v_i)/(sum a_i)`, summing `v_i < a_i (sum v_i)/(sum a_i)` yields a contradiction. Therefore at least one participant has

`v_i/a_i >= (mean v)/(mean a) = 243/9.83 = 24300/983 = 24.720244151 per second`.

This is stronger than E002-558's prior use of the **maximum** 12.8-mm aperture: `243/12.8 = 18.984375/s`; the improvement factor is `12.8/9.83 = 1.302136...`. The inequality is sharp when all individual ratios are equal and does not require individual-level pairing values, only that both means are calculated over the same cohort and compatible definitions. It is a classical weighted-average inequality, **not a novel general theorem**.

**What this does and does not falsify:** Under the published point estimates and consistent anatomical measurements, a universal normalized speed ceiling **strictly below 24.72/s** cannot hold for every member of that observed voluntary-blink cohort. This is an existence lower bound for at least one *measured peak*, **not** a safe upper ceiling, population quantile, guaranteed bound on every person, or certified continuous-time speed. The paper's standard errors and systematic errors are not deterministic guarantees. For illustration only, applying an adverse 10% systematic reduction to speed and 10% increase to aperture gives `20.225654305/s`; this is **not a confidence interval or certified error budget**.

## Independent historical cohort and a post-freeze denominator correction

Kwon's 2013 Table 1 transcribes Sun et al. (1997, PMID 9008634) electromagnetic search-coil results: for 8 adults aged 40-49, mean peak closing velocity **427 mm/s** and mean closing **excursion amplitude** **11.7 mm**. The exact group ratio is `427/11.7 = 4270/117 = 36.495726496/s`. For age 50-59 it is `329/10.2 = 32.254901961/s`; for 60-69, `349/10.6 = 32.924528302/s`. These are **secondary-table transcriptions**: Sun's primary abstract verifies study design and aging effect, not the numeric table values.

**Adversarial correction to the frozen plan:** The 1997 denominator is *blink excursion*, not independently established **initial palpebral aperture**. Therefore these ratios challenge excursion-normalized kinematics, **but cannot be transferred to E002-371's initial-aperture-normalized speed without additional anatomical equivalence evidence**. The frozen protocol's suggestion that 36.50/s directly challenges an initial-aperture ceiling is not established and is rejected. The executable now exposes a per-cohort `supports_initial_aperture_normalized_E002_371` gate and explicitly marks all Sun cohorts false. This negative finding is preserved rather than concealed.

## Reproducibility and controls

- [Exact Python executable](e002_564_cohort_ratio.py) uses `fractions.Fraction` for all four ratios and hypothetical systematic-bias calculations.
- [11 adversarial Python unit tests](test_e002_564_cohort_ratio.py) cover sharpness, unequal pairing, paired-cohort requirement, nonpositive aperture, negative speed, point-estimate tiers, and the critical initial-aperture-versus-excursion transfer rejection.
- [Independent Node.js BigInt oracle](e002_564_independent_replay.cjs) reproduces five exact rational results without importing the Python implementation.
- **Local execution:** 11/11 Python tests and 5/5 independent BigInt equalities passed. [Dedicated hosted CI](../../.github/workflows/e002_564_cohort_ratio.yml) was committed; hosted success must be checked separately and is not claimed here.

## New high-rate dataset suitability check (not an experiment)

Mathema et al., *Scientific Data* 2026, DOI https://doi.org/10.1038/s41597-026-06754-x, publish 1000-Hz EyeLink event labels for 251 participants. Their own paper notes fragmented blink labels (e.g. 51 labels in 0.41 s) as possible detector artifacts. The associated [Figshare dataset](https://doi.org/10.6084/m9.figshare.29312225) has one **11,104,408,472-byte** archive, verified via its public Figshare API metadata on 2026-10-31. It is not a small, independent **anatomical aperture** reference and was not downloaded. A 1000-Hz vendor blink label is not evidence of 1000-Hz anatomical closure sensitivity. This avoids another expensive, misleading proxy dataset sweep.

## Product and next experiment

The Kwon within-cohort result invalidates the **use of a universal speed ceiling below 24.72/s** as a conservative human bound under the reported point estimates. It does not license **any** universal upper ceiling. No E002-371 exclusion is permitted without independently certified participant/session-specific speed upper bounds, calibrated exposure kernel and clock, and anatomical error bounds.

**Next physical gate:** authenticated optical shutter/clock capture; two genuinely independent blinded anatomical raters on source high-rate video with verified acquisition timing; participant-disjoint prospective 30-fps counterfactuals. Prior E002-510 already exhausted S01 XML/CSV metadata-only checks; do **not** repeat them. The E002-563 AVI timebase remains unresolved.

Authenticated physical shutter captures **0**; independent human anatomical rater pairs **0**; certified continuous-time human velocity upper ceilings **0**; held-out physical closure predictions **0**. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. No Hush writes, merges or deployment.

Sources: https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/ ; https://pubmed.ncbi.nlm.nih.gov/9008634/ ; https://doi.org/10.1038/s41597-026-06754-x ; https://api.figshare.com/v2/articles/29312225 .
