# E002-510 | Authentic S01 source-timebase experiment

Date: 2026-10-28. E002-371 human-validation kernel, existing branch and draft PR #26.

## What was actually done

Frozen [E002_510_FROZEN.md](E002_510_FROZEN.md) at commit `c9f6542` **before** reading the Phantom XML or sync CSV. Implemented [e002_510_source_timebase.py](e002_510_source_timebase.py) and [12 adversarial synthetic controls](test_e002_510_source_timebase.py). Launched [hosted S01 acquisition and metadata-only verification](../../.github/workflows/e002_510_source_timebase.yml) at commit `4ed0881`, using the previously checksum-pinned authentic S01 archive. The script reads only source metadata, never exports frames, event timestamps, private source indices, raw CSV or XML.

This is a bounded attempt to determine whether the 150-fps acquisition period reported in the primary paper has **source-level timing support** independent of the unreliable AVI nominal header and the rehost's contradictory ~500-fps description. It does **not** authenticate an external clock. The preregistered mapping parser deliberately requires explicit Phantom frame indices and timestamps with units. If the sync CSV lacks these, the experiment must abstain, rather than reinterpret other device clocks.

## Evidence at original commit time (historical, superseded by observed result below)

- Protocol and code persisted on the established branch.
- Hosted authentic S01 outcome: **pending**, not yet a measured cadence or scientific confirmation.
- Synthetic test outcome: **pending hosted execution**. No test pass is asserted here.
- Existing E002-509 participant-level power [hosted CI 40722329284](https://github.com/sushxnthd/lucent/actions/runs/40722329284): **completed successfully**. This verifies its arithmetic/software only, not population risk.
- No human anatomical ratings, independent physical optical clock measurement, exposure calibration, certified continuous-time eyelid-speed upper bound or held-out physical prediction was acquired.

## Hard scientific stop

This is the **final S01 metadata-only experiment**. Even a perfect source timestamp consistency result cannot establish the physical shutter gap or hard human eyelid-speed bound required by E002-371. A failed or ambiguous source mapping is a legitimate negative result; do not tune a parser to make it pass. Subsequent substantive Lucent work must prioritize two real independent blinded S01 reviewers, calibrated optical clock/shutter measurement and participant-disjoint physical predictions. No more nominal-FPS inference or optical image-motion proxy development.

Product: `ABSTAIN_UNCALIBRATED`. Release: `BLOCKED`. Hush PR #45 unchanged; no merge or deployment.


## Observed authentic-source outcome (verified 2026-10-28; replaces the pending status above)

The frozen one-shot workflow **actually completed**: [GitHub Actions run 40729383600](https://github.com/sushxnthd/lucent/actions/runs/40729383600), job `source-clock`, conclusion `success`. The job downloaded the authentic Zenodo S01 ZIP, passed the frozen archive MD5 check, ran the unchanged strict parser, and uploaded the sanitized aggregate [artifact 12833429993](https://github.com/sushxnthd/lucent/actions/runs/40729383600/artifacts/12833429993). The 12 frozen synthetic parser controls passed independently of the source experiment. **CI success means the script executed; it does not mean the physical hypothesis passed.**

Observed aggregate (from the completed job log; no private frame indices or raw participant content):

| Source and check | Observed result | Interpretation |
| --- | --- | --- |
| S01 ZIP | `checksum_pinned_source=true`; one each Phantom AVI, Phantom XML, sync CSV | Correct frozen source, not authenticated camera timing |
| AVI | `avg_frame_rate=1/1`, `r_frame_rate=1/1`, `time_base=1/1`, `frame_count_claim=51252` | Container metadata reports 1 fps; **not** an observed acquisition cadence |
| Sync CSV | `NO_VALID_PHANTOM_FRAME_TIME_MAP` / `AMBIGUOUS_OR_ABSENT_EXPLICIT_COLUMNS` | No unambiguous explicit Phantom frame-index + timestamp-with-units mapping under the frozen parser |
| Phantom XML | `NO_UNAMBIGUOUS_PHANTOM_RATE`, `xml_nominal_fps=null` | No admissible explicitly Phantom-scoped nominal FPS under the frozen rule |
| Physics | `authenticated_physical_clock=false`, `physical_shutter_calibrated=false`, `continuous_time_speed_certified=false` | No physical shutter-gap/velocity certificate |
| Human validation | `human_anatomical_ratings=0`, `heldout_physical_predictions=0` | No anatomical or prospective human evidence |

**Predeclared decision:** `NO_VALID_PHANTOM_FRAME_TIME_MAP`. The S01 metadata experiment **abstains**, and the 150-Hz paper rate must not be substituted for measured shutter/exposure timing. This does **not** falsify the paper's reported camera rate or imply that the camera physically ran at 1 fps. The AVI's 1/1 field, paper's 150 fps and rehost's approximate 500 fps are contradictory *metadata claims*, not independent optical measurements. The frozen CSV/XML rules deliberately reject ambiguous columns rather than search for an interpretation that yields 150 fps.

**Important epistemic distinction:** This is a genuine observation on a checksum-pinned human-source archive, but only of its metadata and file structure. It is **not** a high-rate anatomical label, continuous-time speed measurement, or empirical validation of E002-371. Do not count it toward the completion gate's human-physiology evidence. The one-shot metadata track is now closed; no further schema archaeology or nominal-rate reinterpretation.

**Direct product consequence:** any camera pipeline using only AVI nominal FPS or source paper FPS to certify the E002-371 blind gap must return `ABSTAIN_UNCALIBRATED`. Release remains `BLOCKED`. Next admissible evidence is (a) two genuinely independent blinded S01 anatomical reviews using the frozen E002-507 packet, and (b) independent optical exposure/clock calibration plus physically justified continuous-time eyelid-speed envelope before any participant-disjoint hidden-closure prediction. No new thresholds, windows, or parser heuristics may be selected using this outcome.

Reproduction: the frozen `.github/workflows/e002_510_source_timebase.yml` and `e002_510_source_timebase.py` with archive MD5 `fb56109542a13aa7879778833fe4cbaa`; original job log and sanitized artifact linked above. No source imagery, frame timestamps, or individual indices are published.
