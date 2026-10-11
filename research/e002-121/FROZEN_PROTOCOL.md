# E002-121 frozen protocol (2026-10-12)
Question: Can original public human RGB pupil/eye segmentation masks support a spatial observability audit at low image resolution?
Data: public Zenodo record 20492528. Access and legal conditions checked before analysis. No paid services or user hardware.
Observable: q=sqrt(pupil area / visible eye-region area); red channel >=128 defines pupil, green or red >=128 defines visible eye region. This is NOT anatomical iris normalization.
Inclusion: >=16 pupil pixels, >=64 eye pixels, q in (0,0.9), matched image/mask. Sort eligible pairs by SHA256(path), retain at most 480. No training.
Compare annotated-oracle hard-mask occupancy (threshold >=0.5) and fractional occupancy from BOX downsampling at 32x16, 64x32, 128x64. Eye ROI padded by 25% of maximum eye dimension. Test crop shifts (0,0), (.25,.25), (.5,.5), (.75,.75) output pixels. Outcomes: median and 90th percentile absolute error against full-resolution q; median per-image shift range. Bootstrap 1000 image resamples for median difference intervals.
G0: accessible valid archive and >=100 eligible matched pairs. G1: 32x16 soft median error and shift range both <=50% of hard. G2: soft error lower at both larger resolutions and >70% of images improve at 32x16. G3: live RGB waveform and behavioral-state validity always UNTESTED.
Preserve all exclusions and failures. This tests oracle-mask quantization only. Area ratios and antialiasing are prior art. Do not claim real RGB segmentation, paired tracker agreement, five-second inference, or a novel physiological result.
