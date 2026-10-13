# E002-161 — FROZEN ORIGINAL JPEG CHANNEL PROVENANCE (2026-10-13)

## Active measurement kernel
Question: Does an ordinary-RGB, geometry/photometry-normalized pupil/full-iris five-second waveform match a concurrent independently timestamped tracker pupil-diameter waveform under participant, device, lighting, and glasses holdout?
Signal/reference: video-derived dimensionless pupil/full-iris temporal ratio versus synchronized tracker pupil diameter (relative change, not absolute millimetres).
Current frontier: E002-158 obtained original-human annotated JPEG pupil/ring rank AUCs; 477/480 images had exactly identical channel AUCs. These are not tracker waveforms. Previous visible-eye reference drift and cross-denominator disagreement remain negative results.
Primary observability scalar: frozen held-out correlation, lag, amplitude fidelity, NRMSE and accepted coverage, with geometry and photometry nuisance controls.
Strongest confound: time-varying illumination, eyelid/crop geometry, camera image processing, and segmentation drift.
Decisive falsification: prospectively held-out waveform gates fail relative to a verified tracker, or nuisance-only controls perform equally well.
Publishable success: independent checker, untouched participant/device holdouts, calibrated rejection, mechanism-derived unseen-condition prediction, and literature collision audit.
Product relevance: a reliably calibrated five-second measurement with useful coverage and truthful abstention. Kill/pivot after repeated valid paired human held-out failures under feasible capture conditions.

## One-time provenance auxiliary (no physiology claim)
Question: Are the original 480 JPEGs from E002-158 genuinely chromatic RGB images, or merely 3-channel representations of effectively monochromatic images?
Source: Zenodo record 20492528, archive SHA256 049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700. Reproduce exact E002-158 hash-sorted matched JPEG/PNG pairs [960:1440], retain eligible images using original E002-158 scoring (up to 480). Do not redistribute source images.
Before opening pixels, freeze metrics: per JPEG Pillow native mode; exact RGB channel equality fraction; fraction pixels with max(R,G,B)-min(R,G,B)<=2 in 8-bit values; mean channel spread in 8-bit units; median/p95 spread; JPEG file SHA256. For provenance, do not use an RGB conversion to infer the original encoded mode. Count by exact filename group, with no claim that groups are participant identities.
G0: verified archive SHA256 and >=300 valid paired JPEG/masks.
G1: classify cohort effectively achromatic if >=95% of eligible images have >=99% pixels within 2 digital levels of equal R/G/B. This is an operational threshold, not proof of native monochrome acquisition.
G2: classify demonstrably chromatic if >=5% of eligible images have >=5% pixels whose channel spread exceeds 2 levels. If neither G1 nor G2, report heterogeneous/inconclusive.
G3: independently recompute image pixel spread and SHA256 for 20 hash-determined images; zero tolerance on integer counts.
G4: physiological RGB/tracker waveform UNTESTED regardless of source outcome.
Wildcard (10%): subgroup asymmetry in chromatic spread versus E002-158 rank AUC discrepancies. Explicitly exploratory.

## Science / product decisions
SCIENCE: if near-achromatic, previous equal channel AUCs are likely modality-provenance artifacts, not evidence of robust multichannel RGB physiology. If chromatic, equal AUCs reflect order-statistic invariance and cannot establish independent chromatic robustness. In either case no physiological claim.
PRODUCT: forbid using this cohort to validate chromatic/white-balance corrections if effectively achromatic; otherwise use it only as static oracle-local contrast test. Advance to genuinely synchronized RGB/tracker data. No repeated dataset access if this attempt fails; switch source after two blocked attempts.
No retuning after inspecting results. CI/data failures are infrastructure failures, not scientific falsifications.
