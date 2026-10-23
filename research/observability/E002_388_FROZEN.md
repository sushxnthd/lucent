# E002-388 frozen prospective instrument protocol — 2026-10-23

**Kernel:** E002-371. **Status:** pre-analysis freeze; no E002-388 results inspected at freeze time.

## Why this experiment
Previous E002-387 showed that 240-fps reference *exposure averaging* can erase sub-millisecond threshold crossings. Published high-speed human blink studies instead report voluntary closed phases on the order of tens of milliseconds (Kwon et al., 2013, 600 fps, mean closed phase 58±4 ms). The present test checks whether a fully specified *video-encoding pipeline*, rather than aperture arrays, preserves the distinction between sustained closure and short threshold excursions. It is a controlled software instrument, **not a physical camera or human validation**.

## Frozen acquisition and endpoints
Render a calibrated 96×64 synthetic eye patch at 30 fps with 10-ms global-shutter exposure, integrating 10 evenly spaced aperture samples per exposure. Two classes: sustained complete closure (50-ms plateau with 15-ms linear entry and exit), and short 8-ms complete closure (no plateau), plus open-eye negatives. Shift onset through 20 equally spaced phases over one 30-fps period. Encode each resulting 60-frame video with FFmpeg libx264 at CRF 18 and CRF 40; decode from the encoded MP4 (never use original uncompressed frames for scoring). Estimate aperture from fixed-ROI mean intensity with a two-point *static* calibration from separate encoded open/closed phantoms. Threshold at aperture <=0.2. Run a second acquisition with adverse brightness gain, synthetic glasses reflection and geometric eye displacement.

## Frozen hypotheses
P1: With the clean 50-ms closed plateau, at least one full exposure must fall inside the plateau for every onset phase because 50ms > frame period + exposure (43.33ms). Hence source-aperture ground truth has a fully closed frame for every phase.
P2: An 8-ms event cannot guarantee any full 10-ms exposure and will have phase-dependent visibility; its ground-truth overlap must be <100% under a requirement of >=4ms overlap.
P3: A static clean optical transfer calibration is not a deterministic aperture bound under combined photometric, reflection and geometric shifts. At least one adverse video will have |estimated minus exposure-average aperture| > the clean-video maximum error.
P4: A fail-closed product gate will abstain on *every* video with unqualified nuisance metadata, regardless of measured eye openness.

## Reporting and falsification
Report phase-wise source overlap, encoded-video detection, continuous-aperture reconstruction error, false detections in negatives, and clean vs adverse error envelopes. Distinguish exposure erasure, image inference failure and codec corruption. If P1 source prediction fails, fix the synthetic instrument, not the prediction; if P2/P3 fail, retain as negative results. Never call this human validation. Independently verify temporal-overlap calculations by a separate analytic implementation and include an actual MP4 example, metadata, executable code, results and human protocol. No hard no-hidden-closure claims based on codec images.

## Literature grounding
Kwon et al., *High-speed camera characterization of voluntary eye blinking kinematics*, J R Soc Interface 2013, https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/ ; *Analysis of Spontaneous Eyelid Blink Dynamics Using a 240 Frames per Second Smartphone Camera*, 2019, PMID 30893187. Neither provides raw paired ordinary/high-speed footage used in this experiment.
