# E002-345: published-reference-label observability gate (2026-10-21)

STATUS: source-code-conditioned impossibility, NOT a new physiological theorem or human validation.

## Source-grounded measurement operator

EyeDentify's public preprocessing source converts Tobii timestamps to whole-second strings, selects the first three unique seconds, horizontally concatenates corresponding within-second rows, computes a row-wise mean, then joins those derived rows by index to webcam video frames. This is also described on the authors' project page. Sources:
- https://github.com/vijulshah/eyedentify/blob/main/data_creation/eyedentify/tobii_and_webcam_data_alignment.py
- https://vijulshah.github.io/eyedentify/
- https://arxiv.org/abs/2407.11204

Ideal balanced case: 270 raw Tobii diameter samples x at 90 Hz over 3 seconds, and 90 processed labels y:

    y_i = (x_i + x_(i+90) + x_(i+180))/3, i=0..89.

The 90x270 operator A satisfies A A^T = I/3, rank(A)=90, dim(ker A)=180. For any vector v of length 90, (v,-v,0) is invisible. The 1-second-spaced three-way transfer is H(f)=(1+exp(2 pi i f)+exp(4 pi i f))/3, with exact zeros f in Z+1/3 and Z+2/3 Hz. These exact nulls assume three equally populated 1-second bins; uneven bins and NaN averaging alter the transfer.

The within-second label row i corresponds nominally to raw reference time i/90 seconds, but is joined to video frame i at approximately i/30 seconds. This is a temporal index mismatch. No precise latency or rapid waveform validation can be inferred from such processed labels without returning to original raw Tobii data and independently synchronized webcam times.

A collision pair with physical pupil diameter 4 mm baseline and opposing 0.04-mm smooth deviations in first and second seconds gives identical derived labels, while the underlying diameter trajectories differ. This is a processed-LABEL impossibility, not an image-level impossibility.

## Mandatory ten-part kernel
1. Signal/reference: ordinary 30-fps RGB eye video vs raw 90-Hz Tobii pupil diameter; test information loss in published *processed* reference labels.
2. Frontier: EyeDentify (Shah et al., WACV 2025) explicitly documents the three-way averaging. EOTT (ETRA 2018) contains RGB and unaggregated 120-Hz Tobii pupil measurements but remains unvalidated for Lucent.
3. Metric: exact rank/nullity, transfer zeros, indistinguishable reference histories, later human holdout coverage.
4. Strongest nuisance: nonlocal reference-label averaging and whole-second timestamp rounding, not only RGB lighting.
5. Model: F_j=C[r(t_j), eyelid, gaze, illumination, optics, scale]+noise; x_k=r(k/90)+e_k; y_i=(x_i+x_(i+90)+x_(i+180))/3 in balanced case.
6. Falsification: demonstrate released dataset did not use this code path, or show raw timestamps permit correct re-alignment; inspect actual source and processed pairs before applying conclusions to released labels.
7. Boundary: nullity 180/270 and exact H(f) nulls in ideal case; no recovery from processed labels on nullspace.
8. Human test: prior to outcome access, split participant IDs by SHA256('lucent-345:'+ID) mod 5; hold out residue 0; use geometry-only, brightness-only, missingness-only and temporal-smoothness controls; no learned model before physical baselines.
9. Publication threshold: raw paired human verification, prospective predicted boundary crossing on untouched participants/device/lighting, independent checker, and novel contribution beyond elementary linear algebra.
10. Product consequence: REJECT rapid pupil timing/lag/velocity certification using these processed labels; ALLOW static/aggregate pupil regression as research with provenance; REDESIGN data collection to retain raw per-sample timestamps; ABSTAIN on uncalibrated temporal claims.

## Numerical independent checks (synthetic operator only)
1500 randomized nullspace and implementation comparisons PASS. Matrix Gram error 0; nullity 180; maximum difference between collision labels 4.44e-16 mm; maximum physical trace difference 0.039966 mm; transfer-zero residual 5.46e-16.

## Failed gates / limitations
No released EyeDentify human data read. No native Tobii/video pairing validated. No subject/device/glasses holdout or prospective human boundary test. The averaging was already described by the dataset authors, and rank/nullspace facts are standard. Do not claim new mathematical priority or a human ocular breakthrough.

## Next scientific action
Do not spend further runs on metadata. Obtain independently timestamped RGB+raw pupil reference (EOTT or a bounded alternative) and test the frozen geometry/brightness/missingness/smoothness controls. If access blocked twice, pivot to a different path while keeping hourly persistence.
