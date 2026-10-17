# SCIENCE
Original-human E002-221 source workflow 38819094753 passed source CRC/SHA and reference analysis on 2026-10-15. Independent E002-254 replay of its original Actions artifact found:
P_33: 150 video packets, 145 distinct PTS; 200 valid left and 199 valid right Tobii samples in the nominal 5s reference window.
P_54: 149 packets, 83 distinct PTS; 199 valid left and 195 valid right Tobii samples.
For BOTH eyes of BOTH participants, 100% nearest-valid reference coverage at all five shifts -1,-0.5,0,0.5,+1s using the prior 75ms gate. The tested offsets span 2s; p95 nearest-valid distances <=11.881ms in all 20 cases. Coverage cannot certify correct clock offset.
The earlier nearest-ANY-sample approach reported ~27.5-30.9% valid coverage because many raw tracker samples were invalid. Valid-only selection corrected availability, not synchronization.
PTS collisions mean packet metadata lacks a unique timestamp label for every packet; they do not prove simultaneous exposures.
No exposure clock, physiological waveform correlation or fatigue state is certified.

# PRODUCT
Retire reference-density/nearest-valid matching as a synchronization certificate. Use only as a reference availability check. Require an independent shared exposure-time anchor or validated clock-error bound before rapid ocular waveform claims. If EOTT cannot provide one, switch to independently synchronized data; retain EOTT for detector development and timing stress tests. Keep E002-234 retired and do not pursue APST-5.

# LIMITATIONS
Two development participants, post-hoc audit of five discrete offsets, not all continuous offsets; no new pixel replay, no reference waveform agreement, no device/lighting/glasses holdouts. No field-level breakthrough.