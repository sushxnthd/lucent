# E002-134 frozen source/timebase audit (2026-10-12)

Published EyeDentify alignment source converts Tobii times to whole seconds, averages corresponding sample positions across three 1-second groups, assigns a single timestamp to all output rows, then pairs these with webcam frames by row index. Three released human CSVs were observed to have one timestamp across 42-89 frames. This code-to-data connection is evidence, not proof of exact generation provenance.

For synthetic 90Hz tracker (270 samples) and 30fps webcam (90 frames), compare C(x)[j]=mean(x[3j:3j+3]) with F(x)[j]=mean(x[j],x[90+j],x[180+j]). Fixed signals: ramp 1+0.2t; sin(2*pi*t); Gaussian pulses exp(-0.5*((t-c)/0.08)^2) at c=0.35,1.35,2.35s; delayed exponential onset at 0.4s with 0.5s time constant and 0.3 amplitude.

G0 three examined CSVs have 1 timestamp despite >30 frame paths (known before freezing). G1 source contains rowwise three-second averaging and constant timestamp (known before freezing). G2 max difference among F of three pulses <1e-12. G3 min pairwise L2 among C of pulses >0.1. G4 range(F ramp)/range(C ramp)=1/3 within 1e-12. G5 active RGB and state not evaluable. No lag search or retuning. Elementary linear algebra, not a physiological discovery. Earlier RGB/reference results against released labels remain numerical observations but are not proven time-aligned physiology.
