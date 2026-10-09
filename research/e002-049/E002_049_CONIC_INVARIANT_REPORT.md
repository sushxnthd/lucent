# E002-049: Conic-pencil RGB pupil/iris normalization — synthetic gate and sham veto

Date: 2026-10-09. Classification: CAPABILITY-BUILDING / DISCRIMINATION. **Synthetic contour data only. No RGB human recordings, tracker-waveform agreement, or five-second fatigue/alertness validation.** Preserves RGB-SCALE-OBSERVABILITY-001 negative and E002-044 frozen human protocol.

## Geometry hypothesis
Under a shared homography of concentric coplanar pupil/iris circles, the generalized eigenvalue ratios of the fitted 3x3 conic matrices are projectively invariant. Estimate pupil/iris radius ratio as sqrt(unique_eigenvalue / geometric_mean(repeated_pair)). The conic pencil and its projective invariants are established prior art: https://link.springer.com/article/10.1186/s41074-018-0050-y. Corneal refraction, gaze angle, noncoplanarity and RGB segmentation are not covered: https://pmc.ncbi.nlm.nih.gov/articles/PMC9046372/.

## Prospective synthetic holdout
Protocol SHA256 before generating results: 4688ef7f87dbe798187e074392912af0c80d427c117d73e69f3901385a182841. Seed 20261031; 200 unseen random shared-projective trials; ratio 0.25–0.50; Gaussian contour noise 0.006; 160 points per contour. Fixed gate: median abs ratio error <0.002, p95 <0.005 and both below major/minor/area ratios.

Estimator | median absolute ratio error | p95
---|---:|---:
Major axis | 0.03119 | 0.09221
Minor axis | 0.02305 | 0.05922
Area-derived | 0.02786 | 0.07565
**Conic pencil** | **0.000451** | **0.001215**

Synthetic gate passed; no human inference. Falsification blocks: decentered pupil n=100 conic median error 0.00615 (p95 0.00925); differential pupil/iris projection n=100 median 0.00410 (p95 0.02565).

## Adversarial photometric counterexample
Ten synthetic 150-frame trials with **constant physiological pupil radius 0.4** and time-varying radial contour-localization bias produced mean false apparent ratio range 0.09893 and mean correlation 0.99988 with the apparent constriction template. An exploratory conic eigenvalue-pair gap <0.03 passed 99.6% of frames. **Boundary-only geometry cannot distinguish true pupil change from observationally identical lighting-dependent segmentation bias.** A separate angular distortion produced large pair gap (~0.343) despite small conic ratio RMSE (~0.00094), so gap-only abstention is unreliable.

## Discovery Protocol V2
KNOWN: mathematical conic identity, 8 local tests, synthetic gate, sham indistinguishability. BELIEVED: conic pencil merits comparison as lightweight geometry baseline on real RGB. CONFLICTING: ideal perspective invariance but no photometric identifiability. FALSIFIED within model: general projective invariance of axis/area ratios, exact conic correction for nonshared projection, gap-only detection of photometric false response. ANOMALOUS: large gap with accurate estimate versus small gap with spurious waveform. UNTESTED: real RGB segmentation, corneal optics, human tracker waveform, cross-device/lighting, active state inference.

Hypothesis: shared projective conics preserve normalized radius. Mechanistic prediction: lower held-out synthetic error than axis/area. Observed: yes, but only under specified idealized model. Residual: illumination and eye optics can violate assumptions. Cheapest discriminator: acquire original timestamp-verified RGB/tracker pair, test waveform lag/amplitude/derivative/coverage and sham controls, participant-wise frozen gates. Keep E002-048 TCP framing and clock-anchor caveats.

Roles: Explorer (conic method), Skeptic (sham), Experimentalist (seeded tests), blinded Analyst (human gates untouched), Anomaly Hunter (pair-gap reversal), Prior-Art Auditor (conic prior art), Replicator (independent matrix identity), Theorist (projective and photometric identifiability).

All computation: cloud-only, zero personal spend. Complete tested code, generated JSON and protocol are in E002-049 reproducibility package, not yet mirrored to this branch.
