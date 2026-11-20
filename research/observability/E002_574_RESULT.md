# E002-574 | Private LPW participant-disjoint window-plan result

Date: 2026-11-01. Primary kernel: E002-371. The [precommitted predictions](E002_574_FROZEN.md) were persisted before the executable and tests. This work implements the frozen [E002-573 LPW human-reference protocol](E002_573_LPW_HUMAN_REFERENCE_PROTOCOL.md); it does not change that protocol or supply new human observations.

## Tested result (synthetic inventory only)

On a deliberately synthetic inventory of 22 participants with three videos each (66 total), with one 190-frame and two 380-frame videos per participant:

- The fixed participant-level SHA-256 ordering produces **11 DEVELOPMENT / 11 HELD_OUT participants**, never mixing a participant between sets.
- Thirty-three held-out videos yield **330 distinct nonoverlapping 19-frame windows** after the frozen ten-window-per-video cap, or **6,270 frame review positions per rater** (12,540 for two independent raters).
- Reversing the entire video inventory leaves all selections, blinded IDs, private mappings and rater templates byte-equivalent after canonical serialization.
- Each A/B template has 330 opaque clip IDs, 19 blank anatomical positions per clip, and **no participant identity, video digest, source frame index or prefilled closure label**.
- All **13 local Python adversarial tests passed**. They cover participant leakage, duplicate digests, malformed counts, missing/extra videos, unsafe identifiers, symlink inventory, existing output and private file layout.
- A dedicated hosted GitHub Actions workflow was committed. **Hosted success has not been verified.**

These counts are **synthetic fixture arithmetic**, not LPW measurements. A 330-window pilot is a substantial human-annotation workload; do not imply that reviewers have been recruited or that any frame has been annotated.

## Private one-shot use after lawful acquisition

On an authorized machine outside the repository, build a source-verified private inventory JSON with the exact schema:

```json
{"videos":[{"participant_id":"<opaque_ID>","video_id":"<opaque_ID>","video_sha256":"<64_lowercase_hex>","native_frame_count":190}]}
```

The displayed object is an **illustrative one-video schema**, not a complete eligible inventory. The actual input must contain 66 videos from 22 participants, exactly three videos per participant. The IDs must reflect documented original source identities. Independently verify each digest and native frame count before passing them to this program.

```bash
python research/observability/e002_574_lpw_plan.py \
  --inventory /private/lpw_verified_inventory.json \
  --outdir /private/lpw_e002_574_plan
python -m unittest discover -s research/observability -p "test_e002_574_lpw_plan.py" -v
```

The script writes only owner-private mapping and separate blank A/B templates with restricted permissions. **It does not download, decode, resize, package or verify actual human frames.** The E002-497 S01 viewer is fixed to 20 x 13 frames and 320 x 288 pixels and **must not** be reused for LPW's 19-frame, variable-geometry windows. A native-geometry LPW viewer and source-bound frame-packet audit remain necessary before real human annotation.

## Scientific interpretation and stop rule

This is a reproducible, privacy-aware **human-validation selection instrument**, not a validated shutter-gap law, native-frame alias witness, anatomical measurement, or physiological speed bound. LPW's reported ~95-fps acquisition rate is not independently authenticated per-frame exposure timing. Do not claim that the synthetic 95-to-ordinary-rate index decimation is physical 30-fps shutter acquisition. The data license is noncommercial research only.

**Unchanged evidence ledger:** acquired/verified LPW archive 0; independent human anatomical rater pairs 0; authenticated physical shutter captures 0; certified continuous-time velocity ceilings 0; held-out physical closure predictions 0.

Next non-synthetic actions: one lawful local LPW acquisition, verified native video/frame mapping, native-geometry private rater handoff, two genuinely independent blinded human reviews, and the separately frozen E002-567 synchronized optical-camera study. Do not run this synthetic planner repeatedly as a proxy for empirical progress. Until the physical/human gates pass, `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush remains separate.
