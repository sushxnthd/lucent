# E002-275: clock observability and device eligibility

SCIENCE: Under separately verified absolute clock error J and lag-estimator error E, true lag is in [observed lag-(J+E), observed lag+(J+E)]. A 67 ms threshold passes only when |observed lag|+J+E<=67 ms. Unknown bounds require abstention. This is elementary conditional arithmetic, not a new physiological theorem.

PRODUCT: EVE Basler is the sole author-documented reliable eye-tracker synchronization path. Three Logitech C922 webcams use potentially imprecise system timestamps and represent one consumer device model, not three independent device models. Split validation into Basler positive control followed by distinct consumer-device transfer.

ACTIVE KERNEL: RGB full-conic pupil/iris ratio versus same-eye Tobii diameter. Scalar: worst-case lag and ultimately held-out Pearson lower confidence bound, jointly with frozen lag, amplitude and NRMSE gates. Confounds: corneal magnification, gaze geometry, illumination, clock error. Falsification: human waveform fails untouched gates or nuisance-only controls match it. Publishable: eight untouched participants, verified clocks, independent checker and participant/device/lighting/glasses holdouts. Product: 75% accurate admitted windows at 50% RGB-only coverage. Kill: three nondiscriminating runs or failed human transfer.

DATA: No human recordings obtained. 2400 deterministic arithmetic trials passed locally. No measured numeric clock bound or lag-estimator bound. No remote CI verified. Source: swook/EVE commit 82757eb2ffb4dd198db36dbfea71601098b597f0, DATASET.md blob 9b04b892e248c2030168c627357e4cb66c87104a, eve_sequences.py blob 8b03f60068cc40f2d2ffacac46a1638a31e2117d. Source SHAs are connector-reported, not independently rehashed.

Wildcard: the three webcam views share the Logitech C922 device model. No fatigue inference authorized.
