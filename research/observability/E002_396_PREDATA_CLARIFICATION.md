# E002-396 pre-data clarification: event-level inversion

This clarification was committed **before S19 acquisition** and does not alter the original frozen source, selection, threshold or predictions.

For each seven-frame event/control window, first compute E002-395's **original** window score `s = max_frame(1 - dark_fraction_frame)`. The inverted hypothesis H1 is the **event-level sign inversion** `s_inverse = 1 - s = min_frame(dark_fraction_frame)`. This is the exact monotone reversal of E002-395's held-out ranking (S01 AUC 0.2004 -> inverted AUC 0.7996), and is **not** a new within-window max of raw dark fraction. Thus the S19 test is a direct, unretuned out-of-person falsification of the sign-reversal hypothesis.

Do not change this rule after S19 scores are examined. It remains an EEG marker association test, not an aperture measurement.
