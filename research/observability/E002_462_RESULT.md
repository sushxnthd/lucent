# E002-462 — High-speed reference cameras can be observationally incomplete

**2026-10-26. Evidence tier: exact synthetic/instrument-model counterexample and independently implemented checks. No human recordings, physical instrument, independently authenticated acquisition rate, or physiological upper bound.** [Primary frozen protocol](E002_462_FROZEN.md) committed at `8eb82fa` before implementation; [finite-duration supplement](E002_462_FINITE_DWELL_FROZEN.md) committed at `20dffba` before its separate implementation, after the primary point-contact experiment. The supplement is not presented as the original preregistered primary outcome.

## Scientific finding: reference-frame absence is not a negative anatomical label

E002-456's proposed >=400-fps anatomical reference should **not** be treated as a perfect binary closure oracle. Even with perfect geometry, a linear anatomical-aperture sensor, authenticated uniform 0.30-ms shutters, no clock error, and *hypothetical* bounded closing/opening velocities, two distinct trajectories can produce **exactly identical shutter observations**: (i) a constant-open trajectory, and (ii) a true subthreshold closure entirely between exposures. This is a direct reference-identifiability counterexample, not a new general theorem; it applies the E002-371/457 reachability logic to the *reference camera itself*.

For baseline aperture b, closure threshold c=2.0 mm, assumed C=567.103928 mm/s and O=274.616337 mm/s, a point-contact triangular event has total duration `(b-c)/C + (b-c)/O` (velocities converted to mm/ms). If this duration fits strictly inside the dark gap between reference shutter supports, the positive and negative trajectories yield **exactly the same exposure-averaged observations**, regardless of static photometric calibration.

### Frozen primary examples and phase sweep

| Reference | b (mm) | Exposure | Point-contact critical duration | Frozen result |
|---|---:|---:|---:|---|
| 400 fps | 2.30 | 0.30 ms | 1.621437 ms | Indistinguishable from always-open |
| 1000 fps | 2.10 | 0.30 ms | 0.540479 ms | Indistinguishable from always-open |

The seeded, uniform-phase sweep used **1,000 synthetic trajectories per nonoverlapping cell**. Counts of events *exactly indistinguishable* from constant-open (not a physical frequency estimate):

| fps | baseline b | 0.30-ms shutter | 0.80-ms shutter |
|---|---:|---:|---:|
| 400 | 2.30 mm | 208/1000 | 36/1000 |
| 400 | 2.10 mm | 664/1000 | 456/1000 |
| 1000 | 2.30 mm | 0/1000 | 0/1000 |
| 1000 | 2.10 mm | 164/1000 | 0/1000 |
| 2000 | 2.30 mm | 0/1000 | ABSTAIN: overlapping supports |
| 2000 | 2.10 mm | 0/1000 | ABSTAIN: overlapping supports |

The exact uniform-phase fraction for this synthetic event family is `max(0, frame_interval - shutter_width - event_duration) / frame_interval`. The Monte Carlo counts are compatible with these deterministic geometric fractions. They are **not** blink rates, sensor error rates, or population estimates.

**Important limitation of the primary:** its event only *touches* c at an instant. Thus the reported 1000/1000 missed-by-naive-mean-threshold outcomes are mathematically trivial and must not be cited as practical detector miss rates. The decisive test is identical positive/negative shutter observations; the separate finite-duration experiment below removes the point-contact degeneracy.

### Frozen finite-duration subthreshold supplement

The separate frozen supplement constructed nondegenerate piecewise-linear closures with a genuine interval **strictly below** the 2.0-mm threshold. Exact integration and independent JS support calculations agree:

| Reference | Baseline | Minimum | Subthreshold duration | Entire excursion support | Shutter dark gap | Observed difference vs always-open |
|---|---:|---:|---:|---|---|---:|
| 400 fps | 2.30 mm | 1.95 mm | **0.370239 ms** | [0.282829, 2.274505] ms | (0.15, 2.35) ms | **0.000000 mm** |
| 1000 fps | 2.10 mm | 1.98 mm | **0.138096 ms** | [0.168399, 0.846973] ms | (0.15, 0.85) ms | **0.000000 mm** |

