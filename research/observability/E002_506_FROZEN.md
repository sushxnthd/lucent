# E002-506 | Frozen independent-pulse instrument falsification

Frozen 2026-10-28 before executing the E002-506 calculator or tests. Primary E002-371 branch, existing draft PR #26. This is a **synthetic optical-instrument validation substitute**, not human data, a new physiological theorem, or camera certification. E002-501 optical proxy remains retired. No S01 thresholds, candidate centers or annotations are changed.

## Question and exact acquisition model

Can independently timed optical pulse edges constrain the **actual frame period** tightly enough for E002-505's conditional 30-fps hidden-closure exclusion, and can they substitute for shutter-exposure calibration? A pulse event with externally authenticated time bracket [l_i,u_i] is independently shown to occur within the exposure of native frame n_i. Under a *global-shutter, stable affine clock* with frame starts b+n_i T and independently measured exposure w, each observation implies

    l_i - w_max <= b+n_i*T <= u_i.

For each i<j, with d=n_j-n_i>0, the exact feasible period interval must obey

    (l_j-w_max-u_i)/d <= T <= (u_j-l_i+w_max)/d.

Intersect all pairwise constraints and T>0. This is the projection of the common-offset feasibility constraints for this idealized model. No claim is made if pulse-to-frame attribution, frame numbering, global shutter, affine clock, exposure bounds, event timing or uncertainty are unauthenticated. For the **largest blind gap**, use T_upper - w_min, not nominal FPS. If w_min is absent, the physical claim must abstain; never silently assume 10 ms.

## Frozen adversarial synthetic cases

- External pulse edges bracketed +/-0.1 ms, assigned to frames 0 and 300, nominal spacing 10 seconds, shutter w_min=w_max=10 ms: period uncertainty should be narrow enough that E002-505's hypothetical V=60/s, b_mean=.999, r=.001, theta=.2 remains conditionally excluded.
- Same precision but pulses at frames 0 and 3, nominal spacing 0.1 seconds: period upper bound should make the same conditional exclusion fail.
- With a 300-frame pulse span but shutter w_min=0 (w_max=10 ms), no conditional exclusion; a measured clock period alone does not measure exposure.
- Add a third inconsistent pulse to force empty feasible period interval and abstention.
- Reorder/duplicate frames, invalid brackets, negative exposure, missing provenance or an unverified pulse-to-exposure attribution: reject.
- The code may compute conditional research numbers but must never set camera authentication, certified eyelid speed, human anatomy, physical closure exclusion or product release true.

## Physical experiment handoff

A future no-cost instrument study must independently time an optical emitter (separate authenticated timebase) and measure its transitions against a photodiode or independent timing reference; establish which exact exposure contains each edge, using calibrated response and known row position. Capture widely separated events (e.g., 3 and 300 frame spacings), verify no dropped/reordered frames and clock drift, and measure shutter start/end and rolling-shutter row timing separately. Repeat at multiple brightness, blur, gaze, glasses, and motion conditions, rejecting ambiguous transitions. Preserve raw local captures privately and publish only anonymized aggregate calibration intervals. A smartphone UI animation, video container FPS, or uncalibrated screen refresh is **not** an independent clock.

Stop after this synthetic instrument test. Actual independent S01 anatomical reviews and physical acquisition calibration remain the decisive bottleneck. Product ABSTAIN_UNCALIBRATED; release BLOCKED.
