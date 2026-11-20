# E002-559 RESULT | Decoder-dependent validity of human annotation acquisition

Date: 2026-10-31. Kernel E002-371. Frozen protocol: [E002_559_FROZEN.md](E002_559_FROZEN.md). Evidence tier: **real Chromium browser + generated synthetic video**, no physiological or physical camera measurement.

## Reproduced instrument failure

Earlier [hosted run 41155599319](https://github.com/sushxnthd/lucent/actions/runs/41155599319) failed **after** hashing the local H.264/MP4 fixture: Chromium returned `canPlayMp4=""`, `errorCode=4`, `DEMUXER_ERROR_NO_SUPPORTED_STREAMS`, `videoWidth=0`. Switching from `file://` to a secure loopback origin did **not** resolve it. This is a codec availability failure, not an anatomical failure. The source SHA-256 alone did not guarantee usable video.

## Independently hosted positive control

[GitHub Actions run 41160549562](https://github.com/sushxnthd/lucent/actions/runs/41160549562), at commit [78c04fc](https://github.com/sushxnthd/lucent/commit/78c04fc7d60b0885add5562c4be0aeb5ef9b1c8d), **completed successfully**. The test uses a generated VP8/WebM synthetic fixture (320x240, nominal 30 Hz, two seconds) to exercise the existing E002-555 offline video rater, plus E002-497's native-frame rater. Only the test fixture's encoding changed; no anatomical adjudicator or physical evidence gate was weakened.

The hosted job's structured output was:

```json
{
  "experiment": "E002-557",
  "status": "SYNTHETIC_BROWSER_E2E_PASS",
  "native": {"packets": 2, "frames_each": 260, "synthetic_nuisance_abstentions": 260},
  "video": {"packets": 2, "synthetic_closed_agreements": 1, "hardware_clock_verified": false},
  "real_human_raters": 0,
  "physical_captures": 0,
  "certified_human_motion_bounds": 0,
  "heldout_physical_predictions": 0,
  "product": "ABSTAIN_UNCALIBRATED",
  "release": "BLOCKED"
}
```

The browser suite checked a matching source-video SHA-256, decoded 320-pixel video width, two independently generated synthetic rater exports, a synthetic landmark pair, the existing independent auditor, zero off-loopback network requests, and 260 explicit nuisance abstentions. This is a **tested acquisition mechanism**, not proof of human rater independence, source frame accuracy, shutter calibration, or closure observability.

## Falsification / limitations

- H.264 failed on this hosted Chromium build; VP8 succeeded. Codec-dependent decodability is an instrument nuisance. A browser can hash source bytes without decoding usable frames.
- VP8 success cannot be extrapolated to human MP4, HEVC, variable-frame-rate files, rolling shutters, camera clocks, or anatomical geometry.
- Synthetic agreement is **not** a human agreement statistic. Presentation timestamps are **not** acquisition timestamps.
- No new authenticated human video, independent human annotations, physical shutter captures, certified continuous-time speed/acceleration ceilings, or held-out physical closure predictions were obtained.

## Next decisive experiment

Obtain permissioned high-frame-rate human eye recordings with known sensor acquisition timing; retain original bytes and establish a frame-index/time map by two decoders or abstain on discrepancies. Obtain two genuinely independent blinded anatomical rater exports. Separately calibrate optical exposure response, clock uncertainty, geometry and motion error. Freeze ordinary-camera exclusion predictions before viewing held-out high-rate reference. Measure calibration/abstention and nuisance-stratified false-exclusion rates; do not infer a hard physiological motion ceiling from observed sampled maxima.

The E002-371 product boundary remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. No clinical fatigue or blink-negative claim is justified by this run.
