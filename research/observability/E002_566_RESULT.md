# E002-566 RESULT | Authentic two-rater handoff end-to-end experiment

Date: 2026-10-31. Frozen **before code/source run** at [E002_566_FROZEN.md](E002_566_FROZEN.md), commit `a928b3e`. Primary E002-371 kernel; existing branch and draft PR #26.

## The missing evidence this run targets

The E002-502 private dual-rater handoff passed synthetic privacy tests, while E002-496 and E002-500 separately verified the authentic 260-frame S01 source packet. **The combined E002-502 source-to-two-reviewer workflow had not been demonstrated on original human-source bytes.** E002-566 tests exactly that unverified integration, with no new clip selection, source archaeology, image-motion proxy or physiology threshold.

The frozen [hosted experiment](../../.github/workflows/e002_566_authentic_handoff.yml) downloads only the checksum-pinned Motor Imagery S01 archive (Zenodo 18970793; MD5 `fb56109542a13aa7879778833fe4cbaa`) into a private ephemeral runner. The existing E002-502 command then runs E002-492 source extraction, E002-496 packet validation, E002-500 full 260-frame replay, and constructs the two separate blinded 260-frame reviewer bundles. The new [independent post-handoff auditor](e002_566_authentic_handoff_audit.py) compares all source-bound PNG bytes, validates distinct blank A/B templates, rejects extra mapping files, tampered frames, symlinks and altered viewers, and emits only fixed-key sanitized aggregate counts. Private media and source ZIP are deleted and never uploaded as artifacts.

## Verified before persistence

**8/8 local synthetic adversarial tests passed**, using [test_e002_566_authentic_handoff_audit.py](test_e002_566_authentic_handoff_audit.py): valid bundle stays uncalibrated; tampered frame, missing frame, extra mapping, cross-rater template, prefilled annotation, symlink frame and viewer tampering all reject. The GitHub-hosted workflow also invokes the seven preexisting E002-502 synthetic tests.

**Authentic-source hosted outcome at report creation: PENDING.** Workflow was committed at `d0708dd`, triggering its push path. Do not interpret a queued/running job, a local synthetic pass, or the earlier E002-500 source replay as a successful E002-566 authentic dual-rater handoff. If the authentic source run fails, preserve the failure and repair the acquisition path before further science. The aggregate artifact, if produced, contains no source images, identities, source indices or raw labels.

## Scientific meaning and next step

A future `AUTHENTIC_RATER_BUNDLES_VERIFIED` would establish only that source-bound blinded reviewer packets can be generated correctly on an ephemeral runner. **It would not constitute two independent human ratings**, since both bundles remain unannotated. The actual reviewers must independently annotate authorized private copies on a local machine; the CI runner must never be used to distribute source imagery. Only then can the precommitted E002-507 native-frame alias adjudication be attempted.

No physical shutter/clock acquisition or certified continuous-time physiological speed ceiling exists. A native-frame alias witness, even if observed, would not validate a shutter-integrated E002-371 hidden-closure claim. Further software-only work is deprioritized after hosted verification.

**Evidence:** human rater pairs 0; authenticated physical shutter captures 0; certified continuous-time human speed ceilings 0; held-out physical closure predictions 0. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush branch and draft PR #45 unchanged.

## Post-freeze hosted observation (2026-10-31, verified after original report)

The previously pending **authentic-source end-to-end** experiment completed successfully in [GitHub Actions run 41185934001](https://github.com/sushxnthd/lucent/actions/runs/41185934001), commit `d0708dd5ed206b1c62abf664d6bc1d8c5634fac9`. The actual `authentic-private-handoff` job 124492742369 reports success for the original seven synthetic controls, eight independent tampering/privacy controls, native decoder provisioning, authentic-source download, packet generation, and independent post-handoff audit. This result was checked against the completed job's decoded logs, not inferred from the queued run.

The successful private-run output was:

```json
{"continuous_time_speed_certified":false,"experiment":"E002-566","frames_per_rater":260,"heldout_physical_predictions":0,"independent_human_raters":0,"physical_clock_authenticated":false,"private_rater_bundles":2,"product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED","shutter_calibrated":false,"source_bound_native_frames":260,"status":"AUTHENTIC_RATER_BUNDLES_VERIFIED"}
```

The 438-byte sanitized aggregate ZIP was uploaded as [artifact 13037410025](https://github.com/sushxnthd/lucent/actions/runs/41185934001/artifacts/13037410025). Raw footage and reviewer packets were not published as artifacts. The archive was not independently downloaded or opened during this follow-up; the result above is directly observed in the job log.

**Interpretation:** An authentic human-source 260-frame packet can now be transformed into two separate intact, unannotated, blinded reviewer bundles in the hosted acquisition environment. This removes a *software acquisition feasibility* blocker, not a *human measurement* blocker. It does not verify sensor frame timing, true eyelid closure, rater reliability, continuous-time velocity, shutter response, or ordinary-camera exclusion accuracy. Two generated reviewer bundles do not equal two human raters.

**Prospective human evidence gate:** Distribute the private packets to two independent human annotators under the existing E002-502/E002-507 instructions; prohibit source indices, timestamps, predictions or cross-rater discussion until both exports are sealed. Retain separate immutable video/frame hashes and rater exports. Report disagreement, abstentions, and adjudicated positive *visible-frame* closure witnesses, without treating unmarked frames as confirmed open. Only use a time axis if authenticated independently of AVI presentation metadata. Keep the E002-371 hidden-closure/physical-camera claim blocked until independently measured velocity *upper* bounds, shutter timing, clock uncertainty and held-out prospective tests exist. If access to authorized reviewers or hardware cannot be arranged, report the absence explicitly rather than simulating raters.

**Evidence tier after hosted completion:** authentic source-to-blinded-reviewer packet generation **verified**; independently blinded anatomical rater pairs **0**; authenticated physical shutter captures **0**; certified continuous-time physiological speed ceilings **0**; held-out physical closure predictions **0**. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
