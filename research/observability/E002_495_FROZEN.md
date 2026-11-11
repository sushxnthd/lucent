# E002-495 | Frozen preimplementation prediction: exposure-mean alias boundary

Date: 2026-10-28. Primary kernel E002-371. This is a **new conditional measurement-model boundary**, not a human validation or camera claim. Frozen before executing the new solver/tests.

## Distinct question
E002-371/E002-486 conditionally exclude hidden threshold crossings using independently known **instantaneous apertures** at the ends of a shutter gap. E002-482 showed scalar exposure averages cannot be substituted for instantaneous values. This experiment derives and attempts to falsify the **sharp replacement boundary** for two adjacent, equal-duration, scalar exposure means.

## Model and prediction
Let frame period T>0, exposure duration 0<e<=T, unexposed gap g=T-e. Exposure windows L=[-e,0] and R=[g,g+e]. Aperture a(t)>=0 is V-Lipschitz (V>0), with threshold c>=0 and two **exact, equal** exposure averages b>c. A hidden crossing means some tau in [0,g] has a(tau)<=c. No gain drift, brightness ambiguity, blur, rolling shutter, dropped frames, gaze effects or unknown camera clock are admitted in this theorem.

**Prediction P1 (sharp):** a crossing is feasible iff 2(b-c)<=V(g+e)=VT, subject to sufficient physical upper-aperture headroom for the witness. Thus R_avg=VT/[2(b-c)] >=1 permits ambiguity; R_avg<1 excludes closure in this ideal scalar model. By contrast R_endpoint=Vg/[2(b-c)] is the correct threshold only when b denotes independently known instantaneous gap-endpoint apertures. The naive substitution of exposure means for endpoints will produce false exclusions when Vg/2 < b-c <= VT/2.

**Prediction P2 (constructive alias):** the nonclosing constant world a_N(t)=b and the closing tent a_C(t)=c+m|t-g/2| with m=2(b-c)/T have identical exposure means b, and the latter reaches c at tau=g/2. The closing tent respects V whenever R_avg>=1 and stays nonnegative. Its peak on the modeled domain is c+m(g/2+e); require an aperture cap above this if a cap is imposed.

**Frozen numerical case:** T=15 ms, e=5 ms, g=10 ms, V=0.1 mm/ms, c=0.1 mm, b=0.7 mm. R_endpoint=5/6 <1 (naive false exclusion), R_avg=5/4 >1 (true exposure-mean alias). Closing witness slope m=0.08 mm/ms, trough c=0.1 mm, exposure means both 0.7 mm; peak 0.9 mm.

**Prediction P3 (sharp failure control):** at b=0.9 mm with other parameters fixed, 2(b-c)=1.6 mm > VT=1.5 mm, so no V-Lipschitz hidden crossing can have both means b. A program that reports a crossing for this case is wrong.

## Tests and falsifiers
1. Independent Python exact-rational calculation of both exposure integrals, peak speed, endpoint values, and dimensionless laws; an independent JS implementation must reproduce the frozen case and strict-exclusion control.
2. Deterministic adversarial sweep of b, e, g, V and c, including equality R_avg=1, vanishingly short exposure, contiguous exposures g=0, and insufficient physical cap. Numerically integrate the constructed tent and compare with the analytic means.
3. Falsify the claim if any admissible counterexample crosses under R_avg<1, if a constructed tent fails to match either mean, or if the result is silently generalized to spatial images, shutter timing of S01, or physiological velocity.

## Evidence / product constraints
The existing authentic S01 result E002-493 killed the motion proxy under 1px registration jitter and stride-2 sampling. Do not revive it. This result is synthetic/exact mathematical measurement science only, not an anatomical closure label or physical camera validation. Product remains ABSTAIN_UNCALIBRATED, release BLOCKED. No human frames, raw imagery, ratings or data are committed. Existing draft PR #26 remains open/unmerged; no force-push.
