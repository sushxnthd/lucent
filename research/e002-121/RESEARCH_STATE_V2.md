# E002-121 Discovery Protocol V2 state
Date: 2026-10-12. Scope: original-human static annotated RGB masks, not live RGB waveform inference.

KNOWN: GitHub Actions run 38184483700 downloaded Zenodo 20492528 (137,446,558 bytes), verified MD5 and ZIP CRC, matched 4,895 JPEG/PNG pairs, and scored 480 deterministic samples. At 32x16, median q absolute error was 0.000770 fractional vs 0.014941 hard; median shift range 0.000742 vs 0.037899. At 64x32, error 0.000596 vs 0.005441; at 128x64, 0.000421 vs 0.001765. Frozen spatial gates passed.

BELIEVED: low-resolution hard thresholding introduces avoidable quantization error. Fractional occupancy is prior art and here uses oracle high-resolution masks.

CONFLICTING: these spatial-ceiling successes do not explain the previous failures of practical RGB/Tobii waveform estimators; segmentation, photometry and timing remain unresolved.

FALSIFIED (scoped): the hard 0.5 occupancy threshold is not as stable as fractional occupancy in this particular oracle-mask downsampling test.

ANOMALOUS: 23/480 images at 128x64 do not improve individually with soft occupancy; investigate masks and crop regimes.

UNTESTED: RGB-derived anatomical segmentation, independent tracker waveform fidelity, person-wise/device holdouts, active-response specificity, and five-second fatigue/alertness validity. Mask-channel convention follows dataset documentation, not a separate human visual audit. Image bootstrap is not participant-clustered.

Experiment: CAPABILITY-BUILDING/DISCRIMINATION. Prediction: fractional area occupancy reduces translation error; observed: yes under frozen oracle-mask gates. Competing explanations: resampler, mask topology, ROI geometry and source imbalance. Uncertainty: 480 image sample, not independent people. Cheapest next experiment: independent source-disjoint replication and real RGB segmentation before tracker waveform scoring. Preserve E002-112/114 and PupilSense negative results unchanged.
