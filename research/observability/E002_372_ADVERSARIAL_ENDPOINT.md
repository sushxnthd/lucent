# E002-372 adversarial endpoint-velocity counterexample (exact rational)

The acceleration-limited law requires both endpoint velocities to be zero. The assumption cannot be silently dropped.

Let H=7/300 s (30 fps with 10 ms exposure), V=100/s, A=20000/s^2, threshold theta=1/5, and aperture a(0)=a(H)=1. Construct velocity:
- v=-100 for the first 1/150 s;
- accelerate at +20000/s^2 for 1/100 s, taking velocity from -100 to +100;
- v=+100 for the last 1/150 s.

The total displacement is zero and aperture returns exactly to 1. At the midpoint the aperture is 1/12, strictly below theta=1/5. Thus a closure is possible with speed and acceleration bounded, although the **resting-endpoint** law predicts no closure at A=20000.

The exact descent is V*(1/150)+V^2/(2*A)=2/3+1/4=11/12; minimum aperture=1/12. All values are rational. A synthetic camera exposing only outside the gap cannot distinguish this closure from a constant-open trace if exposure histories match; matching endpoint aperture alone is insufficient to establish the resting condition.

Falsification: verify endpoint velocities independently or propagate a velocity interval in a reachable-set solver. A resting-endpoint certificate is invalid when a gap starts during an eyelid movement. Reject any product implementation that substitutes inferred rest for measured rest.

Human evidence: NONE. Product: require endpoint-velocity confidence bounds; otherwise revert to speed-only E002-371 or abstain.
