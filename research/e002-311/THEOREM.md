# E002-311: exact photometric shutter bias for scalar eyelid-edge crossing

Status: exact conditional mathematical boundary; independently checked on synthetic data. **No ordinary-RGB human validation or field-level novelty.**

For a moving step edge s(t)=s0+vt, uniform shutter [-T/2,T/2], symmetric Gaussian PSF sigma, and time-varying positive contrast m<=w(t)<=M, the plateau-normalized image profile is F(x)=integral w(t)Phi((x-s0-vt)/sigma)dt / integral w(t)dt. Let x50 be the unique crossing F(x50)=1/2. Set r=m/M and k=|v|/sigma. Define G_k(z)=integral_0^z[Phi(k a)-1/2]da.

**Sharp result:** |x50-s0| <= |v|u*, where u* is the unique root in [0,T/2] of rG_k(T/2+u)=G_k(T/2-u). For zero blur, u*=(T/2)(1-r)/(1+r). In the very-large-blur limit, u*=(T/2)(1-sqrt(r))/(1+sqrt(r)). With r=1 the midpoint is invariant; r->0 allows almost half an exposure of scalar timing bias.

Proof: at x=s0+vu, the sign of Phi(k(u-t))-1/2 changes at t=u. Minimizing its w-weighted integral uses w=m for t<u and M for t>u. The minimum is mG_k(T/2+u)-MG_k(T/2-u), strictly increasing in u and zero at u*. The opposite weight pattern attains the negative extreme. Distinct physical midpoints separated by 2|v|u* can produce identical **scalar 50%-crossing values**. Full RGB image equivalence is **not claimed**.

Assumptions: known constant v, symmetric Gaussian blur, visible straight edge and plateaus, spatially uniform gain, symmetric shutter. Does not cover rolling shutter, acceleration, unknown camera gamma, glasses, gaze displacement, pixel noise, spatially nonuniform lighting or human fatigue. E002-310's midpoint invariant survives time-constant affine brightness, but **not arbitrary within-exposure gain**.
