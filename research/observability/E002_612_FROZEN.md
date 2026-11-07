# E002-612 | Frozen finite-rate velocity-envelope identifiability experiment

Date: 2026-11-02. Parent: E002-371, E002-611. Canonical branch `research/observability-human-boundary`, draft PR #26. Evidence tier: EXACT CONDITIONAL INSTRUMENT DESIGN + SYNTHETIC FALSIFICATION, NOT HUMAN VELOCITY CERTIFICATION.

## Primary question
Can densely sampled eyelid-aperture observations alone justify a continuous-time upper eyelid-speed ceiling for E002-371? No: without a separate regularity constraint, a smooth arbitrarily fast excursion can be inserted between any two samples. Test a constructive positive substitute: under an **independently defended** bound `|a''(t)| <= M` (physical mm/s^2), point-aperture observations `z_i` (mm), independent per-sample absolute errors `epsilon_i` (mm), and positive timestamp interval bounds `dt_lo_i <= t_(i+1)-t_i <= dt_hi_i` (seconds), evaluate the conservative per-interval speed envelope

    U_i = (abs(z_(i+1)-z_i)+epsilon_i+epsilon_(i+1))/dt_lo_i + M*dt_hi_i/2.

For any true differentiable aperture with Lipschitz velocity `M`, `sup_[t_i,t_(i+1)] |a'(t)| <= U_i`. This bounds only the observed temporal span, not unobserved periods, different subjects, or future sessions. Finite exposure averages are **not point observations** and must not enter without a separately justified reduction. A user-provided M or error bound is not independent evidence.

## Frozen synthetic test grid and falsifiers
- Stationary nominal positions `z_i=0`, uniform `epsilon=0.1 mm`, illustrative `M=5000 mm/s^2`, nominal exact frame rates `f={30,120,240,1000}` Hz. Predict U=2*epsilon*f+M/(2*f). Also test epsilon={0.05,0.5} mm. No value of M here is a human physiological fact.
- For 0.1 mm, M=5000: expected U(30)=89.333333..., U(120)=44.833333..., U(240)=58.416666..., U(1000)=202.5 mm/s. A higher frame rate can yield a **worse** deterministic bound because independent per-frame error divided by a shorter interval dominates.
- Strict exact-rational checks: interval and noise monotonicity; no finite bound without M; zero/negative dt rejected; non-finite input rejected; omitted sample/uncertain exposure rejected; no inference across missing intervals; absolute speed bound, not a direction label.
- Independent Node.js rational check for the 4 key rates and the equality/saturation construction. Tests must not import the Python implementation.
- Sharpness check for a single interval with error-free point observations: `a(t)=s*t + (M/2)*t*(t-dt)`, with observed secant s and derivative at t=0 equal to `s-M*dt/2`. This attains the absolute endpoint bound when sign chosen appropriately. This is a mathematical synthetic construction, not a physiological blink.
- The deterministic design optimum for stationary nominal positions occurs at `f*=sqrt(M/(4*epsilon))` Hz, only under these noise/acceleration assumptions. Do not optimize a product frame rate from synthetic values.
- The instrument must return `ABSTAIN_UNCALIBRATED` unless independently authenticated point observations, per-sample error, timing bounds, full span coverage, and an externally defended acceleration cap exist. Even if supplied, output only `CONDITIONAL_OBSERVED_SPAN_VELOCITY_BOUND`, never a universal human hard ceiling.
- Report exact scenario grid, negative controls, and a concrete paired-camera human protocol requiring 240+ Hz reference, 30 Hz ordinary, optical synchronization, blinded raters, explicit shutter/geometry/brightness/blur/gaze/glasses/missingness nuisance stratification, and participant-disjoint predictions. Consent/ethics approval and data custody are prerequisites.

## Stop rule
Do not perform further dataset access archaeology or theorem-only polishing after this experiment. Next eligible primary experiment must use actual independent physical measurements or independent anatomical ratings; otherwise preserve the blocked state. No Hush branch writes on this run. Production BLOCKED.
