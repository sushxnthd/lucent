# E002-606 | Frozen rational-rate human-label decimation falsifier

Date: 2026-11-02. Parent E002-371; follow-up to E002-605. Existing branch and draft PR #26 only.

## Motivation and prior evidence

E002-605 hosted CI run 41398694048 completed successfully, but its attempted public Mendeley API acquisition returned HTTP 401 Unauthorized; zero real annotation events were parsed. This is an acquisition failure, **not** evidence about human blink rates. The published dataset page is available at https://data.mendeley.com/datasets/9yzdnng594/1; the provider documents token authentication for the dataset API (https://data.mendeley.com/api/docs/). No login bypass or credential scraping is authorized. After a second public published-file-route check, stop source-access archaeology.

E002-605's three-phase 'n mod 3' experiment measures **native 3:1 index decimation** only. It does not implement a true 30-fps camera when the source is 100 or 110 fps. This run prospectively tests how large the resulting discrepancy can be.

## Precommitted model and falsifiers

Construct a hypothetical *piecewise-constant* fully closed pulse occupying m consecutive native-frame bins, duration m/f_H seconds. The low-rate camera takes instantaneous point samples every 1/30 second with unknown phase uniformly distributed over one period. This is a **synthetic ideal timing model**, not a physiological dwell guarantee, optical shutter measurement, or a claim that a native-frame annotation implies binwise closure.

For f_H in {100,110} Hz and m in {1,2,3,4}, compute exact miss probability as a reduced rational number. Separately compute the E002-605 native-index 3:1 phase miss fraction for m bins. Independently enumerate all distinct integer tick phases on a common exact lattice using lcm(f_H,30). Compare. Predict in advance:

- f_H=100, m=3: true 30-fps ideal phase miss = 1/10; 3:1 index miss = 0.
- f_H=110, m=3: true 30-fps ideal phase miss = 2/11; 3:1 index miss = 0.
- f_H=110, m=2: true 30-fps ideal phase miss = 5/11; 3:1 index miss = 1/3.
- f_H=110, m=4: both miss = 0.

If independent enumeration disagrees, mark experiment FAIL and do not publish the predicted values as verified. Reject nonintegral or nonpositive rates/durations, impossible phase grids, and phase-index interpretation as a physical camera certificate.

## Evidence and product boundary

The only permitted conclusion is a **conditional idealized sampling-model counterexample** to interpreting 'n mod 3' as a true 30-fps camera at 100–110 Hz. Even a positive real annotated blink event is not automatically a fully closed interval; sensor integration, rolling shutter, dropped frames, clock jitter, anatomical geometry and human velocity ceilings are not modeled. Lucent remains ABSTAIN_UNCALIBRATED; production release BLOCKED. Preserve the Mendeley 401 negative result and human-study need. No human images or individual labels in GitHub.
