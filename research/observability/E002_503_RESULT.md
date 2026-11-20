# E002-503 | Hosted-verified common-mode iris-scale falsification

Date: 2026-10-28. Primary E002-371 kernel. **Synthetic measurement-system counterexample, not human physiology or a new theorem.** Protocol frozen at commit `c47fe47a253756f48af50315f0635412c16a2b1b` before the implementation and execution. The existing E002-492 adjudicator was used unchanged.

## Verified experiment

[Hosted GitHub Actions run 40644763601](https://github.com/sushxnthd/lucent/actions/runs/40644763601) **succeeded** on commit `abcbb8fc091f37f2c51c814517145fd56beee74e`. All **8/8** adversarial test groups passed, including independent exact-Fraction interval arithmetic and the actual E002-492 adjudicator. The committed [executable](e002_503_iris_scale_falsifier.py) produced the frozen predictions exactly.

Two synthetic raters independently represented in the input use identical landmark coordinates and a shared 10% iris-diameter error. Each reviews 260 positions. This simulates a common-mode calibration bias, **not** a measurement of real reviewer errors.

| Prespecified case | Stipulated true aperture | Nominal interval, diameter treated exact | Nominal operational decision | Interval allowing +/-4 px diameter error | Correct conservative decision |
| --- | ---: | ---: | --- | ---: | --- |
| True above c=0.10, d overestimated | 0.105 | [0.093181818, 0.097727273] | BELOW (wrong) | [0.085416667, 0.107500000] | THRESHOLD_UNRESOLVED |
| True below c=0.10, d underestimated | 0.095 | [0.102777778, 0.108333333] | ABOVE (wrong) | [0.092500000, 0.121875000] | THRESHOLD_UNRESOLVED |

**Actual adjudicator outputs:** 260/260 agreement intervals, 0 disagreements and 0 abstentions in **each** synthetic case. The adjudicator itself does not issue threshold labels: the nominal operational decisions above are calculated from its existing aperture-interval convention. Thus even perfect agreement cannot certify the operational threshold side if the shared denominator is biased.

For gap g, per-landmark error e, measured diameter d and independently bounded diameter error delta with 0<=delta<d, the conservative positive-ratio interval is

`[max(0,g-2e)/(d+delta), (g+2e)/(d-delta)]`.

The test independently checked the formula using exact rational arithmetic, invalid denominators, threshold equality and monotone interval expansion. This is elementary uncertainty propagation, not a novel mathematical discovery.

## Scientific and product consequence

E002-492/497's current JSON schema records iris diameter but **no iris-diameter uncertainty**. It therefore cannot justify an aperture-threshold classification from inter-rater interval agreement alone. Retain dual-rater agreement as a **measurement-feasibility** statistic only. For a future physiological study, independently measure the iris reference and its uncertainty, and abstain when the full propagated interval crosses the prespecified threshold. Shared landmark bias, gaze/perspective, blur, glasses, missingness, exposure integration and clock error remain separate unresolved confounds. No retroactive reinterpretation of real human data is made because **zero** independent anatomical ratings exist.

This is a **new falsification of the annotation instrument's threshold-identifiability assumption**, not E002-371 physical validation. The next decisive external step remains two independent blinded S01 anatomical reviews plus authenticated shutter/clock and independently justified continuous-time velocity bounds. Do not continue synthetic measurement refinements instead of acquiring those observations.

**Human anatomical ratings: 0. Authenticated camera/shutter: 0. Certified hard speed bound: 0. Held-out physical predictions: 0. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.** No participant imagery, source frame indices or private ratings committed. Hush branch/PR untouched.
