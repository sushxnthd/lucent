# Lucent E002-059: preregistered cross-platform replication specification
Date: 2026-10-09
Type: DISCRIMINATION / CAPABILITY-BUILDING
Frozen parent: E002-057, protocol SHA256 0d3a23f7294738c72dc7e5803d2370ab86e9f10ff7e4dad2a502631773683f6b.
Source: oocular/ready commit dc0b020eb1ca1ab8966c4c085b9daba3310e1efd.
Sample: development participant 1 (5 images), test participant 2 (15 images).
Ground-truth masks are used ONLY to define an oracle pupil+iris region; none of these estimators is deployable.
Reference outputs (E002-057 Wolfram): median test AUC 0.7260085369; oracle threshold IoU 0.3648286560; threshold-20 IoU 0.2132974635; rank-area IoU 0.3233957752.
Frozen gates: G1 median AUC>=0.80; G2 median oracle IoU>=0.60; G3 median threshold-20 IoU>=0.50; G4 median threshold-20 IoU>=median rank-area IoU. All failed previously.
New test: independently decode the same 20 original JPEG/PNG pairs with Pillow and recompute pixel counts, AUC, threshold and rank-mask IoU. Report discrepancies as discrepancies, do not tune to match.
Difference attribution: JPEG decoder, grayscale conversion, tie ordering, resizing, mask decoding; record SHA256 of each downloaded input.
No threshold, mask, sample, or frozen gate may be changed based on this run. A negative outcome is not a kill: investigate systematic discrepancies and any invariant quantities.
This test does NOT assess real-time pupil waveforms, synchronized tracker reference, 5-second alertness, or participant generalization.
Do not redistribute facial image pixels or masks.
