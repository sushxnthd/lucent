# E002-364 rolling-shutter ROI support law

For frame period F, rectangular exposure w, and informative eye-row offsets s_i, let I_(n,i)=[nF+s_i,nF+s_i+w]. The largest uncovered cyclic interval is H=max(0,max_i(s_(i+1)-s_i-w),F+s_1-s_m-w), with starts sorted.

Consider two *specified* eyelid-closure histories, equal outside a single fully open gap G, with shared phase and calibrated nonzero rowwise open/closed RGB contrast. In a noiseless, unquantized, nuisance-free instrument, an exact complete-RGB collision exists at some phase if and only if G<=H. For G>H, these two specified histories differ at all phases. This is not arbitrary blink-train recovery.

Let rho_i be the Euclidean norm of the calibrated, nuisance-projected contrast for row i. Let ell_(n,i)(a,G) be the overlap length between gap [a,a+G] and I_(n,i). Define d_min(G)=min_a sqrt(sum_(n,i) rho_i^2 (ell_(n,i)(a,G)/w)^2). With bounded concatenated-video Euclidean measurement error epsilon for each of the two histories, these specified same-phase alternatives are guaranteed distinguishable exactly when d_min(G)>2epsilon. At equality or below, the two closed epsilon-balls intersect at the midpoint. Piecewise-affine overlaps make d_min^2 piecewise quadratic; its global minimum is attained at a breakpoint or an interval's quadratic vertex.

If each row offset has independent error <=u_i and the cyclic row order is preserved, the largest possible uncovered gap is H_robust=max(0,max_cyclic(s_next-s_i-w+u_i+u_next)). Each maximum is attained by choosing earlier-row error -u_i and next-row error +u_next. With one informative row, H=F-w regardless of its common offset error.

Assumptions: fixed rectangular exposure, calibrated row timing and contrast, no saturation, no nuisance cancellation, no unknown differential shutter profile. The positive certificate is for a fixed pair with common outer endpoints and phase, not all physiological histories. Unknown timing and nuisance require recomputing the full observation-orbit distance.

Example: F=33.333 ms, w=10 ms, G=20 ms, three informative rows [0,d/2,d], rho=1, epsilon=.12. Exact local finite-noise crossing d=F-w-G+2sqrt(2)epsilon*w=6.727445883 ms; zero-noise crossing d=3.333333 ms. For d=8, H=15.333333 ms; with independent +/-0.5-ms row timing, H_robust=16.333333 ms. No native-RGB human validation or novelty established.