# E002-664 | Phase-locked aliasing defeats unlimited frame-count calibration (2026-11-05 UTC)

## Falsification
A periodic triangular aperture trajectory with period 1/f, aperture 1 at every frame timestamp n/f, and aperture 0 halfway between timestamps is 2f-Lipschitz. Its sampled finite differences are identically zero for any number of frames, despite a complete closure in every gap. Thus arbitrarily long phase-locked footage cannot estimate the requisite velocity ceiling from frame differences. This is a constructive identifiability counterexample, not a claim about human blink periodicity.

For f in {24,30,60,120} Hz and frame counts {2,30,300}, the executable fixture checks observed apertures all 1, hidden midpoint apertures all 0, and observed finite-difference velocity 0. Plugging that invalid estimate into the sharp E002-371 gap certificate falsely certifies absence of closure above threshold 0.3; using the true 2f ceiling yields lower bound zero and abstention. A half-frame phase shift exposes the closure in this idealized fixture. Phase shifting is not a substitute for independently validated velocity and shutter calibration in real cameras.

## Dimensionless boundary and nuisance controls
For equal open endpoints, the sharp lower bound is 1-V/(2f); certification requires V/(2f) < 1-threshold. The counterexample sets V/(2f)=1. Exposure integration, rolling shutter, motion blur, timestamp uncertainty, missingness, eyelid geometry and detector gain require separate bounds; none is covered by the point-sample fixture.

## Frozen human test
With authenticated high-rate video, independently bound velocity uncertainty using high-rate annotated trajectories, then freeze 24/30/60-Hz downsampling rates and multiple phase offsets before viewing participant-held-out sequences. Compare hidden high-rate closure events with low-rate certificates. Cluster inference by participant, record coverage/abstention, and reject any deterministic absence certificate contradicted by high-rate ground truth. Do not infer deterministic velocity ceilings from the same low-rate observations. If high-rate access is unavailable, test a programmable moving aperture with a synchronized independent timing sensor and label evidence instrument-only.

## Product consequence
Do not turn longer observation windows or stable low-rate inter-frame differences into deterministic blink-absence claims. Require independently justified V and camera timing/exposure calibration; otherwise ABSTAIN_UNCALIBRATED, production BLOCKED.

Run: python3 research/observability/e002_664_phase_lock.py. Exact rational arithmetic; synthetic fixture only; no human/physical validation or independent replay.
