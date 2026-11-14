# RGB-SCALE-OBSERVABILITY-001

## Question

Can the released PupilSense RGB-webcam millimetre regressor be used as Lucent's
relative pupil-response observable without explicit geometric calibration?

This is a **derived engineering audit**, not a new human experiment. It uses the
public scale-stress CSV outputs from the independent
[CondadosAI PupilSense/EyeDentify reproduction](https://github.com/CondadosAI/pupil-diameter-webcam).
The underlying model/data are Shah et al.'s EyeDentify/PupilSense assets.

## Frozen analysis

Two tests are run by `experiments/rgb_scale_observability_audit.py`.

1. **Tight apparent-scale stress.** For each of eight published clips, treat the
   1.0× trace as the reference. Compare the binocular mean at 0.9×, 1.0× and
   1.1×. For every frame compute the scale-induced range, average that range
   over frames, and divide by the reference trace's peak-to-peak temporal signal.
2. **Personal-baseline power-law correction.** Use the median 1.0× eye-box width
   as a per-clip baseline and correct the predicted millimetres by
   `(w_ref / w)^alpha`. Select `alpha` only on seven clips and evaluate on the
   held-out eighth. Repeat for each eye.

The correction test is deliberately simple. It asks whether the scale failure
can be repaired by the sort of single-parameter personal baseline Lucent already
assumes, without learning a clip-specific rescue.

## Result

At the 0.9–1.1× scale band, the **median ratio of false scale-induced range to
the real temporal peak-to-peak signal was 0.765** across the eight clips; the
mean ratio was **0.878**. In **2/8 clips**, the average false range exceeded the
entire reference temporal signal.

The leave-one-clip-out power-law correction helped on average but was not
reliable:

| Metric | Raw | Corrected |
| --- | ---: | ---: |
| mean RMSE, all tested scales | 0.1659 mm | 0.1409 mm |
| mean RMSE, 0.9–1.1× only | 0.0758 mm | 0.0715 mm |

The correction improved **11/16** eye×clip holdouts across all scales and only
**9/16** in the tight 0.9–1.1× band. It therefore worsened a substantial
fraction of unseen clips.

## Decision

**FAIL:** raw PupilSense millimetres do not satisfy Lucent's geometry-invariance
requirement.

**FAIL:** a single personal-baseline power-law correction is not robust enough
to rescue the observable.

This does **not** imply that ordinary RGB pupillometry is impossible. It narrows
the measurement design: Lucent should test an explicit dimensionless/reference-
normalized pupil observable rather than treating a learned absolute millimetre
regressor as the sensor.

Relevant prior work already uses this class of control, so Lucent should not
claim novelty for normalization itself:

- SmartPLR uses a pupil-to-iris ratio for smartphone pupillometry.
- Recent webcam pupillometry work normalizes pupil area by a framewise reference
  length to reduce camera-position dependence.
- Recent smartphone work also uses iris geometry as a face-to-screen distance
  reference.

The research contribution, if any, must come from what a calibrated/normalized
ordinary-RGB signal enables for **short active probing and state prediction**,
not from the normalization trick.

## Next decisive experiment

The next cloud-side target is **RGB-REFERENCE-OBSERVABILITY-002**:

1. use public RGB eye data with a tracker reference where licensing/access allows;
2. extract a dimensionless pupil/iris or pupil/reference signal directly from
   frames, without absolute-mm regression;
3. evaluate waveform fidelity person-wise under controlled luminance changes;
4. stress distance/scale, eye color, glasses, lighting, and frame rate;
5. freeze a minimum waveform-fidelity gate before connecting the signal to any
   fatigue/vigilance target.

Until that gate passes, E002 ordinary-phone RGB observability remains open.
