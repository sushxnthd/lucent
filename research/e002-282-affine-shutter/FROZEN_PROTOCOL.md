# E002-282 frozen protocol (before synthetic outcomes)
Six predeclared instrument configurations:
C1 30fps T=1/60 Dmin=.20 delta=.70 eta=.01 m=.6 M=1.4
C2 30fps T=1/60 Dmin=.20 delta=.70 eta=.01 m=M=1
C3 60fps T=1/120 Dmin=.20 delta=.70 eta=.01 m=.6 M=1.4
C4 10fps T=1/60 Dmin=.20 delta=.70 eta=.01 m=.6 M=1.4
C5 30fps T=1/60 Dmin=.06 delta=.5 eta=.015 m=.6 M=1.4 (no-go)
C6 unseen synthetic 24fps T=.010 Dmin=.13 delta=.65 eta=.008 m=.75 M=1.25
For finite cases, compare 0.98*dcrit and 1.02*dcrit at 4096 equally spaced event phases. Require at least one ambiguous below and none above. Independent 8192-phase checker and exact midpoint witness. No human data accessed.
Future human test: >=8 untouched participants, >=2 consumer RGB camera models, independently synchronized high-speed eyelid aperture, independent Dmin/eta/m/M and exposure/readout calibration, held-out lighting/gaze/glasses, preregistered unseen boundary crossing, geometry-only/brightness-only/missingness-only/smoothness controls, reference-blind admission. Frozen sensitivity >=90%, FPR <=5%, admitted coverage >=50%, missing/rejected in denominator. No fatigue claim.
