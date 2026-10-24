# E002-414 — frozen prospective human claim-power gate

**Frozen 2026-10-24 before implementation.** Evidence tier: prospective statistical study-design / falsification of overconfident validation denominators. This is not new human annotation, a new mathematical theorem, or a physical shutter/velocity calibration.

## Question

How many **independent held-out human participants** with independently witnessed, calibrated shutter-gap challenges are needed before a zero-error validation result can support even a **statistical** upper bound on the participant-level rate of at least one false no-hidden-closure certificate? Can the existing 632 high-speed human-video frames from two participants establish that rate? (No: they have no physical reference or certificates, and frames are correlated.)

## Predeclared estimands and assumptions

For participant i, Y_i = 1 iff at least one physically false `CONFIRMED_NO_CROSSING` certificate occurs among independently reference-resolved, preselected eligible challenges; otherwise 0. A participant with no eligible, reference-resolved, non-abstained certificates is **not evaluable**, not a success. Preselect challenges before revealing reference. Count a participant with any false certificate once. Assume held-out participant-level outcomes are independent and identically distributed **within the specified target device/nuisance population**, with immutable protocol and no tuning on validation participants. These assumptions cannot be inferred from an error-free result. Require independently authenticated physical aperture, shutter/clock, geometry and deterministic velocity calibration for any physical product certification; flags in a JSON file are not authentication.

For n evaluable independent participants and k participants with >=1 false certificate, use the exact one-sided 95% Clopper–Pearson upper confidence limit for the Bernoulli participant-level failure probability. For k=0, U=1-0.05^(1/n). Do **not** count frame observations, gaps, sampling phases, rater duplicates or repeated sessions as independent participants. If the participant/device independence assumption is unjustified, the statistical qualification is **not established**.

A separate *research-only* statistical-velocity calibration of n_cal exchangeable participant maxima against m future participants has marginal exceedance probability <=m/(n_cal+m), and is not a deterministic hard velocity bound. A 5% total illustrative budget may allocate 2.5% to calibration exceedance and 2.5% to held-out validation failure; the union bound requires additional assumptions and cannot itself authorize product certificates.

## Frozen numerical predictions (before coding)

1. Zero failures among n=2 evaluable participants gives U=0.77639320225; n=20 gives U=0.13910834067. Treating 632 correlated frames as independent would incorrectly report U=0.00472886625.
2. To attain U <= 0.05 with zero participant failures and 95% confidence, n=59 is sufficient but n=58 is not. For U <= 0.025, n=119 is sufficient but n=118 is not.
3. For m=10 future participant maxima and a 2.5% marginal exceedance allocation, at least n_cal=390 independent calibration participants are required; if validation participants must be disjoint and zero-failure 2.5% validation uses 119 participants, the **illustrative** combined study has at least 509 participants, before nuisance/device replication. This is a design cost, not an observed empirical result or a deployable guarantee.
4. One failure among n=59 must yield an upper bound greater than the zero-failure case. Any participant with zero reference-resolved certificates must be rejected from the denominator. Duplicate participant IDs, mixed devices without stratification, missing independent-reference provenance and unreviewed domain shift must fail closed.
5. Under all synthetic fixtures, physical product state stays `ABSTAIN_UNCALIBRATED`. A passing statistical research gate never emits `CONFIRMED_NO_CROSSING`.

## Execution and controls

Implement standard-library-only exact binomial inversion with an independent binomial-tail oracle, a minimal per-participant validation manifest schema, adversarial duplicate/abstention/device/clock/reference checks, and a command-line power-planning report. Run regression tests without uploading human eye images or raw annotations. Preserve the negative implication for the existing S01/S19 acquisition evidence. Do not simulate human ratings or claim physical validation.

## Scientific consequence

If these predictions hold, freeze a realistic minimum participant-level validation plan and prohibit using correlated frame totals to claim rare false-certificate risk. The E002-407 two-rater pilot remains an **annotation-feasibility study** only. E002-371 still requires independently calibrated human physical-aperture trajectories and unseen-participant prospective predictions.
