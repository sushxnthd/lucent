# E002-618 | Preregistered physical validation: phase-swept shutter-gap falsification

Status: **protocol only; no physical data collected**. Frozen 2026-11-03. This is a prospective instrument-validation experiment, not another reanalysis of Silesian5 annotations.

## Primary question
Can a measured eyelid closure that is present in high-speed ground truth be absent from every exposure of an ordinary-rate camera, and can a *predeclared* velocity-envelope model correctly predict when that is impossible?

## Physical setup and independent calibration
Record the same eye simultaneously with (A) a high-speed reference camera (target >=240 fps, actual exposure-start/end timestamps verified) and (B) a nominal 30 fps ordinary camera. A common visible LED timecode or calibrated optical sync pulse must appear in both fields of view. Measure actual integration/exposure windows with a photodiode + oscilloscope or calibrated light-pulse reference, rather than trusting EXIF/frame-rate declarations. Report synchronization uncertainty, dropped frames and rolling-shutter row offsets. If no trustworthy exposure timing is obtainable, STOP and label the result virtual-sampling-only.

Measure eyelid aperture in mm using an in-plane physical scale or independently calibrated geometry; propagate calibration and tracking uncertainty. Two blinded raters independently label full closure and visibility on the reference recording. Lock threshold and adjudication rules before ordinary-camera inspection. Record gaze, glasses, illumination, motion blur, occlusion and detector failure; exclude ambiguous reference events from the primary endpoint but report them separately.

## Prospective sampling, held-out split, and predictions
Split by **participant**, never by frames or events. Use calibration participants to derive a conservative upper velocity envelope V (if defensible) and anatomical aperture/error intervals; reserve all held-out participants for a single preregistered test. A finite high-speed sample alone cannot certify a continuous-time V; the result is conditional unless a separate acceleration/smoothness model and its uncertainty are independently validated.

For each consecutive ordinary-camera exposure, use measured exposure intervals, not nominal 1/30-second timestamps. Define a *dark gap* G as the time between the end of the first exposure and start of the next, after worst-case synchronization/rolling-shutter uncertainty. Let a and b be lower bounds on eyelid aperture at the gap's two boundaries, and let c be the independently frozen full-closure threshold. For a Lipschitz aperture with |da/dt| <= V, a hidden full closure inside the gap requires

    G >= (max(0,a-c) + max(0,b-c)) / V.

Equivalently define the dimensionless gap budget Q = V*G / (max(0,a-c)+max(0,b-c)) when the denominator is positive. Q<1 rules out a hidden closure **conditional on** the geometry, boundary apertures, threshold, velocity ceiling and timing bounds. Q>=1 means closure is *not ruled out*, NOT that closure occurred. For unequal closing/opening ceilings use (a-c)/V_close + (b-c)/V_open. With uncertain boundary apertures and timings, use the values that make closure easiest before issuing a negative certificate. A continuous camera exposure cannot be treated as a point sample; blur/integration may conceal closure, requiring a separately calibrated optical detection model.

### Primary prospective endpoint
On held-out participants, count high-speed-reference-confirmed full closures that fall within ordinary-camera exposure gaps, stratified by preregistered Q<1 vs Q>=1. **Any** reliable reference-confirmed closure in a Q<1 gap falsifies at least one of the stipulated envelope/measurement assumptions and triggers withdrawal of that certificate family. For Q>=1 report observed omissions, not guaranteed omissions. Report participant-clustered uncertainty and all exclusions.

### Negative controls
1. Static artificial eyelid/occluder with independently driven known trajectories; optical timing and geometry calibration checked before humans.
2. Deliberately offset clocks and vary exposure duty cycle while preserving nominal fps.
3. Adversarial brightness, gaze, glasses, blur, face motion, missing frames and rolling-shutter row positions.
4. Synthetic trajectories that saturate the travel-time bound, used solely to test implementation correctness, not as physiological validation.

## Explicit failure and release criteria
Do not promote a physical no-hidden-closure certificate unless the independent timing/geometry and velocity assumptions survive held-out testing. If the velocity ceiling is inferred from the same held-out closures, label leakage and reject the test. If the exposure-time detector has unbounded false negatives, abstain even when geometric Q<1. Report worst-case subgroup errors and rater disagreements. Do not claim sleepiness, fatigue, attention, or clinical state from a closure detector without independent outcome validation.

Current product consequence: **ABSTAIN_UNCALIBRATED; BLOCKED**. This document specifies how to acquire decisive evidence; it is not evidence that the experiment was conducted.
