# E002-352 — Pre-registered native-RGB blink phase holdout

Clip 1 EyeBlink8 was not used in the preceding seven-clip E002-347 analysis. Local protocol was frozen and SHA256 hashed before opening clip-1 annotations; GitHub contents writes were blocked twice, so remote preregistration did NOT precede holdout access.

Data: EyeBlink8 clip 1 manual frame annotations, immutable source blob 048ae496568af1c14fb53001917f220829e9039c. 38 blink IDs, 32 with at least one clean bilateral 90-100% closure-positive frame; 1 had one, 7 had two, 24 had three or more. All 32 had consecutive clean-positive frames.

Exact phase-loss rates: 2x: 1/64 = 1.5625%; 3x: 9/96 = 9.375%; 4x: 27/128 = 21.09375%; 5x: 53/160 = 33.125%; 6x: 82/192 = 42.7083%. Preregistered broad empirical predictions (2x <=5%, 3x <=15%) passed. Point predictions 1.71% and 7.03% were not exact, as expected under between-clip heterogeneity.

For k consecutive closure-positive native frames, exactly max(0,m-k) of m decimation phases erase all clean closure evidence. This is a known combinatorial sampling identity. No independent high-speed physiological reference, exposure calibration, participant/device holdout, or publication novelty. Product: preserve abstention and sampling-phase vulnerability, reject blink absence claims from missing frames and all five-second fatigue certification.