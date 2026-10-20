# E002-322 — sharp asymmetric exposure-gap law

**Assumptions.** Anatomical normalized eyelid closure c(t) lies in [0,1] and satisfies -D(t-s) <= c(t)-c(s) <= U(t-s) for s<t, where U and D are independent hard speed bounds, not sample-average blink speeds. Two global-shutter exposures occupy [-E0,0] and [G,G+E1]. A calibrated RGB inverse proxy supplies one-sided bounds on exposure means: integral_left(c)/E0 <= m0 and integral_right(c)/E1 <= m1. This is a scalar inverse-instrument theorem, not a theorem about arbitrary RGB images.

Define B(E,V,m) = min(1,sqrt(2*V*E*m)) for m <= V*E/2, and B(E,V,m)=min(1,m+V*E/2) otherwise. Set b0=B(E0,U,m0), b1=B(E1,D,m1).

**Theorem 1 (sharp peak).** For t in [0,G], c(t) <= F(t)=min(1,b0+U*t,b1+D*(G-t)). Therefore

H = max F(t) = min(1, b0+U*G, b1+D*G, (D*b0+U*b1+U*D*G)/(U+D)).

The maximum is attained at t*=clip((b1+D*G-b0)/(U+D),0,G). A threshold crossing is excluded iff theta>H; at equality an isolated crossing may be feasible.

**Theorem 2 (sharp gap occupancy).** For 0<theta<=1, the maximal time in the gap with c(t)>=theta is

Tmax(theta)=max(0, G-max(0,theta-b0)/U-max(0,theta-b1)/D).

This is gap occupancy, not clinical PERCLOS.

**Proof.** An exposure endpoint closure v requires preceding closure at least (v-U*s)_+ for s into the left exposure; its minimal integral is v^2/(2U) if v<=U*E0, or v*E0-U*E0^2/2 otherwise. Inverting the left exposure-mean constraint yields v<=b0. The corresponding right exposure endpoint uses maximal reopening speed D and gives v<=b1. Directional Lipschitz inequalities give the pointwise F(t). The minimum of two opposing affine envelopes and the cap at 1 give H and Tmax. Attainability: set c(t)=F(t) throughout the gap and use minimal ramps c(-s)=(c(0)-U*s)_+ and c(G+s)=(c(G)-D*s)_+ in exposures. This realizes the envelope and obeys both one-sided mean constraints.

**Exact scalar collision.** World A has c=0, observed exposure proxies 0. World B follows the sharp envelope, with true exposure means <=m_i; errors equal negative means. For eta_i=m_i, both produce identical reported zero proxies despite distinct gap peaks. This does NOT prove identical complete RGB images.

**Caveats.** For measured y_i with |error|<=eta_i, m_i=y_i+eta_i is valid only if a separate calibration has proven that the inverse RGB proxy measures shutter-mean c. The formula is sharp for one-sided bounds; it can be conservative when the lower bounds y_i-eta_i are also enforced. Unbounded illumination/gaze/occlusion/clock errors invalidate certification. With U=D=L and equal E,m it reduces to E002-321. The extremal method belongs to classical optimal-recovery theory; general mathematical novelty is not claimed.