> **PRIORITY CORRECTION (2026-10-28): NOT NEW SCIENCE.** A repository cross-check after implementation found that [E002-421](E002_421_RESULT.md) had already proved **the same exact equal-boxcar boundary** `V*d/[2(m-theta)]` on 2026-10-24, with a stronger independent SciPy linear-program verification and hosted CI. Here `d=T`, `m=b`, and `theta=c`. E002-495 is therefore a **redundant independent exact-rational/Node regression replay**, not a new theorem, novelty claim, or progress toward physical validation. The E002-495 frozen/test artifacts are retained as an honest duplicate-detection record. Do not spend further runs on this law; immediately prioritize E002-492 authentic human annotation handoff and physical timing validation. This correction supersedes any "new measurement-model correction" wording below.\n\n# E002-495 RESULT | Sharp hidden-closure boundary for scalar exposure means

Date: 2026-10-28. Kernel: E002-371. Evidence tier: exact conditional theorem, deterministic synthetic parameter sweep, independently implemented Node numerical replay. **Not** human-anatomical, physical shutter, or camera-timing validation.

## The new measurement-model correction
The original shutter-gap/velocity bound uses independently known **instantaneous** aperture at the ends of the gap. A camera commonly reports an **exposure-integrated** quantity instead. E002-482 showed these cannot be interchanged; E002-495 supplies a sharp replacement law in an idealized scalar model.

Let a(t)>=0 be a continuous V-Lipschitz aperture, with two exact equal scalar exposure means b>c over [-e,0] and [g,g+e]. The gap g=T-e>=0, the period T>0, exposure e>0, and c is a closure threshold. A hidden crossing a(tau)<=c for some tau in [0,g] is **possible if and only if**

    2(b-c) <= V(g+e) = VT,

provided the model has sufficient upper-aperture headroom for the constructed witness. The sharp dimensionless observability number is

    R_avg = VT / [2(b-c)].

R_avg<1 excludes a crossing **only in this exact scalar model**. R_avg>=1 allows two indistinguishable scalar measurements, one from a nonclosing world and one from a crossing world. By contrast the endpoint bound R_endpoint=Vg/[2(b-c)] applies when b is a measured **instantaneous** aperture at both gap endpoints. The gap between these laws is the exposure-duration contribution Ve/2 to the maximum allowable mean deficit.

## Proof, including sharpness
If a(tau)<=c, Lipschitz continuity gives a(t)<=c+V|t-tau|. Since the left exposure precedes tau, its mean obeys b<=c+V(tau+e/2). Since the right exposure follows tau, its mean obeys b<=c+V(g+e/2-tau). Thus

    (b-c)/V <= min(tau+e/2, g+e/2-tau) <= (g+e)/2.

For sufficiency set tau=g/2, m=2(b-c)/(g+e), and

    a_C(t)=c+m|t-tau|.

Both exposure means are exactly b by integration; a_C(tau)=c, and its maximum speed m<=V exactly when the stated inequality holds. The constant world a_N(t)=b has the **same two exposure means** and never crosses c. Both are nonnegative. With a physical maximum aperture A, the particular tent is admissible only if A>=c+m(g/2+e); failing that headroom check is NOT proof that all other crossing trajectories are impossible. A physical upper cap or additional spatial measurements may change the sharp feasible set.

## Frozen falsification and numerical outcome
The preimplementation protocol E002_495_FROZEN.md was committed before the executable. At T=15 ms, e=5 ms, g=10 ms, V=0.1 mm/ms, c=0.1 mm and b=0.7 mm:

- R_endpoint=5/6<1 would **falsely exclude** closure if exposure means were mistaken for instantaneous endpoints.
- R_avg=5/4>1 permits a closing tent with slope 0.08 mm/ms, trough 0.1 mm, endpoint apertures 0.5 mm and exposure means **exactly 0.7 mm** on both sides; peak 0.9 mm.
- A stationary 0.7-mm aperture produces the same two means and never crosses 0.1 mm.
- The strict-exclusion negative control b=0.9 mm has 2(b-c)=1.6 mm>VT=1.5 mm, so no admissible V-Lipschitz crossing exists under the stated means.
- At b=0.85 mm, the sharp equality R_avg=1 permits a crossing.
- At e tending to zero, the two laws converge; a deliberately incorrect initial test expecting a false exclusion in this limit failed locally and was corrected **before commit**. This negative control is preserved in the final tests.

Ten Python adversarial tests passed locally. A deterministic 1,000-case exact-rational sweep yielded **540 mathematically feasible alias configurations, 460 excluded configurations and 279 cases where naive endpoint substitution would falsely exclude**. These numbers describe an arbitrary synthetic parameter distribution, **not a measured human prevalence or algorithm accuracy**. Independent floating-point midpoint quadrature reproduced both frozen exposure means within 1e-10, and a separately written Node implementation reproduced the frozen, exclusion, equality, tiny-exposure and zero-gap cases locally. Hosted verification must be checked independently.

## Scope / decisive limitation
This result applies only to exact, equal, *linear scalar aperture exposure means* with independently valid time and Lipschitz bound. A real camera measures spatial, photometric, potentially nonlinear images; exposure windows, rolling shutter, blur, lighting, glasses, gaze, missing frames, sensor clock and biological eyelid speed remain uncalibrated. Unequal means, finite measurement error, image features and a restrictive physical aperture cap require separate analysis. Do **not** use this theorem to claim that two complete sharp images are identical.

E002-493's authentic S01 motion proxy remains **rejected** under 1-pixel jitter and stride-2 sampling. No authentic human closure labels, independently verified anatomical velocity, physical shutter measurements or held-out human falsification were acquired in E002-495. The existing E002-492 dual-rater protocol remains the immediate empirical handoff; the authentic S01 archive timing remains unauthenticated.

## Product consequence
**Block** any claim that an exposure-averaged feature may be substituted for an instantaneous endpoint in the E002-371 exclusion test. If physical clock, exposure model, geometry, velocity bound, and image formation are not independently calibrated, output ABSTAIN_UNCALIBRATED. No blink-duration, PERCLOS, fatigue, medical or hidden-closure certification is authorized. Release BLOCKED.

## Reproduction
- Frozen: E002_495_FROZEN.md
- Exact solver and sweep: e002_495_exposure_mean_boundary.py
- Adversarial tests: test_e002_495_exposure_mean_boundary.py
- Independent replay: e002_495_independent_replay.cjs
- Reproducible aggregate: E002_495_LOCAL_AGGREGATE.json
- Hosted workflow: .github/workflows/e002_495_exposure_mean_boundary.yml

Scientific novelty relative to primary literature remains **unassessed**; the result must not be described as a new discovery until a priority audit and external review. Existing draft PR #26 remains unmerged, Hush PR #45 separate.
