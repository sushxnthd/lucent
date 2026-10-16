# E002-240 holdout metric addendum — frozen before any run

Random seed 240617. Generate 120 paired synthetic image cases (60 nuisance-only, 60 true-change), 192x192 uint8, supersampling x4, iris radius cyclic [10,14,20,28] px, random annulus outer radius U[0.58,0.80], width U[0.08,0.15], Gaussian blur U[0.45,1.0] px, Gaussian noise sigma 0.8, angular iris texture amplitude U[0,3] gray. Both images in each pair share nuisance parameters and sensor-noise realization.

Nuisance-only: true pupil ratio fixed at 0.40; annulus gray 22 vs 42. True-change: true pupil ratio 0.35 vs 0.48; annulus gray fixed at 32. Order of painting: sclera, iris, iris texture annulus, pupil (so annulus cannot erase true pupil). No holdout tuning.

Test frozen GitHub E002-234 edge.py, SHA256 569e750d17ea7dab30ad8d4582137eaef06db4fa648006d6e3b0703f9dfe2220. Compare gate alone to gate plus frozen E002-237 dual-peak rule (second separated radial peak >=0.8 of first at separation >=0.14 normalized iris radii). Primary secondary metrics: both-frame admission; admitted pair with either absolute radius error >0.08 (bad admission); nuisance-only admitted apparent change >0.15; true-change admitted detected difference >0.06 with correct sign. Record all 240 raw image hashes, predictions, and exclusions. No tuning on holdout. Publish both denominators: all pairs and admitted pairs.

Independent checker must recompute summary from raw per-image and per-pair data without using radial detector. Any success is only synthetic evidence, not physiological waveform certification.
