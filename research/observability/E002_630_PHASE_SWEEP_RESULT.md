# E002-630 | Synthetic phase-sweep shutter-gap falsification (2026-11-03)

**Evidence tier:** deterministic mathematical/synthetic instrument surrogate; not physical acquisition, not a human eyelid experiment. This test is a boundary regression for E002-371/E002-626 and does not validate the physiological envelope.

## Frozen setup and independently computed result
A piecewise-linear triangular occluder has baseline aperture 2 mm, closure threshold 0 mm, and a stipulated 200 mm/s closing/opening speed ceiling. Simulated exposure-free gaps are 19, 20, and 21 ms. A 101-point closure-phase grid ranges from -10 to +30 ms in 0.4 ms increments for each gap. Ground truth is evaluated analytically from the triangular trajectory; the exclusion certificate uses only exact endpoint apertures and the stipulated speed bound. This is an **oracle-endpoint** control: the actual camera cannot obtain those instantaneous endpoints without calibrated exposure integration.

A separate exact-rational calculation of the 303 phase/gap combinations gives **8 exclusions, 148 interior closure witnesses, and 0 false exclusions**. These finite counts are synthetic consistency checks, not an estimate of human sensitivity or safety. Equality at 20 ms is treated as attainable closure and is never excluded. The code also computes a numerical exposure average to demonstrate that sensor integration need not equal instantaneous aperture.

Reproduce with `python3 research/observability/e002_630_phase_sweep.py`. The script uses only Python standard library. The aggregate above was separately recomputed using exact Fraction arithmetic; committed-script hosted execution has not been verified. The phase sweep has no independent velocity-envelope calibration and cannot serve as an empirical performance claim.

## Critical failure modes and next physical experiment
1. Motorized aperture with encoder or independently timed photodiode ground truth, synchronized to 30/60 fps camera and >=240 fps reference. Measure real exposure start/end, rolling-shutter row phase, clock offset/drift and aperture error.
2. Freeze the 19/20/21 ms boundary sweep and nuisance matrix before acquisition: brightness, geometry, gaze-like translation, glasses-like reflections, blur, missingness, exposure integration and clock jitter. Use certified upper velocity envelopes from a sensor **independent of the ordinary camera**. If the independent sensor cannot certify a continuous-time bound, the certificate must abstain.
3. Preserve the negative case: any physical hidden closure labeled EXCLUDE is a falsification of the asserted assumptions or implementation. Do not repair by post-hoc threshold tuning on the evaluation sequence.
4. Human translation requires participant-disjoint blinded anatomical truth and a separately defensible physiological envelope; motor dynamics do not transfer to human eyelids.

**Product:** `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. This synthetic result changes no authorized human-facing claim.
