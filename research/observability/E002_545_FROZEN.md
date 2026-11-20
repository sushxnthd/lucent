# E002-545 FROZEN | Paired randomized optical-edge falsification

2026-10-30. E002-371 primary kernel. Frozen before writing the executable or inspecting any new outcome. Evidence tier: prospective instrument-design protocol and synthetic validation only.

## Question and preregistered decision

Can within-session randomized flash/sham pairs control the *whole edge-position search* without relying on exchangeability between calibration sessions and a shifted held-out session (the E002-544 failure)? Test the **sharp no-effect null**: for each pair, the complete K-position sensor-response vector would be unchanged if its flash and sham assignments were swapped. This is not the null that the shutter is correctly specified.

Each pair has two complete blocks of K fixed, predeclared edge positions, one receiving the outside-exposure flash and one receiving sham. A private, externally auditable uniform random bit chooses which block gets flash. For each position j compute D_ij = observed flash-block response minus sham-block response. Predeclared statistic T = max_j sum_i D_ij (one-sided positive response). Enumerate all 2^n *whole-vector* sign flips, not per-position flips. p = count(T_flip >= T_observed)/2^n, including ties. Declare FALSIFICATION_CANDIDATE_RANDOMIZED if p <= 0.05; otherwise NO_RANDOMIZED_EVIDENCE. Any invalid or incomplete evidence -> ABSTAIN.

**Validity:** Under genuine independent fair assignment, sharp null, no spillover/carryover, and fixed potential outcomes independent of assignment, the exact randomization p-value is superuniform conditional on all potential outcomes. Arbitrary position correlation, nonstationary block responses, heteroskedasticity and between-session drift do not invalidate this conditional result *under these assumptions*. It is not a guarantee under adaptive intervention timing, compromised assignment, block-order/carryover effects, or exposure mismatch.

## Frozen synthetic attacks and independent checks

- Exhaustive null relabelling for n=4 with fixed arbitrary vectors: empirical exact rejection probability <= 0.05; with n=4 minimum attainable p is 1/16, so never reject.
- n=8, K=5: strong positive intervention vector should yield p=1/256 when all eight pair differences are positive and all positions share the signal. Zero signal/ties must give p=1.
- n=8, K=5: correlated positions and heterogeneous block baselines; exact enumeration must remain valid under sharp null, without independent-position permutations.
- n=8, K=5: inject flash-induced carryover into the sham block; explicitly mark randomized test guarantee INVALID even if nominal p small.
- A 200-position synthetic scan with common pairwise drift; compare max-statistic p to invalid naive per-position thresholding without retuning thresholds.
- Independent verifier: implement an alternative enumerator (or exhaustive manual oracle) and check counts; reject nonfinite values, duplicated pair IDs, missing positions, mismatched arm lengths, non-binary or repeated assignments, unverified timing/quality assertions, and fewer than 5 or more than 16 pairs.

No calibration threshold may be tuned using outcomes. Do not claim physically authenticated randomness, shutter support, human velocity bounds or anatomical labels. Product remains ABSTAIN_UNCALIBRATED and BLOCKED even on a candidate.

## Physical handoff

Randomize the *order* of flash and sham acquisition inside matched pairs using an independently retained assignment log and reveal it only after immutable capture. Use external photodiode and camera clock traces, confirm all flashes lie outside the entire uncertainty-expanded shutter support, and run separate control blocks to falsify spillover, saturation, rolling shutter, gamma/ISP response, autoexposure, motion, gain, temperature and illumination drift. Predefine 200 edge positions, ROI, exposure settings, paired block timing and a single family-wise decision. Record missing/corrupt blocks as ABSTAIN, never silently drop them. Independently replay raw optical signals. A statistical flash effect is a **transfer-model anomaly candidate**, not a shutter error or an eyelid closure observation. Proceed to blinded two-rater human validation only after physical calibration.
