# E002-420 — exposure-integrated reference ambiguity, executed synthetic falsification

**Date:** 2026-10-24. **Protocol frozen before implementation:** `E002_420_FROZEN.md`, commit `21ab7ee45173bc1a89bec98edf30276ee518b4f0`. **Evidence tier:** analytic construction and independently executed numerical simulation, **not** human eyelid measurement, real-camera calibration, or independent external replication.

## Decisive finding

Two distinct physically admissible **scalar aperture trajectories** produce exactly the same two calibrated boxcar exposure averages. One remains open throughout; the other crosses the closure threshold between camera observations. This extends E002-416's instantaneous reference-frame warning to a specified exposure-integrating measurement model. The result is classical sampling non-identifiability, **not a new general theorem**. Equality applies to the **scalar exposure-average observable**, not necessarily to full RGB frames, motion blur texture, or an arbitrary camera response kernel.

For aperture baseline `a`, velocity cap `V`, frame separation `d`, exposure duration `E` satisfying `0<E<=d`, and threshold `theta`, define:

- Open world: `x_A(t)=a-V*E/8`, constant.
- Hidden-closure world: `x_B(t)=a-V*min(t,d-t)` on `[0,d]` and `a` outside.
- Both exposures are boxcar windows centered at `0` and `d`.

Both worlds yield the same two measurements `y=a-V*E/8`. The closure world's minimum is `a-V*d/2`. When `a-V*d/2<=theta<y`, identical open-valued measurements are consistent with opposite closure outcomes. The witness is bounded in `[0,1]` and respects the **hypothetical** Lipschitz cap `V`.

### Frozen numerical example

| Quantity | Value |
|---|---:|
| Frame separation | 4.166667 ms (240 Hz) |
| Exposure duration | 2 ms |
| Hypothetical velocity cap | 60 normalized-aperture units/s |
| Closure threshold | 0.20 |
| Measured average, both frames, both worlds | **0.285** |
| Always-open world minimum | **0.285** |
| Hidden-closure world minimum | **0.175** |
| Physically authenticated camera or human measurement | **None** |

The exposure-adjusted ratio for this *specific witness family* is `R=V*(4*d-E)/(8*(y-theta))`; `R>=1` is the constructed ambiguity condition when `y>theta` and the witness is admissible. In the frozen example `R=1.294117647...`. **R<1 is not a general no-hidden-closure certificate** for arbitrary trajectories, shutter kernels, or unknown physical bounds.

## Independent numerical result

A separate midpoint-quadrature oracle was implemented without calling the primary aperture function. Local execution on 2026-10-24 passed all three test groups:

1. Frozen 240-Hz/2-ms witness: both independent 20,000-bin exposure integrals equal **0.285** to better than `1e-9`, matching the analytic prediction.
2. **1,000 seeded randomized admissible witnesses:** all four independently computed exposure observations per witness agreed with the analytic common measurement to within `1e-10`; every witness separated open from hidden-closure truth and preserved the [0,1] physical range and product abstention. This is a synthetic family, not 1,000 independent cameras or humans.
3. Negative controls: exposure longer than frame gap, negative physical aperture, nonfinite velocity, zero exposure and incompatible closure thresholds were rejected or returned **no constructed ambiguity**. Invalid numerical-bin input was rejected.

Local reproduction (no paid APIs):

```bash
cd research/observability
python -m unittest -v test_e002_420_exposure_alias
python e002_420_exposure_alias.py
```

Dedicated workflow: `.github/workflows/e002_420_exposure_alias.yml`. **Hosted CI status must be checked separately; this report does not assert a hosted pass.** The vector figure `E002_420_EXPOSURE_ALIAS.svg` shows the two trajectories and exposure windows.

## Scientific and product consequences

A high-speed camera with a known nominal frame rate and even perfectly known boxcar exposure time cannot turn two scalar open exposure measurements into a physical negative closure label by default. This is particularly relevant to E002-407/408's proposed human reference labels: independent human annotations and calibrated acquisition remain necessary, and full-image information may resolve ambiguities that the scalar model cannot. E002-419's unresolved-reference denominator must be preserved. This experiment **does not** measure the frequency of hidden human blinks or establish a human hard velocity ceiling.

The implementation always returns `ABSTAIN_UNCALIBRATED`, `product_claim_authorized=false` and `physical_provenance_authenticated_by_tool=false`. It never emits a product no-hidden-closure certificate.

## Physical validation that would change the evidence tier

Build a programmable moving aperture/occlusion phantom and independently measure its actual trajectory with a photodiode or faster trusted reference. Record the same target with two real cameras at 240 Hz (or verified equivalent) and randomized exposure durations. Verify exposure kernels, rolling-shutter row timing, frame timestamps, target luminance, geometry and independent clock uncertainty; include blur, glare, translation and dropped-frame controls. Preregister which scalar extracted aperture averages should be ambiguous and which are distinguishable. Hold out a camera/exposure condition until after predictions are frozen. A nominal display refresh rate is not a calibrated physical trajectory. Do not treat unmeasured hardware timing or self-reported shutter metadata as authenticated.

**Blocking physical evidence:** two independent real-human rater sheets, validated eyelid-margin geometry, independent camera/clock/shutter measurements, defensible physiological velocity bounds and held-out participant/device predictions. The world-class completion gate remains unmet. Hush is unaffected.
