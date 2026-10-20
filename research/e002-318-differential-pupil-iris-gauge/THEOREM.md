# E002-318: A projective pupil invariant with a sharp differential-optics failure boundary

**Status:** Exact conditional mathematical result and synthetic counterexample. NOT validated on human RGB/reference. The positive conic-pencil invariant is already in Wang, Chern & Alexa (2019), https://arxiv.org/abs/1902.04541 .

## Forward measurement family

For camera channel c and frame n, Y[n,c](x) = Gamma[n,c]( integral over exposure t of w[n,c](t) [K[n,c,t] * F[c](H_t^{-1}x; q(t), A(t), ell(t), m(t))] dt ) + e[n,c](x).

q is anatomical pupil radius / iris radius; H is common projective gaze/scale/head geometry; A is eyelid aperture/occlusion; ell is illumination; m is differential apparent pupil-versus-iris magnification from cornea/glasses/noncommon optics; w is shutter weighting; K is blur; Gamma includes gain, white balance, tone mapping and clipping. This is a proposed measurement model family, not a calibrated webcam instrument.

The exact theorem applies only when both boundaries are nondegenerate concentric coplanar circles mapped by ONE invertible homography, in effectively static exposure frames with calibrated conic fitting. It does not automatically apply to ordinary RGB with unknown refraction, cropping or motion blur.

## Theorem 1 (existing projective invariant, not new)

Let Qp=diag(1,1,-rp^2), Qi=diag(1,1,-Ri^2), 0<rp<Ri, and Cp=sp H^{-T}Qp H^{-1}, Ci=si H^{-T}Qi H^{-1}. Then Ci^{-1}Cp is similar to (sp/si)diag(1,1,rp^2/Ri^2). Thus the ratio of distinguished and repeated generalized eigenvalues is (rp/Ri)^2, independent of common projective geometry and arbitrary conic scalings. This is Wang et al.'s 2019 result, not Lucent novelty.

## Theorem 2 (sharp differential-magnification bound)

Suppose the conic invariant measures p_t = m_t q_t, where q_t is anatomical pupil/iris radius ratio and m_t>0 is independently calibrated differential optical magnification. Assume rho <= m1/m0 <= 1/rho, 0<rho<=1. With Q=p1/p0>0:

  rho Q <= q1/q0 <= Q/rho.

Both endpoints are attainable by setting the magnification drift to 1/rho or rho, respectively. Hence an anatomical increase is CERTIFIED exactly when rho Q > 1; decrease is certified exactly when Q/rho < 1; otherwise ABSTAIN. For Q>1 the critical bound is rho_crit=1/Q.

If apparent per-frame conic ratios are independently bounded by p0 in [L0,U0] and p1 in [L1,U1] with L0,L1>0, the conservative interval becomes [rho L1/U0, U1/(rho L0)]. It is sharp if all calibration intervals can be jointly attained.

Frozen hypothetical: p0=0.50,p1=0.53,Q=1.06, rho_crit=50/53=0.9433962264. rho=.94 yields [0.9964,1.1276596], ABSTAIN. rho=.95 yields [1.007,1.1157895], CERTIFY. Neither rho is established for real cameras.

## Theorem 3 (exact opposite-trend full-RGB collision)

Set apparent pupil ratios p0=.50 and p1=.53, rho=.94. World A: q0=.5, m0=1, m1=.94, q1=.53/.94=.563829787... (anatomical increase). World B: q0=.5,m0=1,m1=1/.94,q1=.53*.94=.4982 (anatomical decrease). Both obey the same calibrated drift range and have identical apparent pupil and iris conics at both times. With identical homographies, reflectances, shutter and deterministic RGB rendering, every pixel of the complete images is identical.

This is an impossibility for the stated nuisance class, not evidence that a physical human cornea can attain these exact drifts. Additional independently measured optics may resolve the ambiguity. A perfect repeated-eigenvalue conic-consistency test cannot distinguish the worlds.

## Controls / limitations

1000 randomized projective transformations had max conic-ratio error 4.44e-16. Known affine brightness correction had max error 1.11e-16; clipping caused max unrecoverable error 0.2567. Masking 8.96% of the image concealed differences between pupil ratios .45 and .65 exactly. A smooth pulse visible at 30 Hz was invisible after instantaneous 10-Hz sampling; shutter integration may change that witness. Independent SymPy rational eigenvalue check and 30000 randomized drift-envelope checks passed.

No real RGB segmentation, optical calibration, human reference or untouched holdout has passed. Projective pupil/iris radius-ratio invariance and pupil foreshortening correction have substantial prior art. **Reject** uncalibrated pupil waveform and fatigue certification. **Conditionally investigate** interval-valued pupil/iris change only after independent optics, segmentation, sampling and illumination calibration; otherwise ABSTAIN.