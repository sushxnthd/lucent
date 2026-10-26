# E002-457 — directional closure boundary and adversarial shutter validation

**Date:** 2026-10-26. **Evidence:** exact conditional mathematics; independently implemented synthetic numerical falsification; external human two-phase velocity audit queued in CI. **No new physical human anatomical trajectory labels.** [Frozen protocol](E002_457_FROZEN.md) was committed first as 96e639a23e6a4fe299aad1b26029db8d548c46aa.

## Sharp directional boundary

For instantaneous aperture a(t) with -C <= a'(t) <= O, two feasible open endpoints a0,a1>c permit a hidden closure to c exactly when

**Delta >= (a0-c)/C + (a1-c)/O**.

The result is sharp: a descending line of slope -C, an optional dwell at c, and an ascending line of slope +O realize equality and every longer feasible interval. The dimensionless ratio R=Delta/[(a0-c)/C+(a1-c)/O] distinguishes conditional exclusion (R<1) from possible hidden closure (R>=1). This is a standard bounded-control reachability calculation, **not a claim of a novel theorem in control theory**. The scientific contribution for Lucent is explicitly separating closure and reopening speed assumptions, because the independently published human study reports opposite gaze effects on these two phases.

For symmetric C=O=V and equal endpoints with margin m=a-c, critical gap is 2m/V, recovering E002-371. For asymmetric C=300 mm/s, O=200 mm/s, m=1 mm, the sharp critical gap is 8.3333 ms rather than 6.6667 ms for a symmetric V=max(C,O)=300 mm/s assumption. These are **hypothetical hard limits**, not observed physiological maxima.

## Frozen illustrative camera consequence (not human certification)

At nominal 144 fps (6.9444-ms center gap) with hypothetical endpoints 3 mm, threshold 2 mm, C=300, O=200 mm/s:

| Model / nuisance | Critical gap (ms) | Conditional decision |
|---|---:|---|
| Instantaneous directional | 8.3333 | EXCLUDED_CONDITIONALLY |
| Instantaneous symmetric V=300 | 6.6667 | NOT_EXCLUDED |
| Directional, 2-ms uniform symmetric shutter | 7.2917 | EXCLUDED_CONDITIONALLY |
| Directional, 2-ms unknown symmetric-support shutter | 5.8333 | NOT_EXCLUDED |
| Uniform 2-ms shutter plus 0.5-ms error at each endpoint clock | 7.2917; conservative gap 7.9444 | NOT_EXCLUDED |

The shutter rule is conservative, **not sharp**. Uniform symmetric shutter correction is (C+O)e/8; support-only correction is max(C,O)e/2 per endpoint. Exposure response, clock uncertainty, rolling shutter, gaze and geometry can reverse a conditional result. Real hardware calibration and genuine hard directional velocity bounds are absent, so all these rows are only mathematical stress tests.

## Independent numerical falsification

An independent JavaScript implementation, separate from the committed Python analyzer, tested 100,000 randomized exact piecewise-linear closure witnesses with 0 logical inconsistencies. A second independent numerical integration challenge tested **30,000 shutter-averaged piecewise-linear trajectories containing a threshold crossing** with randomized C, O, shutter widths, endpoint measurement uncertainty, and clock error: **0 false conditional exclusions**. A separate set of **10,000 no-crossing negative controls** yielded 10,000 conditional exclusions under a deliberately short gap. These are *synthetic stress tests*, not proof of physiological validity, not independent human data, and not a statistical error bound. The committed Python suite adds analytic equality, asymmetric endpoint, nuisance, source-integrity and shutter controls.

## Human-data and provenance barrier

The dedicated [E002-457 workflow](https://github.com/sushxnthd/lucent/actions/workflows/e002_457_directional_boundary.yml) is designed to hash-verify the same 2,306-blink / 17-participant public Culemann et al. 2026 OSF CSV, now examine its previously unused **opening-velocity magnitudes**, and compare separate C/O calibration maxima on the original participant-disjoint 12/5 split. The source must match SHA256 6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43. **At report creation, the hosted workflow is queued; no opening-velocity numerical results are claimed.** Its output is aggregate-only and cannot certify hard speed limits.

Two targeted public-source searches this run found no unrestricted, acquisition-authenticated high-rate eyelid-margin trajectories ready for this test. The 400-fps 3D FaceBase release is restricted and not-for-profit only; EyeInfo records at 150 fps but raw videos require Google/DVC authorization; 2025 PNAS supplementary videos show 120-fps high-definition recordings but published visualizations cannot be presumed original-time anatomical references. No access controls were bypassed. S19 still needs two human raters; S21/S22 remain sealed.

**Primary-literature priority:** This boundary is elementary bounded-derivative reachability, consistent with established reachable-set/differential-inclusion methods (e.g. Kurzhanski & Varaiya, SIAM J. Control Optim. DOI 10.1137/S0363012903437605). The relevant new *physiological* evidence comes from Culemann et al. 2026, DOI 10.3758/s13428-026-02984-4, whose gaze effects differ for closing and opening. Do not call the mathematics a new general theorem.

## Scientific decision / release

The symmetric maximum-speed model is **not sharp** when independently valid directional caps differ; shutter/clock uncertainty can erase the gain. Until independent anatomical human reference trajectories and physically justified C/O bounds are available, **E002-371 remains NOT_PHYSICALLY_VALIDATED**. Lucent must not issue physical hidden-closure, blink-duration, PERCLOS, fatigue or medical claims. Product remains ABSTAIN_UNCALIBRATED; PR #26 draft/unmerged; Hush branch/PR #45 untouched.

Reproduce: python -m unittest -v test_e002_457_directional_boundary.py; python e002_457_directional_boundary.py --csv /authorized/Blinks.csv --out /tmp/E002_457_AGGREGATE.json. The latter fails on checksum mismatch and writes only deidentified aggregate.
