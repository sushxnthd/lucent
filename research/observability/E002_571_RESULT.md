# E002-571 RESULT | Real-browser measured anatomical handoff passed

2026-10-31. Primary E002-371 human-observability kernel. Frozen protocol was committed **before implementation** at [`13c68a6`](https://github.com/sushxnthd/lucent/commit/13c68a6803392d572bb95d2c3c4b1519045fd414). Executable and dedicated workflow were committed at `0bb40ff` and `e036982`, respectively. [Hosted run 41217025993](https://github.com/sushxnthd/lucent/actions/runs/41217025993) **completed successfully on the exact implementation head `e0369822a0c35b332ca63e1754dd31a7c9b595bd`**. The actual hosted job log was inspected, not inferred from a queued state.

## New operational evidence, not new physiology

E002-557 had exercised the native-frame rater's all-abstain path in a real browser, but not its two-landmark measurement path. Its initial hosted attempt failed before executing the measurement test because Playwright's `wait_for_function` invoked evaluation forbidden by the page's strict Content Security Policy. E002-571 instead uses the existing E002-497 HTML and E002-492 adjudicator unchanged, with Playwright locator assertions and real canvas clicks.

Two independent **synthetic browser contexts** each loaded 260 generated native-size PNGs and their own canonical blank A/B template, refused incomplete export, entered measured upper/lower lid landmarks and positive iris/landmark uncertainty on two frames, marked the other 258 frames POOR_GEOMETRY, exported private JSON and passed through the unchanged E002-492 adjudicator. The frozen oracle required one overlapping and one disjoint conservative rater interval; the browser and adjudicator reproduced both.

| Hosted result | Observed |
| --- | ---: |
| Browser contexts (not humans) | 2 |
| Synthetic frames per context | 260 |
| Measured frames per context | 2 |
| Explicit nuisance abstentions per context | 258 |
| Dual-measurable adjudicated positions | 2 |
| Overlapping conservative intervals | 1 |
| Disjoint conservative intervals | 1 |
| Unreviewed positions | 0 |
| External network requests | 0 |
| Physical measurement or human anatomical reference | **0** |

The test ran on hosted Google Chrome, with pinned Playwright 1.56.0 and Pillow 12.0.0, and exited successfully after approximately 56 seconds. No generated images, individual JSON exports or facial data were uploaded as artifacts. The aggregate status was `SYNTHETIC_MEASURED_BROWSER_PASS`.

## Scientific and release interpretation

This closes a specific **instrument usability gap**: the measured-input path of the existing offline anatomical review tool is executable in an actual browser, exports both blinded packets and preserves conservative disagreement rather than silently converting it into agreement. It does **not** establish that two actual humans can consistently identify anatomy on the authentic S01 video, authenticate their independence, or calibrate iris diameter, sensor timing, shutter exposure, rolling rows, human motion or unseen physical closures. The synthetic raters are scripted browser contexts, not human observers.

No E002-371 theorem, threshold, clip selection or product claim was changed. Next external evidence remains two genuinely independent blinded S01 reviews using the existing E002-502/E002-567 private handoff, then photodiode-authenticated synchronized physical acquisition and presealed held-out human predictions. Avoid another synthetic shutter law or automated optical proxy.

**Hard evidence counters remain:** independent human rater pairs 0; authenticated physical shutter captures 0; certified continuous-time human velocity upper bounds 0; held-out physical closure predictions 0. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Hush remains a separate branch/PR and was not modified.
