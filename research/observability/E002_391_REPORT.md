# E002-391 — Repeated-event phase sweep breaks *fixed* aliases, not single-event nonobservability

**Evidence tier:** Frozen, reproducible synthetic shutter instrument. Not physical-camera or human evidence. No publication-level novelty asserted.

## Why this experiment
The E002-371 conditional shutter-gap theorem and E002-390 velocity self-calibration counterexample leave an actionable instrument-design question: can a calibration bench expose otherwise persistent aliases by changing the sensor phase across repeated, independently timed events? We froze the acquisition model and predictions before running (commit `656198c`). This is an **instrument calibration** experiment, not a human blink detector.

## Fixed model and results
Aperture is a continuous triangular event `a(t)=min(1,40|t|)` with trough 0 and slope magnitude 40/s; threshold 0.2. A 30-Hz camera takes 5-ms rectangular exposures. Twelve identical events occur at 400-ms intervals (phase-locked to exactly 12 frame periods). Each of 12,000 trial sets has either one fixed random camera phase, an independent uniform phase for each event, or a fixed phase plus independent ±1-ms jitter. All exposure values are integrated analytically; an independent numerical quadrature oracle checks 100 phases.

| Acquisition condition | At least one event detected |
|---|---:|
| One event, uniform phase (12,000-point deterministic grid) | 30.00% |
| 12 events, locked camera phase | 3,559/12,000 = **29.66%** |
| 12 events, independent uniform phase | 11,812/12,000 = **98.43%** |
| 12 events, fixed phase + ±1-ms jitter | 4,163/12,000 = **34.69%** |
| 12 events, independent phase, bounded ±0.03 optical error and conservative positive rule | 11,643/12,000 = **97.03%** |

Exact geometric control: for `theta/V >= exposure/2`, a shutter mean crosses the threshold only if its exposure center lies within `theta/V` of the event trough. Thus the single-cycle capture phase width is `2 theta/V = 10 ms`, and `p=2 theta/(V F)=0.3`. Under **independent** random phases, `P(any detected in N)=1-(1-p)^N=98.6159%` for N=12. This prediction differs from the observed 98.4333% by 0.183 percentage points. Under phase locking, repetition does not improve the capture probability. All five preregistered predictions passed.

## Optical and reference controls
A positive optical detection is accepted only when `observed shutter mean + epsilon < theta`, with independently justified `epsilon=0.03` in the simulator. Zero false positives occurred for 12,000 always-open synthetic controls. Under an **unbounded** optical bias of -0.30, a nonclosed aperture of 0.40 is misreported as 0.10 in all 12,000 adversarial controls: this is a constructed failure, not an estimated rate. Such unbounded conditions require **abstention**. A simulated 1000-fps, 0.25-ms exposure reference detects the specified triangular event; this does not validate a physical high-speed reference.

Independent checker derives p from threshold geometry, checks five quadrature values at and inside the detection boundary, and compares randomized observations to `1-(1-p)^12`. The primary oracle's largest shutter-integral discrepancy was `7.80e-10`.

## What this does **not** establish
- Repeated identical events are an artificial instrument assumption. Human blink shapes and phases are not identical; event timing may correlate with the camera.
- This does not rescue a single missed closure. Even an excellent repeated-event detection rate cannot certify absence of a crossing in one event.
- Phase randomization needs controllable acquisition timing and **event-phase independence**. Ordinary phone cameras may not expose reliable phase control.
- The simulated `40/s` velocity is not an independently measured physiological upper bound. Geometry, gain, brightness, gaze, glasses, blur, occlusion, rolling shutter, missing frames, exposure timing and clock error remain external calibration requirements.
- No new human/physical-camera validation or primary-literature priority proof is claimed. Randomized sampling/phase dithering is established measurement practice.

## Product decision
**Allow as a laboratory protocol candidate:** controlled repeated-event phase sweeps with independent reference and calibration gates to detect fixed-phase aliasing. **Reject:** treating a multi-event success rate as an individual blink guarantee, using frame-difference velocity as a physical bound, or inferring fatigue/PERCLOS. **Abstain:** absent independently established timing, optical response, velocity, event independence or nuisance bounds.

## Reproduction
```bash
python -m pip install numpy
python research/observability/e002_391_phase_instrument.py
python research/observability/e002_391_independent_check.py
```
The primary script writes `e002_391_results.json`; do not retune seed 39111, trial count or thresholds after the frozen protocol. The independent checker does not import the primary implementation.

**Next decisive milestone:** prospective paired human RGB/high-speed evaluation, as specified in `E002_391_HUMAN_PROTOCOL.md`. No upgrade to Lucent's product claims before it passes.
