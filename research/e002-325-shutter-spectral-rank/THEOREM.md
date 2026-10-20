# Exact measurement theorem and limits

Let x(t)=sum_{k=-K}^K c_k exp(2 pi i k t/T) be a real T-periodic normalized ocular observable. Calibrated shutter measurement y_j=(1/E) integral_{t_j}^{t_j+E} x(t) dt+e_j has matrix A_{j,k}=h_k z_j^k with z_j=exp(2 pi i t_j/T), h_k=sinc(pi k E/T) exp(i pi k E/T).

**Rank law:** If M sample start phases are distinct modulo T and the known exposure duration E is shared, A has full column rank iff M>=2K+1 and h_k !=0 for every included k. Proof: multiply each row by z_j^K and factor out nonzero h_k to obtain a Vandermonde matrix with exponents 0..2K. Distinct nodes yield full rank; M<2K+1 or any h_k=0 gives nullspace.

**Sharp stability law:** For ||e||_2<=eta, least-squares coefficient error <=eta/sigma_min(A), attained along a minimum right-singular direction. For two signals with coefficient separation Delta, worst-direction guaranteed distinction under independent eta noise requires Delta*sigma_min(A)>2eta. At/below this bound there exists an indistinguishable pair in the least-observed direction. This is a universal worst-direction criterion, not an assertion that every specific pair fails.

**Exact alias witness:** At 10 fps, E=.01 seconds, define H(f)=sinc(pi f E)exp(i pi f E), x_f(t)=.5+.03 Re[exp(2 pi i f t)/H(f)]. f=4 Hz and f=-6 Hz have identical exposure-integrated samples at n/10 because frequencies differ by 10 Hz; native trajectories differ and remain in [0,1]. Both are analytic, so smoothness alone cannot resolve the ambiguity.

**Exact shutter-null witness:** A 10-Hz sinusoid integrates to zero over every 100-ms shutter interval.

**Gauge failure:** Real RGB has y_j=g_j(Ac)_j+b_j+e_j after incomplete photometric normalization. If g_j>0 and b_j are uncalibrated per frame, different positive latent sample sequences can yield identical RGB scalars. The rank theorem is conditional on independently verified geometry/photometry/timing and a finite-bandwidth model. No biological bandlimit or human calibration was established.