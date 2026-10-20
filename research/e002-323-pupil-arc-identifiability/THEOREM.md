# E002-323: sharp feature-level pupil-arc identification

Assume an exposure-static, projectively rectified minor circular arc with exactly known chord endpoints (-a,0),(a,0), a>0, and midpoint (0,s), 0<s<=a. A measured sagitta shat satisfies |shat-s|<=epsilon, with epsilon independently bounded. The anatomical radius R=(a²+s²)/(2s). This is an idealized reduced feature, NOT an automatically recoverable RGB measurement.

Let lo=max(0,shat-epsilon) and hi=min(a,shat+epsilon). If hi<=0 or lo>hi, the feature is infeasible. Otherwise the exact identified radius interval is [R(a,hi),R(a,lo)], with infinite upper endpoint when lo=0. Proof: dR/ds=(1-a²/s²)/2<=0 for 0<s<=a; every admissible sagitta defines a circle through all three points, so both bounds are sharp. At lo=0 the upper bound diverges as s->0+.

For a true radius R and visible angular span phi<=180 degrees, a=R sin(phi/2), s=R(1-cos(phi/2)). At centered observation shat=s, finite upper radius iff phi>2 acos(1-epsilon/R). For target relative upper radius error <=tau, solve R(a,s-epsilon)/R-1=tau, obtaining cos(phi/2)=(tau R²-tau R epsilon-epsilon²/2)/(tau R²+R epsilon). The transition exists in the minor-arc domain if this cosine lies in [0,1]. For R=20px, epsilon=.2px, tau=.1, transition=51.80323311930823 degrees. At or below 16.219228911988367 degrees the radius upper bound is infinite.

For independently bounded differential optical magnification m in [mmin,mmax] and calibrated iris radius Ri, pupil/iris ratio q is in [Rlow/(mmax Ri), Rhigh/(mmin Ri)]. A strict increase between two frames is certified only if the later lower endpoint exceeds the earlier upper endpoint; equality abstains. Sharpness of combined bounds requires independent attainability of nuisance ranges.

Two distinct static circles with sagittas shat±epsilon yield identical measured three-point features under opposite admissible extraction errors. Their time derivatives are both zero, so a smoothness-only prior does not distinguish them. This is NOT an identical full-RGB-image counterexample.

Full measurement equation:
Y[k,c](x)=ISP[k,c]{(1/Ek) integral(tk,tk+Ek) [K[k,c]*F[c](x; Rp(t),Ri(t),aperture(t),gaze(t),scale(t),illumination(t),glasses(t))] dt}+noise.
Reduction to (a,shat,epsilon) requires independently validated deprojection, feature extraction, exposure timing, iris geometry and optical bounds. Time-varying pupil radius within exposure, unknown clock offset, 10-Hz downsampling, blur and photometric drift invalidate instantaneous interpretations. No field-level novelty is claimed; NIST Hopp (1994) provides strong prior art.