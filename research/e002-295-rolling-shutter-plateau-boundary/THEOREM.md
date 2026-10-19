# Exact conditional law
Assume a horizontal hard eyelid edge h(t)=h0+v*t, v>0 px/s, linear pixel radiometry, unknown framewise spatially constant baseline A and contrast B>0, row-delay tau, exposure T, and ROI height H. For k=1-v*tau>0, the physically exposure-integrated row profile is
J(y)=A+B*clip(1/2+(k*y-h)/(v*T),0,1).
The two ramp endpoints are y_minus=(h-v*T/2)/k, y_plus=(h+v*T/2)/k; width w=v*T/(1-v*tau).
When BOTH nonempty plateaus lie within ROI (0<y_minus<y_plus<H), ramp width is invariant to A,B,h and velocity is exactly v=w/(T+tau*w).
Sharp plateau-loss transition: v_crit=H/(T+tau*H). For v>=v_crit no placement permits both plateaus; for v<v_crit centering the edge does. This is an existence boundary, not a universal human-camera threshold.
Exact nonidentifiability above transition: H=40,T=1/50,tau=1/50000,v1=3000,v2=4000. Both ramps cover the ROI, with widths 3000/47 and 2000/23. Center them. A1=3/10,B1=2/5; A2=157/690,B2=188/345. For every y in [0,40], J1(y)=J2(y), with all intensities in [0,1]. Thus two distinct speeds yield identical noiseless RGB profiles under admissible unknown photometry.
If ramp-width error <=epsilon_w, velocity interval is [v(max(0,w_obs-epsilon_w)),v(w_obs+epsilon_w)] with v(w)=w/(T+tau*w). Requires independently calibrated epsilon_w.
Restrictions: constant speed, hard edge, spatially affine brightness, known row time/exposure, no acceleration, glare, gaze/head shifts or unknown PSF. No fatigue or mm/s inference. Rolling-shutter inversion and velocity recovery are established prior art.