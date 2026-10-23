# E002-381 human validation protocol (not yet executed)

Recruit consenting adults under ethics/data-protection review. Concurrently capture native ordinary-RGB 30/60fps (known exposure, row time and clock) and a synchronized >=480fps eye reference, preferably >=1000fps for very brief events. Verify timebase with an LED/photodiode pulse. Independently annotate per-row eyelid front onsets, durations, aperture, and whole-eye closure. Never treat a 10Hz loader as 30fps evidence.

Use separate training calibration to bound row delays, velocity/acceleration, photometric contrast, error, blur, gaze, glasses, missingness and clock drift. Freeze predictions before untouched participants/devices/lighting are evaluated. No test-reference leakage into certificate inputs. Compare exact phase coverage, visible row occlusion and simultaneous whole-eye closure as distinct labels.

Strong controls: geometry-only, brightness-only, missingness-only, blur-only, gaze-only, glasses/glare-only, clock-error-only, temporal-smoothness and RGB-landmark baselines. Report calibration failure and abstention. Any certified but missed event under validated bounds falsifies the conditional model. Report participant-clustered and device-stratified confidence intervals, not frame-level pseudo-replication. An illustrative 300 independent zero-failure events give about a 1% one-sided 95% upper failure bound; correlated human blinks require cluster-aware uncertainty.

Human data acquisition remains unfulfilled. Two previous targeted dataset attempts were exhausted; do not repeat dataset archaeology. Public 1000Hz eye-tracker tabular records without simultaneous RGB cannot validate this RGB boundary.
