# E002-122 frozen protocol — independent-image mask-error budget (2026-10-12)

**Type:** DISCRIMINATION / CAPABILITY-BUILDING. **Scope:** original-human static oracle annotation masks from public Zenodo record 20492528; no live RGB segmentation, tracker waveform, or behavioral-state measurement.

**Hypothesis:** E002-121's fractional occupancy advantage survives image-disjoint replication under oracle masks but is sensitive to small anatomical mask-boundary errors. This distinguishes subpixel quantization from segmentation uncertainty.

**Sample:** verify original archive MD5/ZIP CRC. Sort all matched JPEG/PNG pairs by SHA256(JPEG path), skip the first 480 used by E002-121, evaluate the next 480 *eligible* pairs. Report all exclusions, source prefixes and whether image disjointness is achieved; no person-wise independence is asserted. Mask convention red>=128 pupil, red OR green>=128 eye is **provisional** pending manual audit.

**Observable:** q=sqrt(pupil pixels / visible eye-region pixels), reference computed from full-resolution unperturbed masks. ROI, shifts, hard >=0.5 and BOX fractional downsampling follow E002-121 exactly at 32x16, 64x32, 128x64. Use unperturbed reference ROI for every perturbation, a favorable upper-bound assumption.

**Perturbations:** unmodified oracle; pupil-mask erosion and dilation by 1 original-image pixel (3x3 structuring element); erosion and dilation by 3 original-image pixels (7x7). Keep eye region fixed and constrain dilated pupil to eye region. Report invalid/empty masks, both direction-specific and pooled median absolute error. All transformations operate on labels, NOT on actual RGB segmenter predictions.

**Primary outcomes:** median absolute q error across four crop shifts, fraction of images where fractional beats hard under same mask condition; compare perturbed fractional error to unperturbed oracle hard error. Separately report 128x64 and 32x16. Report at least one uncertainty interval via bootstrap over images; no participant-level CI claim.

**Frozen gates:** G0 >=300 held-out eligible images with zero path overlap with E002-121 first 480; G1 oracle soft median error < oracle hard median error at all three resolutions; G2 128x64 pooled 1-px perturbation fractional median error > unperturbed oracle fractional median error (a segmentation-sensitivity test); G3 explicitly NOT EVALUABLE for operational RGB waveform or 5-second state. Gate outcomes must not be retuned.

**Anomaly mining:** quantify source-prefix differences, 128x64 soft-vs-hard exceptions, mask colors, whether pupil boundary direction reverses effects, and mask area dependence. Keep E002-112/114, E002-121 and RGB-SCALE-OBSERVABILITY-001 intact.

**Claim boundary:** fractional occupancy is prior art; this is an annotation-space quantization/error-budget study, not a demonstrated segmentation model, tracker transfer, or physiological advance. Strongest next experiment remains source/participant-disjoint *actual RGB-derived* pupil masks paired with eye tracker reference.
