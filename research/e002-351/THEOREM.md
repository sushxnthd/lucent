# Sharp shutter-kernel transfer law

Active question: Can a frame-decimated high-speed eye video be treated as native low-fps ordinary RGB for rapid blink measurement? **Not without matching exposure kernels and camera nuisances.**

Signal: calibrated RGB dimensionless eyelid aperture or exposure-averaged closure fraction. Reference: independently synchronized high-speed anatomical eyelid video and original frame/exposure timestamps. Scalar reduced model: y_k=alpha+beta*(K_w*c)(t_k)+r_k+e_k, c(t)=1[a(t)<tau]. Full RGB: I_k(x)=Q_k((1/w_k)∫R(x;p(t),a(t),scale(t),gaze(t),lighting(t),glasses(t))dt)+noise. Reduction to scalar y requires independent calibration.

For a V-Lipschitz f and centered box exposures of widths w1,w2 with center offset delta, the exact unrestricted Lipschitz discrepancy is V*W1. Put d=|w1-w2| and c=|delta|. Then W1=c if d=0 or c>=d/2, and W1=d/4+c²/d otherwise. Proof: monotone quantile coupling of uniform shutter kernels and Kantorovich-Rubinstein duality. With equal centers f(t)=V|t| attains Vd/4. A physical [0,1] range may make this conservative.

For a single contiguous binary closure, concentric short and long exposures wS<wL, the maximum long-shutter closure fraction when the short shutter is fully open is (wL-wS)/(2*wL), attained by a blink between the short and long right endpoints. The minimum long-shutter closure fraction when the short shutter is fully closed is wS/wL, attained by closing only over the short exposure. With 2-ms and 20-ms shutters, these are 0.45 and 0.10. A strict native detection threshold q can be exceeded despite an open decimated frame iff q<(wL-wS)/(2*wL).

These are exact **reduced-instrument** results, not impossibility theorems for unrestricted RGB. All high-speed frames can sometimes be re-integrated to emulate native exposure if temporal coverage, spectral response, radiometry and synchronization permit; pure frame selection cannot. Known mathematical foundations, no novel theorem or paired-human result.