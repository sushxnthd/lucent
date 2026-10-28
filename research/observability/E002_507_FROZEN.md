# E002-507 | Frozen dual-rater native-frame alias witness (S01 feasibility only)

Frozen 2026-10-28 **before any independent S01 anatomical labels are available or inspected**. Primary E002-371 branch and existing draft PR #26. This experiment bridges the already frozen E002-492/502 private human-review packet to a **predeclared, anatomy-based falsification** of sparse frame sampling. It is not a camera-speed, shutter, fatigue, or continuous-time validation. The E002-501 optical alias proxy stays retired.

## Prior evidence and precise question

The authenticated S01 source archive (MD5 `fb56109542a13aa7879778833fe4cbaa`) has 20 previously frozen 13-native-frame clips (one image-motion candidate and 19 blinded controls). S01's paper, rehost and AVI have inconsistent nominal frame rates (150, ~500, 1 fps respectively); **none independently authenticates physical time**. Zero independent anatomical labels currently exist.

Question: In each 13-frame clip, do two genuinely independent blinded reviewers find an **anatomically closed native frame** strictly between two anatomically open sparse endpoints? Such a positive would be an observed **frame-index alias witness** against the naive rule "open sparse frames imply no observed closure between them." A negative does not exclude closure between native frames or within exposures.

## Frozen sampling and labels

- S01 calibration participant only. Do not open or select S21–S31 held-out anatomy.
- For **each of 20 clips**, select exactly one native-frame window with endpoints at local indices **3 and 8**, four interior positions **4, 5, 6, 7**. This includes the already frozen candidate center at local index 6. **20 windows**, no optimization on labels, no FPS conversion, no synthetic camera-exposure approximation.
- Use the existing E002-502 local-only reviewer handoff and E002-492 A/B templates unchanged. Two real independent raters, blinded to candidate/control status and to each other, annotate all 260 frames and abstain on gaze, glasses, blur, lighting, occlusion, missing anatomy and poor geometry.
- Because E002-503 falsified common-mode iris-diameter assumptions, require a **separate, independently justified, positive** per-clip iris-diameter error bound `delta_px` before classification. No missing/zero/default error bound. For each rater, aperture interval is `[max(0,g-2e)/(d+delta), (g+2e)/(d-delta)]` with `0<delta<d`, gap `g=lower-upper`, per-landmark error `e`, diameter `d`.
- Freeze the **illustrative threshold 0.10** (normalized iris units) from the existing E002-503 adversary. This is not a clinically validated eyelid-closure definition. Both raters must independently have lower interval >0.10 for OPEN, or both upper interval <=0.10 for CLOSED. All other cases, disagreement and nuisance => UNKNOWN. Shared rater bias is not eliminated by agreement.
- Count a witness only if both endpoints are OPEN and **at least one of four interior native frames is CLOSED**. If all four interiors are OPEN, report `no_observed_interior_closure`, never physical exclusion. If none CLOSED and any UNKNOWN, report `interior_unresolved`. If endpoints are not both OPEN, report `endpoint_not_both_open`.
- Publish **only six aggregate counts** and hard-blocked product status. Never publish native frame indices, per-clip states, identifiable imagery, raw reviewer data or owner-only mapping. An A/B string and a numeric delta do not independently authenticate reviewers or calibration.

## Frozen kill / continuation criteria

A single dual-rater CLOSED interior with two OPEN endpoints establishes an *observed native-frame alias witness conditional on valid human annotations*, but not an actual shutter-integrated hidden blink. Zero witnesses with low coverage cannot establish absence. If >50% of 20 windows lack both OPEN endpoints, or >50% of endpoint-open windows have UNKNOWN interiors, report **pilot infeasible**; do not retune threshold or sample windows. Even high coverage does not validate continuous-time E002-371.

After this S01 pilot, participant-disjoint S21–S31 high-rate testing requires **new preregistration** and independently measured exposure/clock plus a certified physical velocity envelope. Native finite differences alone never certify a hard between-frame velocity maximum.

## Bounded external-data/priority audit (two attempts completed; stop searching)

1. Guttmann-Flury et al. S01 (https://zenodo.org/records/18970793): existing source with real human imagery and frozen private packet, but acquisition rate not independently authenticated and zero dual-rater labels.
2. Katrychuk & Komogortsev 120-Hz VOG dataset (https://zenodo.org/records/13852050), 40 subjects, AVI per subject, roughly 2.7–3.3 GB each, public but no independent shutter/velocity certification. OpenEDS (https://arxiv.org/abs/1905.03702) reports 200-Hz images and 152 subjects but access is upon request. Silesian5 (https://www.blinkingmatters.com/research) reports 100-Hz Basler acquisition but requires a signed license/permission. None supplies the required physical hard speed bound out of the box.
3. Primary-literature novelty check: "The method for quantified analysis and pattern visualization for eye blinking using high-frame-rate video" (https://pmc.ncbi.nlm.nih.gov/articles/PMC12638546/), 80 human volunteers, already quantifies upper-eyelid trajectories from high-frame-rate video. **Do not claim that measuring eyelid displacement/velocity or high-speed blink video is new.** Lucent's candidate contribution is a falsifiable, nuisance-aware **observability/abstention boundary** under explicitly authenticated physical assumptions, not generic blink measurement.

## Privacy, product and completion

The code is an **offline private evaluator**, not an annotation substitute. Its software tests may use fabricated A/B labels solely to verify fail-closed behavior; those are never human evidence. Real ratings: 0; authenticated shutter/clock: 0; certified continuous-time V: 0; held-out physical predictions: 0. `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Do not run further optical proxy tuning or additional synthetic timing sensitivity sweeps in place of independent human reviews and physical calibration.
