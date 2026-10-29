# E002-523 | Finite optical-response sampling cannot certify a shutter-concentration cap

Date: 2026-10-29. Primary E002-371 kernel. Frozen protocol: [E002_523_FROZEN.md](E002_523_FROZEN.md), committed first as `046ac85edc7c6774a31b898892b68d1739a39d32`. Branch `research/observability-human-boundary`; draft PR #26 remains unmerged.

**Evidence tier:** exact two-world synthetic instrument identifiability counterexample, deterministic executable, 15 local adversarial tests, and independently coded exact-rational Node.js replay. **No camera, photodiode, high-speed human video, human rater, or physical eyelid-speed measurement was acquired.** Hosted CI must be checked separately.

## What was falsified

E002-522's physical closure-duration law requires an independently certified essential-supremum bound `q(t) <= R/T` on the *continuous-time* normalized shutter-response weighting. It would be unsafe to infer `R=T*max(sampled photodiode response)` from finite point samples, even if samples are noise-free and the total response integral is independently known.

Construct two normalized nonnegative shutter kernels on a 10-ms exposure:

- World 0: `q0(t)=0.1 /ms` (uniform).
- World 1: `q1(t)=q0(t)+A(t)-B(t)`, with a narrow triangular positive pulse `A` of area 0.02 strictly inside (1,2) ms, and a compensating triangular negative dip `B` of equal area and 0.8-ms width strictly inside (5,6) ms. The dip never drives q1 negative. Both kernels equal 0.1 /ms at **all 11 exact integer-ms sample points**, and both integrate to 1. But the true peak of q1 is `0.1+0.04/w` per ms, so its concentration cap is `R1=1+0.4/w`, unbounded as w shrinks.

Use closure threshold theta=0.20. In World 1, physical aperture is zero only on the narrow positive-pulse support of duration w and is 0.201 everywhere else. Its shutter-weighted mean is `M=0.201*(1-0.02-w/10)`, below theta. In World 0, aperture is constant M for the whole exposure, so the weighted mean is **identical** and the physical closure duration is 10 ms. Thus even perfect finite response samples, exact normalization, and the same measured mean cannot distinguish the two worlds.

## Frozen numerical results (exact fractions in executable)

| World 1 pulse width | True R1 | Identical observed mean M | Incorrect R=1 inferred minimum closure | Actual closure | Correct R1 inferred minimum |
|---|---:|---:|---:|---:|---:|
| 0.01 ms | 41 | 0.196779 | 0.16105 ms | 0.01 ms | 0.00392805 ms |
| 0.0001 ms | 4001 | 0.19697799 | 0.1511005 ms | 0.0001 ms | 0.00003777 ms |

**Failure:** inferring R=1 from the 11 samples overstates a *guaranteed* physical closure duration by more than 16x in the first construction and more than 1500x in the second. Both worlds are compatible with the same calibration observations and measured aperture mean. The E002-522 law itself is **not** falsified when its independently attested true R is used.

This is an exact counterexample to a proposed calibration inference, not evidence that any actual camera has a 0.0001-ms shutter-response spike.

## Independently defensible calibration rule

If a separate instrument experiment justifies a global Lipschitz bound `|q(t)-q(s)|<=L|t-s|`, sample errors are bounded by delta, and h is the maximum distance from any exposure time to the nearest sample, then:

```
q(t) <= max_i(y_i + delta) + L*h
R <= T*(max_i(y_i + delta) + L*h).
```

For 1-ms sampling over 10 ms with exact endpoints, h=0.5 ms. With hypothetical readings 0.1 /ms, independently bounded delta=0.005 /ms and L=0.02 /ms^2, the conditional cap is R<=1.15. **The script cannot establish that L or delta is physically valid.** If these assumptions are only fitted from the same point samples, the counterexample remains.

This is a standard sampling/regularity implication, not a novel mathematical theorem. Any alternative anti-alias or integrated-photodiode calibration must independently bound the continuous-time response between measurements; simply increasing the finite sampling rate is not a proof of an essential-supremum bound.

## Physical validation acceptance protocol

1. Before looking at eyelid data, freeze camera model, exposure mode, rolling-shutter row, optical wavelength/intensity range, analog front-end bandwidth, photodiode response and independent timing uncertainty. Acquire *raw* intensity data and independently timed light-source/photodiode waveforms; never rely on nominal FPS or encoded-video timestamps.
2. Calibrate radiometric linearity, saturation, dark offsets, illumination geometry and temporal response at multiple pulse phases and pulse widths, with independently characterized source rise/fall times. Repeated phase scans are useful **falsification tests**, not by themselves proof of a global response cap.
3. Supply an external upper envelope for unresolved between-sample response (certified bandwidth/regularity or a validated integrating acquisition model), with uncertainty propagated to a conservative R. If the analog front end, LED, shutter, photodiode or sampling clock has unbounded/unmeasured nuisance response, record `R=UNKNOWN`.
4. Freeze unseen capture conditions and acceptance thresholds before validation. Test all previously excluded ordinary-camera blind gaps against independently contained high-speed anatomical witnesses, with native-index provenance and two blinded human raters per E002-519. Record all abstentions and failures. An apparently open reference frame is not a no-blink ground truth.
5. Never use the E002-523 synthetic response as a stand-in for human calibration. Release requires genuine external physical measurements and participant-disjoint prediction tests.

## Reproduction

```bash
python -m unittest discover -s research/observability -p 'test_e002_523_sampled_shutter.py' -v
python research/observability/e002_523_sampled_shutter.py --output /tmp/e002_523.json
node research/observability/e002_523_independent_replay.cjs
```

The 15 Python tests passed locally; independent Node.js BigInt cross-multiplication reproduced both exact counterexamples. Both implementations verify the numerical implications, not acquisition provenance.

**Product consequence:** point-sampled photodiode readings alone do not authorize the E002-522 duration feature. Keep `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Existing S01 independent anatomical ratings: 0; authenticated physical shutter captures: 0; certified human velocity ceilings: 0; participant-disjoint physical predictions: 0. Further synthetic response sweeps are not justified; the next decisive work is actual calibrated capture and blinded human review.
