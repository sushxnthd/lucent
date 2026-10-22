# E002-362 status
2026-10-22. Conditional two-row rolling-shutter alias boundary, synthetic only.
With row delay d+/-u and f1=f0+m/F, gamma=2*pi*max(0,(f1-f0)*d-(f1+f0)*u), D=rho*sqrt(2-2*cos(gamma/2)). Guaranteed binary separation iff D>2*epsilon under calibrated common-row-signal assumptions.
Synthetic 30-fps f0=5Hz f1=35Hz d=1.2ms rho=1 epsilon=.04: u_critical=263.21034us. Independent checker: 200us pass, 400us fail. No human validation, novelty or product clearance. Row-specific unknown phase defeats the guarantee. Full local archive prepared; GitHub source writes may be blocked.
