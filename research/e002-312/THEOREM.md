# E002-312: exact full-image temporal gauge

## Instrument equation
For global shutter [0,T], monotone eyelid edge s(t), spatially uniform temporally varying contrast w(t)>0 and known fixed PSF, the complete continuous normalized image is
I(x)=B+C*[integral_0^T w(t) Phi((x-s(t))/sigma)dt]/[integral_0^T w(t)dt].
It is not merely the scalar 50% edge crossing.

## Theorem 1: temporal-reparameterization gauge
For any increasing differentiable bijection h:[0,T]->[0,T] fixing both endpoints, s_h(t)=s(h(t)), w_h(t)=w(h(t))*h'(t) gives exactly the same full image for every x and any fixed PSF by substitution u=h(t). Boundedness and positivity of the transformed gain must be checked; the explicit examples below meet them.

## Theorem 2: sharp monotone event-time interval
Let Q(a) be the spatial occupation CDF identified from a noiseless complete image with known injective PSF, q=Q(a), and r=m/M for m<=w(t)<=M. The event time t_a=s^{-1}(a) satisfies
T*r*q/(1-q+r*q) <= t_a <= T*q/(r*(1-q)+q).
Proof: at z=t_a/T, the weighted pre-event fraction q lies between r*z/(r*z+1-z) and z/(z+r*(1-z)). Inversion yields the interval. Bang-bang gains attain both bounds. This remains sharp conditioned on the entire image: for any admissible w, set W(t)=integral_0^t w and s(t)=Q^{-1}(W(t)/W(T)); all these trajectories induce the same Q and hence the same complete blurred image. Additional speed/acceleration constraints can narrow the interval. For r=1, t_a=T*q; as r->0, the interval approaches [0,T] for interior q.

## Smooth finite-speed exact collision
Let z=t/T and D>0.
w_A(z)=1-z/2; s_A(z)=D*(4z-z^2)/3.
w_B(z)=1/2+z/2; s_B(z)=D*(2z+z^2)/3.
Both gains lie in [0.5,1], have equal integrated brightness 3T/4, and induce the same uniform spatial occupation distribution [0,D], so even the full raw image is identical under every fixed PSF. Speeds are in [2D/(3T),4D/(3T)]. For the event s=D/2, t_A/T=2-sqrt(5/2), t_B/T=sqrt(5/2)-1, difference (2sqrt(5/2)-3)T. Their midpoint edge positions differ by D/6. This is a smooth exact counterexample, not a human observation.

## Corollary: constant-brightness blink-peak nonidentifiability
Let a_tau(t) increase linearly 0->A by time tau and decrease linearly A->0 by time T. Its time-occupation density is T/A uniformly on [0,A], independent of tau. Hence every pixel integral of any instantaneous image function F_x(a_tau(t)) is identical for all tau. Even constant brightness, full spatial images and identical exposure endpoints cannot recover peak timing. If |a'(t)|<=L, the sharp peak-time interval within this triangular family is [A/L,T-A/L] if LT>=2A; if LT<2A no complete such triangular excursion fits.

## Scope
Conditional global-shutter single-exposure impossibilities only. Rolling shutter, time-resolved illumination, independent motion cues, gaze, glasses, unknown PSF, noisy finite pixels and anatomical fatigue inference are not covered. Temporal ordering loss in motion blur has primary prior art; field novelty and synchronized human RGB/reference validation remain unestablished.
