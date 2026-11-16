# Lucent bounded alpha — local reaction-time demonstration

**Status:** research-branch prototype, not a released or validated fatigue product.

## Run
1. Download `reaction-time-demo.html` from this directory, then open it locally in a modern browser. No account, server, build tool, camera, or network connection is required.
2. Choose a self-reported sleepiness rating (1–9). This is a subjective input, not a diagnostic scale interpretation.
3. Start five trials. Wait for the panel to turn green; respond by tap/click or keyboard Space/Enter. An early tap retries the trial.
4. Read the five browser-input latencies and median. Optionally export the JSON locally. Reset or close the tab to discard in-memory session data.

## Automated smoke test
With Node.js 18+ from the repository root, run:

```sh
node alpha/test-reaction-time-demo.cjs
```

The deterministic VM harness checks basic state transitions and export behavior. It is **not** a browser/device timing calibration, and no independent device validation is claimed. Before public tagging, verify Chrome/Firefox/Safari on desktop and mobile, keyboard and touch paths, page visibility/focus interruption, delayed responses, offline operation, and that no requests or storage writes occur. Capture browser version, device, OS, test date and outcomes.

## Measurement boundary
The only measured quantity is browser input-response latency, including screen, OS, browser and motor delays. The median is descriptive, not a validated fatigue or alertness score. Self-report is displayed separately. **No hidden-eyelid-closure inference, physiological velocity ceiling, diagnosis, risk classification, or fitness-to-drive determination is produced.** E002-371's shutter-gap result remains conditional on independently calibrated human velocity and physical shutter timing. Until then camera-derived closure claims must abstain.

## Privacy and failure behavior
The page has no application network calls, accounts, camera use or persistent storage. Export is user-initiated and writes a JSON download through the browser. Focus loss, hidden page, invalid elapsed time and responses over 10 seconds invalidate the current task. Do not rely on the output for safety-critical decisions. If sleepy, rest rather than using the task to establish safety.

## Release blockers
- Run and document automated test execution, not just test source.
- Complete actual-device browser acceptance and accessibility checks.
- Freeze an explicit version, file checksum and installation instructions.
- Verify the packaged artifact against a clean offline install.
- Keep unsupported camera/fatigue claims disabled; no medical claims.
