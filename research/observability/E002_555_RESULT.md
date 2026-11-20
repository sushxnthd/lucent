# E002-555 RESULT | First usable blinded human-video annotation handoff

2026-10-31. Primary E002-371 human-observability workstream. Frozen protocol was committed first at b2cc4ad. Evidence tier: **working offline annotation code and local parser tests only; no actual human footage, no physical shutter calibration, no certified physiological bound.**

## Why this was necessary
E002-548/549's one-sided witness logic could check supplied records but did not produce independent anatomical annotations from video. After E002-554 explicitly ruled out further synthetic shutter-kernel tuning as the primary next step, this run built a concrete acquisition-to-adjudication handoff rather than another threshold simulation.

- [Offline browser rater](e002_555_offline_rater.html): local video input (complete SHA-256, maximum 200 MiB), local frame canvas, two normalized image-space upper/lower eyelid landmarks, visual open/closed/uncertain labels, seven explicit nuisance flags, opaque sample IDs, anonymous rater ID, JSON export. No network requests or external dependencies. Raters must be blinded to each other's annotations and to Lucent exclusion predictions. Browser presentation time is recorded, **not hardware exposure time**.
- [Independent Python two-rater audit](e002_555_rater_audit.py): strict schema, source-video hash and packet identity, distinct declared rater IDs, identical sample sets and timestamps, finite in-range landmarks, computed separation integrity and nuisance validation. Produces only aggregate counts, no facial video or coordinates. Agreement on closed is \`RATER_CONCORDANT_UNCALIBRATED\`, open is \`REFERENCE_NEGATIVE_CENSORED\`, disagreements/quality flags are \`CENSORED\`. No outcome certifies a continuous-time hidden closure.
- [Adversarial test suite](test_e002_555_rater_audit.py): **17/17 local Python methods passed** including all seven nuisance flags, forged source mismatch, duplicate sample, wrong timestamp, false hardware-timing claim, malformed coordinates and no-promotion. Offline UI JavaScript passed \`node --check\`.
- [Dedicated CI workflow](../../.github/workflows/e002_555_rater_audit.yml) committed. Hosted success is not claimed until independently checked.

## Reproduction and first physical handoff
1. Obtain an authorized native eye video (e.g. 150-fps Eye-BCI or 400-fps FaceBase only under their applicable access terms). Preserve original file and its independent SHA-256, consent/access documentation, acquisition configuration, and native hardware timestamps separately. **Do not upload participant media or rater exports to the repository.**
2. Open \`e002_555_offline_rater.html\` locally in a Web Crypto-capable browser; if the browser denies Web Crypto for \`file://\`, serve the directory on \`127.0.0.1\` only. Two blinded raters separately load the same video and receive identical opaque sample IDs and presentation-time targets. Record all missing, blurred, occluded, glasses/gaze/brightness and geometry concerns.
3. Export two separate JSON files and run \`python research/observability/e002_555_rater_audit.py rater_A.json rater_B.json\`. Audit must return \`release=BLOCKED\` even if both label a closure.
4. Independently establish shutter exposure support, rolling-row timing, clock uncertainty, anatomical normalization/transfer, continuous-time hard kinematic ceiling and precommitted E002-371 ordinary-camera excluded gaps. Only then may an externally reviewed, positively witnessed anatomical closure enter the E002-548/549 prospective falsification pipeline.

## Known limitations and negative results
- No authorized public 150/400-fps native human footage was downloaded; existing high-speed candidates require controlled access. Lower-rate openly available blink videos cannot certify the needed continuous-time velocity ceiling.
- Browser presentation timestamps and displayed video frames are **not** sensor acquisition timestamps or proof of actual exposure integration. Pixel landmarks are not anatomical calibration. Declared distinct rater IDs do not authenticate independence.
- Browser runtime end-to-end smoke test could not be completed in the local sandbox because Chromium blocked both \`file://\` and loopback HTTP navigation by administrator policy. JavaScript syntax and Python audit were checked locally, but UI functionality in a normal browser is not yet independently demonstrated.
- This is a **human-validation acquisition artifact**, not a new measurement-science theorem, physiological result, or product readiness evidence. It does not close the world-class completion gate.

**Lucent product:** \`ABSTAIN_UNCALIBRATED\`; production \`BLOCKED\`. Authenticated shutter captures 0; independent human anatomical rater pairs 0; certified hard human velocity/acceleration ceilings 0; held-out physical predictions 0. Next run must prioritize obtaining and analyzing authorized human or physical optical evidence, not another synthetic instrument law.
