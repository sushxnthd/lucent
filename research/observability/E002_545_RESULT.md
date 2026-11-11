# E002-545 RESULT | Within-session randomization replaces fragile shifted-session calibration

2026-10-30. E002-371 primary kernel. [Frozen protocol](E002_545_FROZEN.md) committed first at `0629f2c`. Evidence tier: **conditional exact randomization proof, seeded synthetic stress, independent implementation, and prospective physical handoff**. No physical camera captures, human eyelid labels or physiological speed ceilings.

## Scientific decision

E002-544's session-maximum rank calibration is distribution-free only under exchangeability between independently collected null sessions and the held-out session. Its 25% noise-scale shift produced 45.15% false candidates in a synthetic stress. A different *experimental design* avoids requiring such between-session exchangeability for a narrower question.

Randomize which of two matched within-session acquisition blocks receives the outside-shutter flash, with a sham in the other block. For each randomized pair, preserve its **entire vector** of K predeclared shutter-edge positions. For the one-sided family-wise statistic

```
D[i,j] = measured_flash_block[i,j] - measured_sham_block[i,j]
T_obs  = max_j sum_i D[i,j]
p      = 2^(-n) * #{s in {-1,+1}^n : max_j sum_i s[i]*D[i,j] >= T_obs}
```

the p-value is superuniform **under the sharp no-flash-effect null**, independent uniform assignment of the two block labels in each pair, and no carryover/interference. Conditional on fixed potential outcomes, each of the 2^n assignment vectors is equally likely, and the observed rank among all assignments has at most alpha mass in the rejection tail. Flipping *whole vectors* preserves all arbitrary correlations across 200 positions. This is standard Fisher randomization inference applied to a shutter-transfer intervention, **not a novel general theorem**.

This does not require equal noise scales across separate calibration sessions, but it **does require** genuine prospective randomized assignment, no carryover, valid outside-exposure pulse timing and stable predeclared analysis. Arbitrary sensor effects that violate the sharp null can cause rejection without implicating the shutter itself. An observed rejection means only an optical-transfer anomaly **candidate**.

## Frozen tests and results

Local Python stdlib adversarial tests: **10/10 passed**. Independent Node.js sign enumeration: **passed**. On an 8-pair, 200-position all-positive synthetic intervention, both implementations return exactly 1/256; with all ties, both return 256/256. Exhaustive 256-way null relabelling of heterogeneous, correlated 8-pair, 5-position potential outcomes produced **11/256** rejections at alpha=0.05, consistent with exact finite-sample control. With only 4 pairs, the minimum p is 1/16, so no alpha=0.05 rejection is possible. The executable enforces 5-16 pairs, <=200 positions, fixed arm lengths, unique IDs, finite responses and owner assertions for timing, quality and carryover; missing or malformed evidence abstains.

A separate seeded 1,000-replication synthetic stress per condition (seed 5452026; eight randomized pairs, 20 correlated positions, heteroskedastic common drift) produced:

| Frozen synthetic condition | Rejections | Rate |
| --- | ---: | ---: |
| Sharp no-flash-effect null | 50/1,000 | **5.0%** |
| Injected +4 response at one predeclared position | 1,000/1,000 | **100.0%** |

The injected effect is intentionally large and is **not** an estimate of physical power or real sensor behavior. The 5% null result is consistent with, but does not independently prove, the conditional randomization theorem. The output is preserved in [E002_545_SYNTHETIC_AGGREGATE.json](E002_545_SYNTHETIC_AGGREGATE.json). Hosted CI is configured; hosted success must be checked separately.

## Falsification and limitations

This method solves one statistical design failure from E002-544, not the physical-measurement problem. It cannot verify that a public randomization manifest was created before seeing data; owner-asserted flags are not cryptographic attestation. The paired acquisition can fail under flash carryover into sham frames, order-dependent ISP state, rolling-shutter row shifts, saturation, autoexposure, motion, uncontrolled exposure timing or sensor gain changes. A single `no_carryover_owner_attested` flag is not scientific evidence of its own truth. No independent photodiode, calibrated shutter, external clock or human anatomical data was acquired. **Physical measurements: 0; independent human ratings: 0; certified human continuous-time velocity/acceleration bounds: 0; participant-disjoint predictions: 0.**

## Product consequence and next experiment

Do not claim a camera shutter error or a hidden blink from a significant optical edge result. Permit only an owner-private `FALSIFICATION_CANDIDATE_RANDOMIZED` if a prospective, authenticated physical protocol and independent replay eventually exist; all other invalid evidence abstains. No consumer-facing change is justified. Product remains `ABSTAIN_UNCALIBRATED`; release remains `BLOCKED`.

**Next decisive experiment:** physical paired flash/sham acquisition with photodiode-authenticated timing, prospective concealed random assignment, 200 frozen edge positions, fixed ROI, nuisance-matched negative controls and blinded independent replay. If a genuine anomaly is found, discriminate shutter support from ISP transfer/illumination leakage before any claim. Then execute the already prepared E002-502 blinded two-rater human study and participant-disjoint velocity-bound prediction. Stop synthetic edge-threshold tuning.
