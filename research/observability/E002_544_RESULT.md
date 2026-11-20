# E002-544 RESULT | Uncorrected shutter-edge scanning produces near-certain false candidates

2026-10-30. Primary E002-371 observability kernel. Protocol frozen in `E002_544_FROZEN.md` at commit `2e1b582` before implementation and synthetic evaluation. Evidence tier: **exact null calculation, seeded synthetic Monte Carlo, and owner-private noncertifying intake code**. Zero physical captures; zero new anatomical ratings.

## The new falsification

E002-543's one-sided per-trial optical edge rule is a candidate generator, not a family-wise error-controlled session decision. Searching 200 independent null flash positions, each with a nominal 5% two-sided noise exceedance probability, gives

```text
P(at least one false candidate) = 1 - (1 - 0.05)^200 = 0.9999649473.
```

This is an **independent-null stress case**, not a measured camera noise law. With dependent positions, the exact value changes. The scientifically relevant unit for this optical sweep is the whole acquisition session, not each frame, pulse or row. Thus treating a single flagged E002-543 trial as session-level evidence would be an unsupported inference.

## Frozen experiment outcomes

Python stdlib PRNG seed `5442026`, 2,000 replications, 39 independent null calibration sessions per replication, 200 positions per session, independent held-out test sessions. All numbers are synthetic.

| Decision under synthetic null | Flagged / 2,000 | Empirical rate |
| --- | ---: | ---: |
| Naive any position exceeds a per-trial 5% threshold | 2,000 | **100.00%** |
| Session-maximum rank p <= 0.05, exchangeable null | 101 | **5.05%** |
| Same rank rule, held-out noise scale 1.25x calibration | 903 | **45.15%** |

The shift failure is the essential adversarial result: a mathematically valid rank calibration is not a license to claim physical error control under changed camera gain, lighting, ISP, sensor temperature, missingness or acquisition regime. It is not an estimate of real camera behavior. The finite Monte Carlo sampling error at 5% with 2,000 replicates is approximately 0.49 percentage points (one standard error); 5.05% is consistent with the exact 5% exchangeable rank guarantee.

## The independent session-wise gate

The separate `e002_544_session_fwer.py` CLI takes owner-private matched null-session paired ROI differences and one held-out outside-flash session, all in one nuisance stratum with the same nonzero number of windows and no missing trials. It computes the maximum absolute difference within each session and the conservative rank p-value

```text
p = (1 + #{null session maxima >= held-out session maximum}) / (m+1).
```

Under exchangeability of all `m+1` session maxima, the probability of a false candidate at level 0.05 is at most 5%, regardless of within-session dependence. Ties make the procedure conservative. With 39 null sessions, the threshold is exactly the top two ranks out of 40; an independent Node.js enumeration confirms 2/40. The program requires at least 19 null sessions, equal trial counts, distinct session IDs, frozen alpha, valid private digest format, matched stratum and explicit owner-asserted E002-543 timing/quality gates. Invalid evidence abstains without dropping trials. It emits no private IDs, residuals or certified physical state.

**Important:** The CLI does **not** verify that null sessions were genuinely independent, that held-out sessions were prospectively sealed, that optical timing was physically authenticated, or that null and test sessions are exchangeable. These are external evidence requirements, not software flags. A `FALSIFICATION_CANDIDATE_FWER` remains an unauthenticated candidate, not a shutter-error finding. No E002-543 frozen threshold is retuned or silently overwritten.

## Verification and direct product consequence

17 Python adversarial tests passed locally. The independent Node.js script tests exact rank/tie arithmetic and exhaustive 40-way held-out relabelling. The reproducible synthetic aggregate is committed as `E002_544_SYNTHETIC_AGGREGATE.json`; dedicated CI runs all three checks. Hosted status must be verified separately.

**Product consequence:** E002-543 single-window candidates must not be promoted into session-level or product-level falsification claims without a predeclared multiple-testing policy and authenticated matched-session null evidence. Even a statistically gated optical result does not certify shutter support or human eyelid closure. The operational state remains `ABSTAIN_UNCALIBRATED`; production remains `BLOCKED`.

**Next physical step:** photodiode-synchronized ordinary-camera acquisition with independent whole-session sham/null controls and randomized held-out outside-edge pulses, including separate nuisance strata and documented drift. Then independently review any flagged raw records and obtain the existing E002-502 two-rater anatomical evidence. Physical captures: **0**; human ratings: **0**; certified continuous-time eyelid bounds: **0**; participant-disjoint predictions: **0**. No new branch, merge, deployment or Hush changes.
