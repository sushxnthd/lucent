# E002-598 | Offline anatomical-review interface: executable handoff, not human validation

Date: 2026-11-02. E002-371 primary research kernel. [Frozen protocol](E002_598_FROZEN.md) was committed first at `3d583e6`, before implementation. Evidence tier: **SYNTHETIC_OFFLINE_REVIEW_INSTRUMENT_ONLY**.

## New substantive artifact

The [offline reviewer interface](e002_598_offline_rater.html) turns E002-595's previously authenticated, blinded 95-to-nominal-30-fps LPW reviewer packet into an executable manual anatomical-labeling workflow. The prior interface was a blank JSON file, which required raters to edit structured records manually. This instrument instead accepts the assigned `BLANK_ANATOMICAL_RATINGS.json` and the corresponding local `ARM_0`, `ARM_1` or `ARM_2` directory, verifies all 60 expected 640x480 images, and permits frame-by-frame lid-margin annotation.

The reviewer first selects a single measurement column, then upper and lower eyelid margins, and supplies at least 0.5 px uncertainty. The export records raw lid y coordinates, measurement x, uncertainty and explicit nuisance flags. It **never fills iris diameter from the image**: that scale must be calibrated independently, and downstream anatomical classifications remain uncertain until then. Nuisance flags clear measurements instead of forcing OPEN/CLOSED. Unreviewed frames remain explicit. No native indices, participant IDs, source video hashes or owner mappings are displayed or exported.

This is a private, local-file research instrument, not a deployed product. It does not contain human imagery, real rater decisions, clinical outputs, network calls, telemetry, autosave or physical-certification logic. A browser can still retain caches/downloads or be compromised; offline operation is not a complete privacy/security guarantee.

## Verification completed in this run

- The actual HTML's embedded JavaScript parsed successfully in a V8 syntax check.
- A synthetic JavaScript browser-stub replay loaded the **actual committed HTML code** with ten blind clips and 60 image stubs, including an extra blank JSON file in the selected ARM directory. The corrected loader accepted the expected 60 PNGs, rejected a prefilled template, and verified exact blind clip/frame mapping.
- In the synthetic replay, three reviewer clicks produced upper y=210, lower y=240, measurement x=320, uncertainty=2, and **iris diameter=null**. Export retained 59 explicitly UNREVIEWED frames, without fabricating labels or source identifiers.
- The [committed Node.js VM regression suite](e002_598_offline_rater_test.cjs) adds adversarial missing-image, duplicate-image, wrong-rater, prefilled-template, nuisance-abstention and clearing tests. The [hosted workflow](../../.github/workflows/e002_598_offline_rater.yml) is committed; **hosted execution was not verified at report time**. The direct V8 replay is not a substitute for a physical-browser, human-usability or privacy audit.
- During review, an actual usability defect was found and fixed: directory pickers can return the packet's blank JSON alongside PNGs, so the loader must ignore non-PNG metadata rather than reject the entire valid folder. A prototype-property blind-clip key was also explicitly disallowed.

## How to use privately

Copy the standalone HTML into the **private** reviewer workspace, open it locally in a browser, choose the reviewer-specific blank E002-595 ARM template and select that ARM folder. The reviewer must not receive the owner-only mapping or the other rater's export. After reviewing, download the JSON and transfer it through an approved private channel to the E002-576 source-bound evaluator, with independent iris-diameter/geometry error budget. Do not upload private images or ratings to GitHub or use CI to conduct human review. See [concrete acquisition and review protocol](E002_598_HUMAN_STUDY.md).

## Science and release boundary

This work advances the **operational feasibility of acquiring independent human anatomical labels**, not the empirical truth of E002-371. There are still **zero** newly obtained independent human rater pairs, independently calibrated physical shutters, hard human velocity/acceleration ceilings, or participant-disjoint physical gap predictions. The previously rejected dark-pixel and vertical-edge proxies remain rejected.

The decisive next step is genuinely independent human review, followed by prospectively frozen synchronized-camera predictions under independently validated timing, anatomical and motion premises. A confirmed closure in any supposedly excluded physical gap falsifies the claim or its premises. If no hard velocity envelope can be established, deterministic no-hidden-closure claims remain forbidden.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. **Draft PR #26:** open, unmerged. **Hush:** separate branch and PR #45 not modified in this primary-validation run.

## Native-reference coverage added after initial ARM-only freeze

An explicit [prospective extension](E002_598_NATIVE_EXTENSION_FROZEN.md) was committed before expanding the UI. The same tool now accepts **E002-574 native 95-fps templates** (ten clips x 19 frames = 190 PNGs, no arm field), alongside the original E002-595 nominal 30-fps ARM templates (ten clips x six frames = 60 PNGs). It preserves each template's export schema, refuses mixed native/ARM shapes, and never claims the 95-fps images are instantaneous anatomical ground truth. The [regression suite](e002_598_offline_rater_test.cjs) includes native missing-frame refusal, 190-image mapping, native export, and mixed-template refusal. These added checks are committed, not yet hosted-verified. This closes the practical gap in collecting both sides of a paired blinded human-review study; **no reviewer has yet supplied real annotations**.
