# E002-606 | True 30-fps rational-rate phase mismatch: frozen predictions reproduced

Date: 2026-11-02. Parent E002-371; existing research branch. **Evidence tier: EXACT SYNTHETIC IDEAL POINT-SAMPLING ONLY.** [Frozen protocol](E002_606_FROZEN.md) committed first at d3cf682 before code or execution.

## E002-605 hosted result recovered, not misrepresented

[GitHub Actions run 41398694048](https://github.com/sushxnthd/lucent/actions/runs/41398694048) completed **successfully**: eight Python tests and 500 independent JavaScript integer checks passed. But the actual public annotation download attempt returned **HTTP 401 Unauthorized** at 2026-11-02 06:19 UTC; source_access=ABSTAIN and recognized_events=0. No real human annotation was read. The provider's [current API documentation](https://data.mendeley.com/api/docs/) requires bearer-token authentication; the [public dataset landing page](https://data.mendeley.com/datasets/9yzdnng594/1) advertises the workbook but does not expose a usable direct per-file download URL in its static text. Do not bypass authentication. Stop repetitive source-access probing; obtain the workbook through authorized browser/manual access or pursue independent blinded human raters.

## New preregistered falsification of a tempting E002-605 interpretation

E002-605's exact three-phase 3:1 index decimation **does not equal a 30-fps acquisition** when native recordings are reported as 100–110 fps: it is 33.333 or 36.667 nominal samples per second. We froze a hypothetical piecewise-constant closed pulse of m native bins, instantaneous 30-fps point samples, and uniformly random low-camera phase. The idealized phase-miss fraction is max(0, 1 - 30m/f_H), and the 3:1 index miss fraction is max(0, 3-m)/3.

| Source Hz | Closed native bins | True ideal 30-fps phase miss | 3:1 index phase miss |
|---|---:|---:|---:|
| 100 | 1 | 7/10 | 2/3 |
| 100 | 2 | 2/5 | 1/3 |
| 100 | 3 | **1/10** | **0** |
| 100 | 4 | 0 | 0 |
| 110 | 1 | 8/11 | 2/3 |
| 110 | 2 | **5/11** | **1/3** |
| 110 | 3 | **2/11** | **0** |
| 110 | 4 | 0 | 0 |

The preregistered m=3 predictions were met: even when all three native frame bins are hypothetically fully closed, a 30-fps point camera can miss them for 10% (100 Hz) or 18.18% (110 Hz) of phases, while 3:1 index decimation reports zero misses. This is a **model counterexample**, not a measured human blink miss fraction.

The [Python executable](e002_606_rate_alias.py) uses exact Fraction arithmetic and independently enumerates phases on an integer lcm clock lattice; [five adversarial unit tests](test_e002_606_rate_alias.py) passed locally. A separate [Node.js finite-grid enumerator](e002_606_independent.js) passed all eight rate-duration cases locally without invoking the Python code. [Dedicated hosted CI](../../.github/workflows/e002_606_rate_alias.yml) was committed; hosted success was unverified at report time. All inputs are synthetic, with no subject-level labels or images.

## Interpretation and allowed claims

This correction is **not** a new physiological law. It is an exact sampling-rate mismatch in a proposed validation assay. Native frame labels do not establish closure over entire bins; actual video exposure integrates light and may roll scanlines, and nominal codec FPS does not authenticate the sensor clock. E002-605 remains valid *only* as a native-index assay and must not be relabeled as a 30-fps shutter experiment.

A valid held-out physical prediction requires: (1) independent anatomical closed/open intervals, (2) measured optical exposure start/end and clock uncertainty, (3) independent continuous-time eyelid speed ceilings or explicit abstention, and (4) participant-disjoint predeclared nuisance controls and blinded adjudication. Existing [E002-598 human study protocol](E002_598_HUMAN_STUDY.md) remains the field protocol. Do not expand synthetic theorem polishing in place of recruiting raters and capturing calibrated human footage.

**Human closure measurements:** 0. **Authenticated physical shutter captures:** 0. **Certified physiological velocity ceilings:** 0. **Held-out physical predictions:** 0.

**Lucent product:** ABSTAIN_UNCALIBRATED; **release:** BLOCKED. Hush PR #45 unchanged.
