# E002-168 — Positional pupil-reference schema non-identifiability

**Source-level exact conditional counterexample, not a human physiological result.**

RGBE-Gaze acquisition requests \`ENABLE_SEND_COUNTER=1\`, TIME, TIME_TICK and LPMM/RPMM. Its commented converter example lacks CNT (48 fields), while downstream MATLAB assumes numeric column 2 is seconds and column 42 is left pupil diameter in mm. The enabled counter should make the intended schema 49 fields, with column 2 TIME and column 42 LPMM.

| Synthetic fixture | Fields | Column 2 | Column 42 | Unique matches / 251 frames | Provisional gate |
|---|---:|---|---|---:|---|
| Counter enabled | 49 | TIME | LPMM | 251 | Accept |
| Counter absent | 48 | TIME_TICK | LPMMV | 1 | Reject |
| Counter enabled; missing middle + extra trailing field | 49 | TIME | LPMMV | not evaluated | **False accept** |

The tick example uses illustrative 10 MHz, 50 Hz and 5 seconds. These are **not measured participant data**. The first-record collapse follows from mismatching tick units with seconds in nearest-neighbor matching. This failure is conditional on absent CNT; the official acquisition enables it.

**Exact identifiability boundary:** A 49-field headerless record with a monotonic seconds clock does not uniquely determine the meaning of numeric column 42. Thus field count and clock checks alone cannot certify pupil-mm reference validity. Require named attributes or independently verified schema contracts.

**SCIENCE:** three synthetic tests and an independent XML checker pass; no released CSV inspected, no participant waveform, no device holdout. **PRODUCT:** reject ambiguous positional references; preserve native tracker clocks, pupil validity and named fields. Do not build fatigue inference.

E002-167 GitHub Actions 38454520974 succeeded. This run's CI status must be inspected separately. RGBE-Gaze public GitHub tree has no participant CSV/images; public OneDrive link was inaccessible via web fetch. Switch data path rather than continuing code-only audits.