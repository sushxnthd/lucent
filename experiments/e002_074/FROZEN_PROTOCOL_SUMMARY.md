E002-074 FROZEN PROTOCOL (2026-10-10; before new mask pixel inspection)
Full local protocol SHA256: c5fc7166c451fab0d2165fdc4357406a5229a130dbe5052f43d27e334b6c8ba0
Dataset: MEYELens Zenodo 20492528, original ZIP PNG/JPEG and annotations CSV.
Select first eight lexicographic capture-series prefixes, one SHA256(stem)-minimum mask per series; additionally inspect union of all blink=1 or eye=0 metadata rows separately as targeted anomaly probes.
G1: all eight masks decode and pupil/eye area counts match CSV exactly.
G2: >=90% of eight masks satisfy red pupil-positive subset green eye-positive.
G3: report pupil equivalent radius, intersection, component counts and flagged mask statuses.
Exploratory: phase/scale stress at effective pupil radii 2,3,4,6 pixels with 4x4 fixed phase grid; compare hard threshold with fractional area, 5% synthetic reference only.
Hypotheses: H1 annotation topology holds in >=90% of deterministic sample; H2 low-resolution binary measurement has nonzero translation quantization variation and fractional improves; H3 blink/eye flags not equivalent to empty pupil masks.
Preserve nulls, audit topology failure causes, never infer iris contour, person-wise generalization, waveform, state, or physiological validity.
Full protocol and code will be attached as reproducibility package.