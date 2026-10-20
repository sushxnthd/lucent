# E002-315 — Dual-edge common-mode observability and differential-gain impossibility

## Conditional image formation
For upper/lower eyelid edge positions `s_U(t)=a u(t)+b(t)`, `s_L(t)=a(u(t)+h(t))+b(t)`, constant scale `a>0` during exposure, common displacement `b(t)`, normalized PSF `K` and positive temporal contrast weights `w_j(t)`, let
`p_j=K * Law_{w_j}(s_j(t))` be the complete, sign-corrected, normalized image derivative. Write `c_j=mean(p_j)` and `k=mean(K)`. Then `c_j=k+E_{w_j}s_j`.

If `w_U=w_L=w` and `K` is shared, **the differential centroid is an invariant**:
`c_L-c_U=a E_w h(t)`.
Arbitrary shared gaze/head displacement, including during exposure, and any shared PSF shape/centroid cancel. With same-exposure canthal width `D=a d_0`, `Z=(c_L-c_U)/D=E_w(h/d_0)`. Only for constant temporal contrast does this equal the unweighted anatomical shutter mean. Cropping, spatially varying reflectance, separate PSFs, rolling shutter and changing scale violate assumptions.

## Sharp failure law
Restrict to constant anatomical aperture `h(t)=h_0` within exposure. Let common projected motion `G(t)=a u(t)+b(t)` have excursion `DeltaG=sup G-inf G`. Assume each edge has independent temporal contrast weights `m<=w_U,w_L<=M`, `r=m/M`. Then
`A_obs=c_L-c_U=a h_0 + E_{w_L}G-E_{w_U}G`, with the **sharp** bound
`|A_obs-a h_0| <= DeltaG (1-r)/(1+r)`.
Proof: for a temporal subset of measure `p`, the largest weighted probability difference is `p/[p+r(1-p)] - rp/[rp+1-p]`, maximized at `p=1/2`, giving total-variation bound `(1-r)/(1+r)`. A bounded `G` multiplies that TV. Equality is attained with equal-duration two-level `G` and opposite extreme weights. Smooth approximations approach equality.

For two independent exposures with constant aperture in each, no other errors, and a common excursion bound, a strictly positive anatomical aperture change is certified **iff**
`delta_obs > 2 DeltaG (1-r)/(1+r)`.
Equivalently `r > (2 DeltaG-delta_obs)/(2 DeltaG+delta_obs)` when `0<delta_obs<2 DeltaG`. Equality requires abstention.

Frozen hypothetical example: `delta_obs=.06`, `DeltaG=.25`, `r_critical=11/14=.785714...`. At `r=.75`, maximal false change is `.0714286` (abstain). At `r=.85`, it is `.0405405` (certify). These are synthetic instrument parameters, not measured RGB calibration.

Exact rational counterexample: with `r=1/2`, equal-duration common displacement `G=(0,1)`, upper gains `(1,1/2)` and lower gains `(1/2,1)`, constant true aperture, the apparent aperture has bias exactly `1/3`. The complete images can be noise-free and fully captured while differential temporal illumination creates this false anatomical signal.

**Scope:** The sharp bound is for constant within-exposure aperture and independently bounded per-edge gains. For time-varying aperture, weighted anatomical selection adds uncertainty; no general sharp claim is made. Additional PSF/centroid/scale/crop errors require independently calibrated additive bounds. Does not recover pupil radius, event ordering, blink velocity, or fatigue state.
