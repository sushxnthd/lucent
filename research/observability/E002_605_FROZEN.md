# E002-605 | Frozen independent high-rate blink-label assay and prior-art test

Date: 2026-11-02. Parent E002-371; research branch `research/observability-human-boundary`. This freeze must precede source ingestion, parsing, code, and result.

## Newly identified independent source and priority issue

N. Alsaeedi and D. Wloka, *Sensors* 19(5):1121 (2019), DOI https://doi.org/10.3390/s19051121, report a **100–110-fps eye-facing camera** (OV4689) and a **12-participant** dataset with blink annotations. Dataset: N. Alsaeedi (2019), Mendeley Data v1, DOI https://doi.org/10.17632/9yzdnng594.1, CC BY 4.0. The paper explicitly argues that 30-fps sampling may miss the spontaneous blink's short **pause/fully-closed phase**, citing 13.7 ± 3.3 ms and a heuristic ~73 fps. Thus neither the general possibility of missing a blink pause at 30 fps nor the heuristic frame-rate observation may be claimed as new Lucent discoveries. The cited ± quantity is *not* an individual hard minimum or a continuous-time velocity ceiling. No priority claim for the E002-371 sharp boundary is justified until comparison with its actual theorem assumptions.

## Preregistered source and split

Only this dataset/version; subjects S1–S4 are development for input/schema checks and S5–S12 are a **sealed holdout**. Inspect at most two public acquisition routes: (1) Mendeley Data public files API, (2) its published per-file download URLs. Do not scrape login sessions or work around access controls. Verify any published file SHA-256, and keep images and person-level source annotations out of GitHub.

Accept a frame-index annotation only when its workbook contains unambiguous integer inclusive start/end native frame indices, an explicit subject identifier, and an unambiguous type. Allowed explicit type classes are `blink_event` and `fully_closed`; ambiguous/untyped rows are excluded with counts. Never infer fully closed from a generic blink interval. Never infer physical fps from a nominal codec rate. No optical timing or velocity bound is asserted.

## Frozen analysis

For each valid, nonempty interval [lo, hi], evaluate **exact three-phase native-index decimation**: phase p retains frames n with n % 3 == p, for p=0,1,2. Count per phase whether an interval contains a retained index; report participant-stratified counts, class-stratified missed intervals, and conservative unknown/excluded totals. Predeclared index-law controls: 1-frame interval misses 2/3 phases, 2-frame interval misses 1/3, and >=3 consecutive frames miss 0/3. Test both complete annotation and intentionally missing frames (must abstain if a claimed witness intersects missingness). Treat the test as a **native-index sampling assay**, not a physical 30-fps shutter experiment; event-level detection cannot validate hidden full closure. Do not use S1–S4 to optimize holdout thresholds, sampling phases, or event definition.

## Falsifiers and success criteria

- If only broad blink-event intervals are available, report that they cannot validate the E002-371 fully-closed interval hypothesis, even if event visibility is 100%.
- If valid fully-closed intervals are present, report positive missed native-index witnesses when observed, but never a population risk guarantee from a handful of participants.
- If source download, workbook semantics, index origin, frame count, or participant disjointness is ambiguous, abstain with the exact failure reason. No silent column-guessing or synthetic substitution.
- Independent implementation must reproduce the integer phase coverage results.
- No human-image uploads, no reidentification, no assertion that native frame labels authenticate camera exposure or hard eyelid speed.

## Product decision

Until synchronized optical shutter/clock calibration, independent anatomical adjudication, hard velocity bounds, and held-out physical tests exist: `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. E002-604's ideal shutter integration counterexample remains conditional. This protocol is intended to find **genuine independent human-label evidence** or a documented fail-closed limitation, not to declare a product ready.