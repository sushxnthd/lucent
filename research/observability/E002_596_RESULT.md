# E002-596 | Continuous-phase falsification of three-phase 95-to-30 sampling

Date: 2026-11-02. E002-371 primary kernel. [Frozen protocol](E002_596_FROZEN.md) committed first at 091130e. Exact-rational Python and independent JavaScript BigInt implementations agree on the full output locally.

## New result: the E002-595 phase schedule is not exhaustive

E002-595's p=0,1,2 native-frame-offset mappings are individually correct, and their union truly misses native index 9. But nominal 30-Hz sampling of a 95-Hz source admits phases 0 <= p < 95/30 = 19/6, not merely p in {0,1,2}. The fourth integer phase p=3 is valid and samples native indices **[3,6,9,13,16]**. It sees index 9. Thus the four-integer-phase union covers **19/19**, while the original three-phase union covers **18/19**. This **falsifies any interpretation of index 9 as an intrinsic blind index of the 95-to-30 rate conversion**; it does not invalidate the three-phase counts themselves.

The p=3 arm contains **five**, not six, samples inside the fixed 19-native-frame window. Naively assuming equal per-phase opportunity is invalid for truncated windows.

## Exact all-phase law

Enumerate the half-integer nearest-frame boundaries of the map

    i_k(p) = floor(p + 19k/6 + 1/2),  0 <= i_k(p) <= 18,
    0 <= p < 19/6.

All critical phases are the **20** rational endpoints
0, 1/6, 1/3, 1/2, 2/3, 5/6, 1, 7/6, 4/3, 3/2, 5/3, 11/6, 2, 13/6, 7/3, 5/2, 8/3, 17/6, 3, 19/6.

There are **19 distinct point-sampling signatures** across continuous phase. The number of retained frames varies from **5 to 6**. Exhaustive counts of consecutive discrete native-frame pulses wholly missed by an individual phase are:

| Pulse width (native indices) | Best-phase misses | Worst-phase misses | E002-595 p=0,1,2 misses |
|---|---:|---:|---|
| 1 | 13 | 14 | 13,13,13 |
| 2 | 6 | 8 | 7,6,7 |
| 3 | 0 | 2 | 1,1,1 |
| 4 | 0 | 0 | 0,0,0 |

These are finite-grid combinatorial counts, not event probabilities, blink durations, exposure-integrated measurements, or eyelid closure outcomes.

## Verification and study consequence

[Python exact-rational enumerator](e002_596_phase_audit.py) enumerates each rational boundary and each open interval midpoint and tests quarter points for stability. [Independent BigInt oracle](e002_596_independent_replay.cjs) reconstructs all boundaries and mappings without importing Python results. Local comparison of their complete JSON objects, including every phase signature and pulse count, **passed**. Dedicated hosted CI is committed separately; hosted pass must be checked before claiming it.

**Design correction:** Do not promote E002-595's three-phase review as an all-phase study. If independent anatomical review becomes possible, preserve the existing frozen three-arm analysis, add p=3 as a separately declared fourth integer arm with five frames, and report a complete continuous-phase sensitivity analysis. The p=3 frame set reuses existing source images but does not provide independent human or camera observations. Never select a favorable phase after observing labels. Distinguish within-window boundary truncation from physiological non-observability.

**Scientific priority:** This is a protocol falsification, not a novel human blink law. Physical E002-371 validation still requires paired high-speed and ordinary cameras with calibrated exposure timing, response, anatomical geometry, independently justified velocity/acceleration bounds, blinded raters, and prospective held-out predictions.

**Evidence:** Human anatomical rater pairs 0; calibrated physical shutters 0; certified human velocity ceilings 0; held-out physical predictions 0. Product ABSTAIN_UNCALIBRATED; release BLOCKED; draft PR #26 remains unmerged. Hush remains separate.
