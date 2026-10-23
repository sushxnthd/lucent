# E002-386 frozen prospective selective-risk protocol
Frozen 2026-10-23 before running E002-386 evaluation. This experiment addresses the E002-385 failure in which clipwise marginal optical coverage did not control error among issued no-hidden-closure certificates.

## Scope
Synthetic reference instrument only. **Not** a human or physical-camera result. The single scientific kernel remains E002-371 shutter-gap observability; this run tests the calibration-to-product step, not a new physiology law.

## Fixed measurement model
Aperture a(t) in [0,1], threshold 0.2, Lipschitz bound V=40/s, 30-Hz global shutter, 10-ms exposure, two consecutive shutter exposures, with the 23.333-ms intervening blind gap. The hidden-event reference is a triangular aperture valley with minimum in [0.17,0.195] at the gap midpoint and slope V, clipped at 1; the open reference is constant 1. Each synthetic exposure is integrated numerically using fixed midpoint quadrature. Independently check selected integrals by adaptive quadrature and speed bounds by direct formula. Treat optical aperture-estimator outputs as surrogate measurements, not physical RGB pixels.

## Sampling and nuisance
Use independent seeded calibration (n=6000), in-distribution held-out test (n=30000), and unseen-device held-out test (n=30000), plus 100 independently seeded calibration/test replications if compute permits. P(open)=0.35. On hidden clips, 5% receive positive correlated optical bias sampled U(0.07,0.14) on both exposures; otherwise bias U(-0.002,0.002). Independent frame jitter U(-0.002,0.002). Quality proxy q is U(0,0.6) for normal clips and U(0.25,1) for confounded clips. The unseen-device test adds a further *unrecognized* confound to 12% of hidden clips with bias U(0.18,0.26) and quality proxy U(0,0.6). Also test explicit missingness and unknown timing as fail-closed gates.

## Predeclared selective policy
Compute the conservative naive gap safety margin using E002-385's exposure-to-endpoint lower bound with e=0.002. A candidate issues a **statistical risk-qualified** decision only when margin >= m and quality <= q. Candidate grid m in {0,.04,.08,.12,.16,.22,.26,.30}, q in {.30,.50,.75,1.0}, K=32. On independent calibration labels, count issued n and false issued k. Use one-sided exact Clopper-Pearson upper bound Beta^{-1}(1-delta/K;k+1,n-k), with delta=.05 and n>0. Select the candidate with largest calibration issue fraction among those with upper bound <= alpha=.02; deterministic ties prefer smaller risk bound, then higher m, then lower q. If none qualifies, issue no decisions. For any unrecognized device, missing frame, or unknown timing, ABSTAIN; do not assert physical no-hidden-closure guarantee.

## Frozen hypotheses and kill criteria
P1: naive margin>0 has conditional false-issuance rate >.02 on in-distribution holdout.
P2: selected calibrated policy has in-distribution held-out conditional error <=.02, while issuing at least 10% of clips. Failure is reported, not tuned away.
P3: applying the calibrated thresholds *without* the device gate to the unseen-device test increases conditional false-issuance rate above .02. If not, report falsification of the shift hypothesis.
P4: product policy abstains on unknown device, missingness, and unknown timing; hard deterministic physical guarantee never issued.
P5: in 100 independent repetitions, simultaneous CP calibration bound covers the true per-candidate conditional risks in at least 90 of 100 trials; failures reported.
No thresholds, seeds, or nuisance distributions may be altered after the run without a new preregistration.

## Interpretation
Exact finite-sample binomial risk statements require IID/exchangeability of calibration and deployment clips and independently known ground-truth labels. They are not deterministic per-event guarantees, are not distribution-free under device shift, and are not a replacement for paired high-speed human reference validation. Independent participant and device holdouts are mandatory before a human-facing claim.
