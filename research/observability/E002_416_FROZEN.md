# E002-416 — freeze: reference-video negative-label identifiability

Date: 2026-10-24. Evidence tier: prospective reference-adequacy falsification with independently checkable synthetic trajectories; **not measured human aperture, camera timing or human velocity**. This is a necessary correction to the E002-407/408 human-validation interpretation, not a claim of new Lipschitz mathematics.

## Question
Can a 160–240-fps reference recording, even with correctly measured instantaneous aperture at its frames, justify treating an apparently open/open inter-frame interval as a negative hidden-closure ground-truth label? Freeze the following test *before implementing the triage code*.

## Exact target
For each pair of externally calibrated instantaneous physical aperture observations at times t0<t1, lower/upper uncertainty intervals [L0,U0],[L1,U1], threshold theta, and independently justified deterministic velocity cap V, compute the sharp minimum possible aperture between observations. With gap d=t1-t0 plus worst-case independent timing errors d_eff=d+2*clock_error_s, the conservative lower envelope is max(L0-V*t,L1-V*(d_eff-t),0). Its minimum over t in [0,d_eff] is the piecewise value obtained by clipping the two-cone intersection to the interval. A reference interval is NEGATIVE_CERTIFIED only when the envelope minimum is strictly above theta. An interval is POSITIVE_WITNESSED only when at least one independently calibrated instantaneous endpoint has U<=theta. All others are REFERENCE_UNRESOLVED. No shutter-averaged or EEG-aligned frame is accepted as instantaneous physical aperture.

## Frozen predictions
H1: With theta=.20, L0=L1=.30, V=60 normalized-aperture units/s and zero timing error, 160-fps and 240-fps reference gaps are REFERENCE_UNRESOLVED, while 1000-fps is NEGATIVE_CERTIFIED. The dimensionless ratio V*d/[2*(.30-.20)] is respectively 1.875, 1.25 and .30.
H2: At 160 fps, a piecewise-linear trajectory matching both .30 endpoints has midpoint .1125 and hence a hidden threshold crossing; endpoint-only labels incorrectly call it negative.
H3: For the 1000-fps case, adding +/-1.5 ms independent clock uncertainty per endpoint changes the negative certificate to unresolved.
H4: Without an independently justified hard velocity cap, *no open/open interval* may be negative-certified, regardless of nominal frame rate; a measured sample maximum is not a hard bound.
H5: Missing/blur/glare/occlusion/gaze/glasses/geometry invalidation, unauthenticated physical aperture or frame timing, nonfinite numbers, impossible aperture intervals and duplicated/nonmonotone timestamps never produce negative certificates.
H6: A directly observed U<=theta can be POSITIVE_WITNESSED only if independent instantaneous physical-aperture calibration is authenticated; the tool must not turn either reference label into a Lucent product certificate.

## Implementation/verification
Implement a dependency-free reference-label triage module, an **independently coded** discretized adversarial oracle checking sharpness across 1,000 seeded consistent cases, and an executable negative/positive/missingness/clock test suite. Keep evidence and product decisions separate. Do not use this synthetic work to claim measured human velocity or validate E002-371. The resulting gate is intended to prevent an invalid *human-validation denominator* in a future prospective study. No private human video or annotation files are to be committed.

## Decision
If H1–H6 hold, classify the uncalibrated E002-407 632-frame pilot as reference-unresolved for physical negative labels. Next decisive evidence remains two independent blinded human annotations plus independently calibrated camera exposures, geometry and velocity. Preserve `ABSTAIN_UNCALIBRATED` for all physical product claims.
