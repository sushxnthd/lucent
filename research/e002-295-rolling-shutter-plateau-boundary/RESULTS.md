# Executed synthetic results
H=40 px, exposure T=20 ms, row delay tau=20 microseconds: sharp plateau-loss speed = 1923.076923 px/s.
v=1600 px/s: ramp width 33.058 px, each centered plateau margin 3.471 px; width error +/-1 px yields velocity interval [1553.10,1646.81] px/s.
v=3000 px/s: ramp width 63.830 px > ROI, no two-plateau certificate.
Frozen unseen synthetic H=48,T=1/90,tau=14 microseconds: vcrit=4073.627; 3500 passes, 4500 fails.
Exact-rational checker: 401 identical pixels for 3000-vs-4000 collision; 45 inverse equalities; corrupted-contrast mutation rejected.
Independent numerical exposure integration: 80 random configurations, 4001 exposure time samples each; max error 0.00006035 (within midpoint-integration discretization tolerance).
Nuisance stress: geometry shift 2px preserves width; affine brightness naive estimate 1459.4 vs calibrated 1600.9 px/s; missing plateau => abstain; acceleration 150000 px/s^2 causes +179.9 px/s bias; reflection 0.12 intensity causes +690.5 px/s bias. All hypothetical, no human evaluation.
No general rolling-shutter novelty or real RGB observability established.