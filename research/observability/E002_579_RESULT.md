# E002-579 | Real LPW development-video motion-proxy falsification result

**Evidence tier:** authenticated human eye-region *video*, non-anatomical image statistic. **Result:** negative under the frozen criterion. **Decision:** reject this proxy as a selector for anatomical review. This is **not** evidence that no blink occurred.

## Provenance and execution

- Precommitted protocol: [E002_579_FROZEN.md](E002_579_FROZEN.md), before computing real-video statistics.
- Source: original LPW archive, `LPW/1/1.avi` (development participant 1 only); verified source SHA-256 `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86`.
- Source properties: 2,000 frames, reported 95 fps, 640x480 source; FFmpeg area-downsampled to 80x60 grayscale for this *proxy only*. Reported FPS is not independent shutter/clock authentication.
- [Hosted Actions run 41252756295](https://github.com/sushxnthd/lucent/actions/runs/41252756295): **success**, executed 2026-10-31 23:32–23:34 UTC; source acquisition, preregistered computation and synthetic self-test passed. No source imagery or individual frame indices uploaded.
- Code: [e002_579_real_motion_proxy.py](e002_579_real_motion_proxy.py). The full aggregate JSON was emitted in the hosted job log. The frozen thresholds were native-step normalized dissimilarity >=0.05 and three-frame endpoint dissimilarity <=0.02; no threshold was tuned after viewing the results.

## Predeclared primary outcome

| Condition | Eligible 4-frame windows | Flagged hidden *image-proxy* excursions | Abstained |
|---|---:|---:|---:|
| Baseline | 1,997 | **0** | 0 |
| Positive affine brightness change, alternate frames | 1,997 | 0 | 0 |
| Alternating one-pixel horizontal jitter | 1,997 | 0 | 0 |
| 3x3 box blur | 1,997 | 0 | 0 |
| Every twentieth native frame missing | 1,600 | 0 | 397 |

Phase-specific baseline counts: 0/666, 0/666, 0/665 for starts modulo 3 = 0,1,2. The photometric control gave maximum distance error 0.0 at logged precision; this confirms the intended algebraic invariance for this execution, **not** camera illumination robustness.

The baseline native-step dissimilarity medians were 0.001946, 0.001950, 0.002045 by phase, with 99th percentiles 0.046505, 0.044272, 0.044279. Baseline endpoint-distance medians were 0.009000, 0.009050, 0.009498. Thus the locked native-step threshold 0.05 lies above the phase-specific 99th percentiles, explaining why the combined criterion was exceptionally selective in this recording. This does **not** prove absence of anatomical excursions.

### Nuisance stress: changes in the *continuous statistic* despite unchanged binary flags

- Alternating one-pixel jitter: native-step median rose from ~0.002 to ~0.050 (about **25x**) across phases; endpoint-distance median rose from ~0.009 to ~0.042 (about **4.5x**). The endpoint requirement still suppressed all flags.
- 3x3 blur: native-step median fell to ~0.00045 (about **0.23x** baseline); endpoint-distance median fell to ~0.0025 (about **0.28x** baseline).
- Missingness: 397/1,997 windows abstained, not treated as negative observations.
- Flag-set Jaccard is **undefined** (both sets empty), not a robustness score of 1.0. A zero-to-zero flag comparison does not establish nuisance invariance or diagnostic sensitivity.

## Frozen decision and interpretation

The preregistered primary outcome is **zero baseline flags**, so **kill this motion proxy as a prospective anatomical-review selector**. No retuning the thresholds, swapping features, or selecting promising frames post hoc for confirmatory inference. This failure is a useful negative result: a mathematically invariant image statistic can be non-informative under realistic imaging variation and predeclared thresholds.

There are no independent anatomical labels on this video. Consequently this result cannot estimate sensitivity, specificity, false-negative rate, blink prevalence, closure duration, eyelid velocity, or E002-371's physical observability boundary. It cannot exclude hidden closures. The 95-fps stream is not an independent calibrated physical shutter reference.

**Product consequence:** keep `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Prohibit the E002-579 proxy from selecting human-review windows or supporting blink, PERCLOS, fatigue, sleepiness, or closure-absence claims.

**Next decisive experiment:** execute the already frozen E002-573/574/575/576 participant-disjoint, source-bound anatomical protocol with two genuinely independent blinded human reviewers, without motion-proxy-based triage. Independently synchronize camera exposure and photodiode timing in the E002-567 physical experiment and obtain defensible continuous-time velocity constraints before making held-out shutter-gap predictions.

**Evidence not obtained:** genuine independent human rater pairs 0; authenticated physical shutter captures 0; certified human eyelid-velocity ceilings 0; held-out physical closure predictions 0. Hush research branch/PR #45 unaffected.
