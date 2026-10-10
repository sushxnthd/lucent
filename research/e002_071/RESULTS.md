# E002-071 — Rasterized ratio audit

Frozen protocol SHA-256: `b3d2761d51fa77fd9fa25825e97822322ad7c73301ff5b8d4a5715bb976b8676`.

A conditional two-timepoint interval for a ratio p/i with independently bounded radius error b is [(p-b)/(i+b), (p+b)/(i-b)]. For p=r, i=2r, later p=1.05r, the intervals certify an increase exactly when r>60.5b. If the iris denominator is exact and stable, the threshold is r>40b.

A frozen synthetic audit rasterized perfect concentric circles at pupil radii 2, 3, 4, 6, 10 and 20 pixels and 64 common subpixel offsets. The false range of sqrt(pupil_mask_area/iris_mask_area), relative to a stipulated 0.025 response, was 2.91, 2.19, 0.96, 0.70, 0.18, and 0.12 respectively.

An independent scalar-loop implementation reproduced all 384 NumPy pixel-count cases without disagreement. Eight unit tests passed. Numerical threshold-equality and mask-crop implementation errors were corrected before final results.

These are mathematical and synthetic results only. No image model accuracy or external participant inference is claimed. Earlier negative controls are preserved. Next: annotated visible-light segmentation and a separately frozen paired-reference waveform benchmark.