Both positive sequences are **exactly indistinguishable from a constant-open negative control** at every ideal reference exposure. These are intentionally adversarial constructed trajectories, not measured human motions. The 1000-fps example has only ~0.003 ms clearance to the second exposure support, so even modest unmodeled timing errors could change that *particular* construction; the broader identifiability issue remains whenever an excursion fits inside a dark gap.

## Reproduction and adversarial controls

- [Analytic shutter integrator and 1,000-phase sweeps](e002_462_reference_aliasing.py) with [10 Python tests](test_e002_462_reference_aliasing.py): exact frozen examples, negative control, timing units, kernel widths, malformed inputs, nuisance abstention and deterministic sweep.
- [Finite-duration exact integrator](e002_462_finite_dwell.py) with [3 additional Python tests](test_e002_462_finite_dwell.py), including a shifted phase where the shutter *does* observe a difference.
- [Independent JS point-contact check](e002_462_independent_replay.cjs) and [independent JS finite-dwell check](e002_462_finite_dwell_independent.cjs) use independent support arithmetic without importing Python.
- [Primary aggregate](E002_462_SYNTHETIC_AGGREGATE.json), [finite-duration aggregate](E002_462_FINITE_DWELL_AGGREGATE.json), and [CI workflow](../../.github/workflows/e002_462_reference_aliasing.yml) preserve reproducibility.
- **Local execution:** 13/13 Python adversarial tests passed; both independent Node scripts passed. Hosted GitHub Actions status must be checked separately; do not infer a hosted pass from the existence of a workflow.

The synthetic evaluator refuses unknown geometry, brightness, missingness, blur, gaze, glasses, sampling, clock, rolling-shutter, or exposure-kernel status; it never returns physical certification. The idealized counterexample isolates *temporal* information loss and does not show those nuisances are harmless.

## Direct consequence: change the reference-labeling and validation gate

**Withdraw the assumption that >=400 fps plus two anatomical raters provides complete negative closure labels.** A frame showing an open aperture is a positive observation of that exposure only, not proof of uninterrupted opening between exposures. Do not score an unseen closure as absent solely because no sampled high-speed frame shows it.

For the physical phantom, the reference truth must come from an **independent continuous-position encoder, contact switch/event trace with independently verified temporal response, or a demonstrably sufficient bounded-speed/exposure-aware reference model**. Synchronize a shared hardware time code, record raw exposures and readout, and withhold the continuous trace until ordinary-camera predictions are frozen. Include finite-duration closures and controls near the derived reference observability boundary. Use interval-censored labels: `WITNESSED_CROSSING`, `EXCLUDED_ONLY_UNDER_AUTHENTICATED_REFERENCE_BOUNDS`, and `REFERENCE_UNRESOLVED`. Unknown is not open.

For human work, no continuous anatomical ground-truth oracle has yet been obtained. A high-speed camera can positively witness an adequately resolved closure, but *negative* claims require separate reference completeness validation; otherwise classify those intervals as unresolved. Independent anatomical raters do not repair missing temporal samples. Validate participants and acquisition sessions disjointly, with geometry/brightness/blur/gaze/glasses/sampling/clock nuisance strata and authenticated exposure kernels.

## Priority and completion boundary

The mathematical construction follows classical sampling/aliasing and bounded-derivative reachability; E002-371/457/460 already contain the relevant conditional laws. The new contribution here is a **frozen, executable falsification of the proposed high-speed-reference labeling assumption** and an explicit study/product veto. It does **not** establish original measurement-science priority, validate a physiological cap, or measure human error.

**E002-371 remains NOT PHYSICALLY VALIDATED.** No hidden-closure guarantee, blink-duration, PERCLOS, fatigue, or medical claim is authorized. Product remains `ABSTAIN_UNCALIBRATED`. S21/S22 remain sealed; no merge or release. Hush's independent PR #45 is untouched. Next decisive work: acquire an independently timed continuous physical-aperture trace and perform a prospective, blinded moving-aperture study, followed by genuinely independent anatomical human measurements.
