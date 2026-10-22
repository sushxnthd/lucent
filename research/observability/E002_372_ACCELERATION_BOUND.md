# E002-372 acceleration-limited shutter-gap observability

This is a conditional mechanics theorem and independently optimized synthetic result, not human validation.

Let a(t) be normalized eyelid aperture. In an unobserved gap H, assume a(0)=a(H)=1, a'(0)=a'(H)=0, |a'|<=V, |a''|<=A, 0<=a<=1. A closure is a<theta; put L=1-theta.

**Exact contact boundary:**
- If L<=V^2/A, Hcrit=4*sqrt(L/A).
- Otherwise Hcrit=2*L/V+2*V/A.
A hidden threshold touch is possible iff H>=Hcrit; positive-duration strict closure requires H>Hcrit.

**Proof:** The minimum has zero velocity. Each endpoint-to-minimum segment is a rest-to-rest bounded double-integrator transfer. Its optimal control accelerates at A, optionally cruises at V, then decelerates at A. Each leg takes 2*sqrt(L/A) when speed is inactive, or L/V+V/A when speed is active. Two legs are necessary; concatenating them is sufficient. For unequal resting open endpoints, sum the respective one-leg times.

**Dimensionless law:** r=VH/L, s=AH^2/L. If s<=r^2, threshold contact iff s>=16. Otherwise contact iff 2/r+2r/s<=1.

**Frozen synthetic prediction and check:** 30 fps, exposure 10 ms, H=23.333333 ms, theta=.2, V=100/s. Critical A=27272.727/s^2. Independent piecewise-constant-acceleration linear programming (120 steps) yielded minimum apertures 0.33349 at A=20000, 0.20375 at 27000, 0.19072 at 28000, and 0.16681 at 30000, agreeing with predicted transition. At exact threshold discretization yields 0.20013; do not treat this as an empirical margin.

**Literature frontier:** 2013 high-speed 600-fps eyelid kinematics of 25 volunteers, https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/ ; 2019 240-fps smartphone study, https://pubmed.ncbi.nlm.nih.gov/30893187/ ; 2025 segmental eyelid-control study, https://pmc.ncbi.nlm.nih.gov/articles/PMC12358864/ . These reports do not provide universal human upper bounds for V or A. 2026 FaceBase kinematics dataset requires restricted-access approval: https://trackhub.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/ .

**Limitations and falsification:** Zero endpoint velocity is a strong independently testable assumption. A violation of that condition invalidates the new bound, not the speed-only E002-371 law. Camera aperture estimates require geometric, photometric, blur, gaze, glasses, missingness, and clock uncertainty bounds. No human RGB/reference evaluation completed. This is a synthetic instrument validation substitute, not native RGB evidence.

**Product:** Allow only calibrated, interval-valued eyelid evidence with abstention. Reject unconditional rapid pupil reconstruction, exact PERCLOS, and five-second fatigue diagnosis. Frozen human validation protocol is in FROZEN_PROTOCOL_2026-10-22.md.
