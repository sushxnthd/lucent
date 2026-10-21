# E002-340 prospective human protocol

Signal: exposure-timestamped normalized RGB log pupil/iris ratio. Reference: independently time-locked >=120Hz pupil diameter, display photodiode, camera exposure/gain/white-balance. Estimand: signed stimulus-locked pupil response, not fatigue.

Calibrate physiological template s, nuisance span N and joint L2 error bound epsilon only on training participants/devices. Freeze masks and code before final holdout. Hold out participant, camera model, lighting and glasses regimes. Use geometry-only, brightness-only, missingness-only and smoothness-only controls. Include no-stimulus and shuffled-probe baselines.

Before final holdout predict a boundary crossing from epsilon_crit=|beta| ||P_N s||/2. Certificate only if sharp feasible amplitude interval excludes zero; otherwise abstain.

Proposed publication gate (NOT achieved): independently synchronized paired data; >=95% coverage for nominal 95% intervals in each preregistered stratum; >=99% sign accuracy among certificates with confidence intervals; predicted crossing confirmed; controls beaten; independent reproduction.

Previous Eye-of-the-Typer access path exhausted. No more than two substantive access attempts per new dataset route.