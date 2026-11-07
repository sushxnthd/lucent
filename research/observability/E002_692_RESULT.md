# E002-692 — Velocity-bound misspecification adversary

Evidence tier: **exact-rational synthetic falsification only**, not physical or human validation.

## Frozen test
Use two aperture endpoints a,b, blind gap h, closure threshold c, stipulated velocity ceiling v. The nominal certificate excludes closure when |a-b| <= vh and (a+b-vh)/2 > c. Generate an attainable V-shaped trajectory using actual velocity kv, with k in {1,5/4,3/2,2}. A closure is possible when (a+b-kvh)/2 <= c. Compare the nominal certificate with a robust certificate using 2v. Exhaustively enumerate a,b in {2/4,...,8/4}, h in {1/2,1,3/2}, v in {1/2,1,2}, c in {0/8,...,8/8}, k in the specified set. Discard endpoints infeasible at actual speed.

## Locally executed result (Python standard library)
13,428 feasible configurations; 6,476 nominal exclusion certificates, of which **1,414 are false** against attainable trajectories at actual speed; 3,840 robust certificates using the independently stipulated factor-two envelope, with **zero false exclusions** on this grid. These counts are not physiological error rates and the robust result follows from the assumed envelope. Example: a=b=1/2, h=1/2, v=1/2, c=1/4, k=2; nominal lower envelope=3/8 > c but actual attainable minimum=1/4.

## Product consequence
The conditional exclusion certificate is **not robust to underestimating the physical velocity ceiling**. No measured camera-derived upper bound should be treated as a deterministic human maximum. Without an independently defensible hard upper envelope for eyelid speed, or a separately justified acceleration bound and calibrated endpoints/timing, return ABSTAIN_UNCALIBRATED. The factor-two safety margin in this experiment is an adversarial scenario, **not** a validated universal physiological factor. Keep production BLOCKED.

## Limits and decisive next experiment
This is a scalar ideal-aperture surrogate; it excludes exposure integration, rolling shutter, geometry, brightness, blur, gaze, glasses, missingness and clock uncertainty. These must be evaluated in synchronized physical acquisition and participant-disjoint human reference tests under E002-690. Run the committed script independently and compare printed counts before treating GitHub artifact as replay-verified. No new human or physical data acquired.
