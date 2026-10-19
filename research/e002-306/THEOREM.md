# E002-306 — exact conditional pupil arc observability

## Signal and measurement equation
Reference: synchronized independently calibrated anatomical pupil/iris radius ratio q_ref(t). Candidate RGB signal: the visible pupil boundary after calibrated geometry and photometry, represented by sagitta s_hat(t) and chord halfwidth a(t). No qualifying paired human test has been run.

General RGB forward model: Y_nc(u)=Gamma_nc((1/T_n) integral_{W_n} [h_nc * (M_aperture(u,t) {B_c(u,t)+(P_c(u,t)-B_c(u,t)) 1_{D(R(t),g(t),kappa(t))}(u)})]dt + G_nc(u))+epsilon_nc(u).
Nuisances: gaze projection g, differential optical magnification kappa, eyelid aperture M, brightness B/P, optical blur h, glasses glare G, radiometric response Gamma, shutter W/T, sampling/10-Hz retention, and reference clock error.

Reduction REQUIRES independently verified static exposure, circular rectified pupil, calibrated gaze/optics, known chord endpoints, and |edge_error(x)|<=eta. Edge extraction and exposure averaging do not generally commute.

## Exact full-contour minimax theorem
For R>=a>0 define f_R(x)=sqrt(R^2-x^2)-sqrt(R^2-a^2), |x|<=a, and s(R,a)=f_R(0)=R-sqrt(R^2-a^2).
Two candidate radii R1,R2 yield the SAME admissible complete observed contour under independent sup-norm error <=eta iff |s(R1,a)-s(R2,a)|<=2eta.

Proof: for R1<R2, f_R1-f_R2 is nonnegative, symmetric, and decreases with |x| because derivative for x>0 is -x(1/sqrt(R1^2-x^2)-1/sqrt(R2^2-x^2))<0. Therefore sup_x|f_R1-f_R2|=|s(R1,a)-s(R2,a)|. Sup-norm eta balls intersect iff their centers are <=2eta apart; the midpoint is an explicit common observation.

Sharp unbounded-radius boundary: if s(R,a)<=2eta, arbitrarily large R' remain observationally equivalent. With a=R sin(alpha), this occurs for alpha<=acos(1-2eta/R) when 2eta<R; if 2eta>=R, all minor arcs satisfy it.

Sharp fixed-chord relative-change boundary: distinguish R from R(1+q) only when s(R,a)-s(R(1+q),a)>2eta. Equality is NOT distinguishable.

## Synthetic illustrative numbers, not consumer-camera calibration
R=25px, eta=.3px, q=.1: critical half-angle 38.30020125198 degrees; full visible arc 76.60040250396 degrees. Unbounded-radius half-angle 12.57811865578 degrees. At half-angle 30 degrees, radius 25 and 27.5px complete contours are only 0.3442623332px apart, below 2eta=.6px.

Exact rational witnesses: (a,R,s,eta)=(7,25,1,1/2) has unbounded alternative radius. (a,R1,R2,s1,s2,eta)=(15,25,17,5,9,2) has a complete-profile midpoint collision.

## Limits and novelty
Not a universal ordinary-RGB observability theorem: unknown gaze, glasses, radiometry, blur, rolling shutter, unknown chord, noncircular pupil, and timebase invalidate the reduction. Smooth temporal priors cannot resolve a structurally shared observation. The underlying arc-radius ambiguity was already studied in Worring & Smeulders, IEEE TPAMI 1995 (DOI 10.1109/34.387505). Field-level novelty and human validity remain unproven.
