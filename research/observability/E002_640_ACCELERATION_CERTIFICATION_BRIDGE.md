# E002-640 | Acceleration-certified intersample velocity: executable falsification bridge

Status: **synthetic instrument design, not human or physical validation**. This packet addresses E002-639: finite-difference speed is not a continuous-time velocity certificate.

## Independently measurable premise

Let aperture x(t) be twice differentiable over an independently timed high-rate reference interval of duration h, and suppose a **separately validated** absolute acceleration ceiling |x''(t)| <= A holds throughout that interval. Let d=|x(t+h)-x(t)|/h. Then the true absolute velocity obeys

    sup |x'(s)| <= d + A*h/2.

Proof: with v=x', the mean m=(1/h) integral v equals the signed secant. For any s, |v(s)-m| <= (A/h) integral_0^h |s-u| du <= A*h/2. Equality is achievable at an interval endpoint by a linear velocity profile with slope ±A. This is sharp under the stated assumptions.

**Dimensionless certification penalty:** P=A*h/(2*d) for d>0. At d=0, the entire certificate is A*h/2, not zero. This specifically defeats the E002-639 zero-interframe-motion shortcut. A=0 requires independently established constant velocity, not an inferred property.

## Predeclared instrument tests

1. Synchronized encoder/reference shutter at >=1000 Hz with measured exposure start/end, hardware timebase and uncertainty. Treat nominal FPS as insufficient.
2. Independent acceleration ceiling from an encoder/inertial instrument with calibrated bandwidth and an uncertainty budget; do not estimate A solely from the same sampled video. If jerk or acceleration between encoder samples is unconstrained, **ABSTAIN**.
3. For each high-rate interval, compute V_cert = |delta x|/h + A*h/2; propagate conservative timebase, spatial, exposure and threshold uncertainty. Use the maximum across all intervals as the continuous-time speed ceiling *only within the certified time span*.
4. Freeze ordinary-camera sample windows and phase offsets before revealing continuous high-rate reference closures. Score strict EXCLUDE predictions using E002-631; one confirmed closure under a certified EXCLUDE falsifies the pipeline.
5. Cross conditions: geometry/pose, gaze, glasses, light, blur, missing frames, rolling shutter and clock drift. Any unsupported condition must abstain; keep participants and capture sessions disjoint between calibration and held-out evaluation.
6. Record both positive and negative findings, including fraction of ordinary-camera gaps that can be certified. A method that abstains everywhere is sound but not a useful product.

## Exact synthetic controls

- h=0.010 s, d=0, A=10000 mm/s²: certified ceiling = 50 mm/s; a triangular velocity profile with endpoint velocities +50 and -50 mm/s and acceleration -10000 mm/s² attains the bound while returning to the same aperture.
- h=0.010 s, d=0, A=0: certified ceiling = 0; no hidden excursion is possible under the independently certified zero-acceleration premise.
- E002-639's smooth hidden closure is **not** excluded unless its actual acceleration envelope is independently certified; sampled endpoint equality is not a certificate.

## Human evidence protocol and decision gate

Prospective consenting adult participants, controlled illumination and synchronized high-speed camera with independently checked frame timestamps. Two blinded raters label complete eyelid contact/occlusion and aperture uncertainty from full-rate sequences; disagreements adjudicated before opening ordinary-camera predictions. Human annotation alone cannot certify continuous-time acceleration; if no independent physiological acceleration envelope is defensible, restrict all sharp exclusion validation to the motorized aperture instrument and report human data as descriptive only. No clinical drowsiness or sleepiness inference follows from a closure-bound test.

**Current evidence:** zero new human recordings, zero new physical trials, zero independently certified acceleration envelopes. Product remains `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. This is a calibration bridge, not a physiological law or validation claim.
