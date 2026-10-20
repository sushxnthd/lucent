# Sharp full-image expectile occupancy bound

Camera model: I(x) = integral w(t) F_x(s(t)) dt / integral w(t) dt, with known fixed optical response F, independently calibrated m <= w <= M and r=m/M. The complete calibrated image identifies the weighted occupation measure nu of edge state s. The unweighted shutter mean of a bounded functional X=phi(s) lies in [L,U], where:

r E_nu[(X-L)_+] = E_nu[(L-X)_+]

E_nu[(X-U)_+] = r E_nu[(U-X)_+].

Proof: h(s)=E_weighted[1/w|s] lies in [1/M,1/m], and theta=E_nu[Xh]/E_nu[h]. Scale h into [r,1]. Optimizing E[(X-c)h] pointwise gives h=1 above c, h=r below c, yielding the upper root. Reverse for the lower root. Bang-bang weights attain the bounds in the unrestricted class.

For uniform nu on [a,b], L=a+(b-a)*sqrt(r)/(1+sqrt(r)), U=a+(b-a)/(1+sqrt(r)). Two uniform occupations shifted by delta with width d have a certifiable increase iff delta>d*(1-sqrt(r))/(1+sqrt(r).

Exact collision: s_A=(4z-z*z)/3, w_A=1-z/2; s_B=(2z+z*z)/3, w_B=(1+z)/2. Both yield the same uniform weighted occupation and identical complete images for all fixed PSFs, but true means 5/9 and 4/9. Assumptions exclude unmeasured gaze motion, missing spatial support, rolling shutter and unknown temporal gain; abstain if calibration fails. This is classical robust expectation mathematics, not a novelty claim.