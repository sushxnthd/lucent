# E002-531 Amendment A | Pre-experiment arithmetic correction

2026-10-29, after frozen protocol commit `9394752a7837771d63b49d00799ffb410e7a2d7c` and **before writing or running the executable**.

The frozen protocol's predicted 9.375-ms piecewise-linear below-threshold dwell was an arithmetic error. The 1/4 threshold is crossed between indices 32 (2/5) and 33 (1/5), at index **32.75**, and again between 35 (1/5) and 36 (2/5), at index **35.25** (not 36.5). The continuous duration with aperture <=1/4 is therefore `(35.25-32.75)/400 = 1/160 s = 6.25 ms`. Three native sampled values (indices 33,34,35) are at/below threshold. All other predictions, data values, masks and test criteria remain frozen. The original text is preserved for auditability.
