# E002-432 — frozen missing-frame observability experiment

**Frozen 2026-10-25 before running the simulator.** Primary kernel: E002-371. Evidence tier: **synthetic boxcar camera / ideal physical-aperture surrogate**. Not human or real-device validation; not a new general theorem.

## Question and counterexample

Does treating two successive *retained* eyelid measurements as if they were successive camera frames produce a false no-hidden-closure certificate when a frame between them is dropped? The independent variable is the original acquisition timestamp/missingness mask, not row number in the exported table.

Use 30 Hz frame centers (d=1/30 s), ideal 2-ms boxcar exposures, physical aperture threshold theta=2.000 mm, endpoint means 2.100 mm, and a **hypothetical** hard speed cap V=4.000 mm/s (not a physiological claim). A frame at t=d is dropped; frames t=0 and t=2d survive. World A stays at 2.100 mm. World B is flat at 2.100 mm through t=E/2, then decreases linearly to 1.980 mm at t=d, rises symmetrically and is flat from t=2d-E/2 onward. Its maximum speed must be <=4 mm/s, and the two surviving exposure averages must match World A exactly. Both worlds have the same dropout mask. Their different closure status is therefore not identifiable from retained aperture observations.

**Frozen predictions:** the wrong compressed-row gap d yields a candidate lower 2.100-Vd/2=2.033333...>theta, falsely certifying World B; the actual gap 2d yields 2.100-V(2d)/2=1.966666...<=theta, requiring abstention. With independent aperture uncertainty +/-0.005 mm and endpoint timestamp error +/-0.5 ms, the conservative actual-gap lower must also abstain. An un-dropped midpoint exposure must witness the closure. These are conditional calculations within the ideal-boxcar model, not a deployment authorization.

## Holdout stress protocol

Using deterministic seed 432, construct 1,200 independently parameterized synthetic trials, 600 constant-open and 600 dip trajectories. For dips, uniformly draw depth in [0.08,0.125] mm (slope <=4 mm/s); ground truth is closure iff minimum aperture <=2 mm. The dropout decision at the center is either MCAR p=0.15 for both types, or deliberately MNAR p=0.90 for closure dips and p=0.05 otherwise. Apply both dropout regimes to the **same frozen trial parameters** with independent random draws. Evaluate a naive retained-row certificate against a timestamp-aware certificate using the exact boxcar integrals and the fixed V; compare false-certification counts and candidate coverage, including the witnessed closure control. Do not retune parameters after inspecting outcomes.

**Release gate:** timestamp-aware certificates must have zero witnessed false certificates in both simulated regimes; naive compressed-row certification must produce at least one false certificate under MNAR. The test must explicitly report the conditional model and coverage loss. Independently verify trajectory speed, shutter integration, the equality of retained measurements, and rejection of invalid/missing timestamps. A zero simulated false-certificate count is not a population safety estimate.

## Scientific interpretation and physical follow-up

This is a targeted falsification of *timestamp compression and unmodeled missingness*, not of E002-371's correctly applied temporal law. Real pipelines must retain original sensor capture times, frame IDs, explicit missing intervals, shutter support and clock uncertainty; dropped/duplicate/reordered/undated frames must not silently shorten gaps. Motion blur, gaze, glasses, geometry, illumination, and physiological velocity are not authenticated here and must independently gate physical claims. The real study should prospectively log raw frame IDs and hardware timestamps before tracking, deliberately induce random and blink-associated dropouts, independently annotate high-rate physical eyelid traces, and test unseen participants. Until that evidence exists, ABSTAIN_UNCALIBRATED for physical hidden-closure, blink-duration, PERCLOS and fatigue claims.
