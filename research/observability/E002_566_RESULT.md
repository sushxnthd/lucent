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
