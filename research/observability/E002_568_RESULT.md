# E002-568 RESULT | Human-cohort speed evidence rules out universal closure-exclusion claims across two missing 30-Hz frames

Date: 2026-10-31. Primary E002-371 kernel; existing research branch and draft PR #26. [Frozen protocol](E002_568_FROZEN.md) was committed at \`925608f\` before the executable. **Evidence tier: exact product consequence of E002-371 and Kwon et al.'s published 2013 cohort means, not a new human measurement or independently calibrated camera.**

## Prediction and outcome

E002-564 established, using Kwon et al.'s same-cohort reported mean peak closing speed 243 mm/s and mean initial palpebral aperture 9.83 mm, that a *single universal normalized upper speed ceiling for all 25 measured participants* cannot be strictly below \`v0=24300/983 = 24.720244... s^-1\` under the published point estimates and definitions. This is a **necessary floor for a universal upper bound**, not a safe speed upper bound. It is not a general population guarantee.

For ideal exact, fully open endpoints, E002-371's sharp condition permits a positive-duration hidden threshold closure whenever \`V H > 2(1-theta)\`. At \`theta=0.2\`, the exact critical gap based on the necessary cohort floor is:

\`Hcrit = 2(1-0.2)/(24300/983) = 1966/30375 s = 64.724279835... ms\`.

If an authenticated blind gap exceeds this threshold, a positive-duration hidden closure is feasible in the ideal Lipschitz model **for every universal ceiling V >= v0**. At equality a threshold touch is feasible. This is a structural *non-certifiability* result, **not** evidence that any human closure actually occurred, nor proof that every individual could execute the extremal trajectory.

Frozen hypothetical 30-Hz global-shutter camera with 10-ms exposures; \`k\` counts consecutive missing exposure opportunities:

| Missing opportunities k | Ideal blind gap H | H relative to 64.724 ms | Consequence of cohort witness |
|---:|---:|---|---|
| 0 | 23.333 ms | Below | No no-go established by this necessary-speed argument; still no certificate |
| 1 | 56.667 ms | Below | No no-go established; still no certificate |
| 2 | 90.000 ms | Above | Positive-duration hidden closure feasible for any cohort-applicable universal ceiling |
| 3 | 123.333 ms | Above | Same structural no-go |

A deliberately **incorrect** policy would treat the published \`v0\` as a safe physiological upper bound and issue an EXCLUDE for k=0 or k=1. The executable never does so. It emits \`ABSTAIN_UNCALIBRATED\` for every case, including k=0/1. Even k=2/3 do not imply an observed blink.

## Timing uncertainty, nuisance, and falsification

The independent uncertainty model takes period interval \`[Fmin,Fmax]\`, shutter interval \`[wmin,wmax]\`, missed opportunities \`k\`, and endpoint clock error \`e\`:

\`Hmin=max(0,(k+1)Fmin-wmax-2e)\`, \`Hmax=(k+1)Fmax-wmin+2e\`.

At k=2 with 1-ms endpoint uncertainty, the minimum gap remains 88 ms, so the no-go survives. With 15-ms uncertainty per endpoint, the gap range becomes [60,120] ms, straddling the critical boundary; the algorithm refuses to classify the no-go as robust across all admissible timings. These are hypothetical instrument parameters, not measured shutter or clock errors.

The ideal exact endpoint observation is strictly stronger than a real exposure-average RGB measurement. Thus missing frames and plausible geometry/brightness/blur/gaze/glasses nuisances cannot *restore* a deterministic no-closure guarantee under this insufficient model; however the argument does **not** certify that a real camera implements the idealized gap model. Rolling shutter, overlapping exposure, and unverified missing-frame counts are outside the executable's global-shutter assumptions and require abstention.

## Verification

- [Exact rational Python executable](e002_568_cohort_dropout.py) and [12 adversarial unit tests](test_e002_568_cohort_dropout.py): **12/12 passed locally**, including all frozen missing-frame cases, equality/touch, uncertainty straddling, malformed input, monotonicity, and universal product abstention.
- [Independent Node BigInt replay](e002_568_independent_replay.cjs): **13 exact assertions passed locally** using separately implemented rational operations.
- [Dedicated hosted CI](../../.github/workflows/e002_568_cohort_dropout.yml) committed on the same existing branch; **hosted outcome not yet verified**. Do not claim hosted success until job logs are inspected.
- No original human participant trajectories, optical hardware captures, or blinded anatomical annotations were obtained. The study design remains [E002-567](E002_567_PHYSICAL_HUMAN_STUDY.md).

## Product consequence and limitations

A generic "30 fps is sufficient" or "two dropped frames do not matter" assertion cannot support a universal absence-of-closure certificate under the cohort-applicable speed model, even with ideal exact open endpoints. This is an **impossibility warning** for a particular conditional model, not a newly established universal physiological law or independent replication. For future participants, the Kwon cohort floor does not substitute for their speed evidence. At shorter gaps, the absence of a hard independently validated upper bound remains decisive: no certification.

Current independent human anatomical rater pairs **0**; authenticated physical shutter captures **0**; certified continuous-time human speed upper bounds **0**; held-out physical closure predictions **0**. Product \`ABSTAIN_UNCALIBRATED\`; release \`BLOCKED\`. No changes to the Hush branch. The next real evidence must be independently blinded S01 annotation and original synchronized optical shutter/clock acquisition, not another synthetic kinematic theorem.
