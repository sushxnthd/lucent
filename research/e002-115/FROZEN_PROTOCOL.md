# E002-115: Frozen independent original EyeDentify RGB/Tobii replication
Date: 2026-10-11 UTC. CAPABILITY-BUILDING / DISCRIMINATION. No original-data Python scoring before this commit.

Hypothesis: A separate Python implementation of the fixed E002-114 photometric dark-core ratio q=sqrt(P/I) will reproduce the failure of rapid RGB/Tobii waveform fidelity. This is a replication of the *same* three-second recordings, not new independent human data.

Source: EyeDentify, https://www.kaggle.com/datasets/vijuls/PupilDiameterDatasets, CC BY-NC 4.0; never redistribute biometric images.

Frozen subjects: 7,17,34. Sessions: 1,11. Left eye only. CSV rows at 0,3,...,87 (maximum 30 frames). Fixed 32x16 RGB ROI y=4:12,x=7:25; luminance Rec.709, per-frame inverted-CDF 2%/90% quantiles; weighted sigmoid dark-core P and iris proxy I from E002-112; no lag tuning, sign flips, participant fits or threshold changes. This q is NOT an anatomical pupil/iris mask.

Independent replication gates: original-source sample counts [30,30,30,30,29,30]; all six raw, ratio and first-difference Pearson correlations within 0.015 of saved E002-114 values; all six Tobii SDs within 0.003 mm. Report SHA-256 digests for source CSV and image digest chain; fail closed on missing, corrupted or inaccessible data.

Frozen scientific gate (unchanged): at least 4/6 sessions n>=20, tracker SD>=0.015 mm, Pearson(q,Tobii)>=0.30 AND Pearson(diff(q),diff(Tobii))>=0.20, plus median(q-minus-raw correlation)>=0.05. Preserve FAIL; no rescue by retuning. Exploratory shift-10 and time-reversal placebo correlations cannot change gate.

Competing explanations for mismatch: Kaggle source revision, decoding, frame indexing, CSV alignment, quantile definition. Investigate before claiming physiological effects. No five-second state inference, device held-out, active-response validation or novelty claim.

Cheapest discriminator: run independent Python on original files in free GitHub Actions, preserve errors and compare all six numeric outputs to E002-114.
