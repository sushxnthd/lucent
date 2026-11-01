# E002-591 | Frozen positive-duration closure observability and anatomical-certificate protocol

Date: 2026-11-01 UTC. Primary kernel: E002-371. Parent: E002-590. **Evidence tier: exact idealized measurement-model mathematics plus synthetic validation; no new human or physical camera data.** This is one bounded extension addressing a scientifically distinct endpoint: a sustained, nonzero-duration partial closure, rather than an instantaneous exact zero.

## Preregistered question
Let a:[0,1]->[0,1] be absolutely continuous, a(0)=a(1)=c, |a'|<=L almost everywhere, 0<=tau<c<1, and an unknown interval of length d in (0,1) have a(u)<=tau throughout. An ideal full-duty linearly integrating sensor observes Y=int_0^1 a(u)du. The no-closure control is a_open(u)=c, Y=c. For which dimensionless speeds L can a sustained threshold closure be hidden with exactly the same mean as the constant control? Require a sharp **existence/nonexistence** boundary, including an impossible regime for any finite L. All endpoints, exposure integration and tau are exact in this narrow model.

## Frozen analytic prediction
Set S=1-d and C=tau+(1-tau)*S. Closure is feasible only if L*S>=2*(c-tau). Its maximal possible full-frame mean is

- M_d(L)=tau+L*S^2/4 if L*S<=2*(1-tau);
- M_d(L)=tau+(1-tau)*S-(1-tau)^2/L if L*S>=2*(1-tau).

The sharp alias threshold is

- Lcrit=4*(c-tau)/S^2 if c-tau <= (1-tau)*S/2;
- Lcrit=(1-tau)^2/[C-c] if (1-tau)*S/2 < c-tau < (1-tau)*S;
- Lcrit=INFINITY if c>=C.

At L=Lcrit finite, construct an exact equal-mean witness by taking the E002-590 speed-sharp extremal for b=(a-tau)/(1-tau) over compressed outside time S and inserting a dwell a=tau of duration d at its zero. At any larger L, the threshold witness remains admissible. Below threshold, the maximum mean is <c or the closure is unreachable. At c=C, no finite L permits equality (a limiting speed is not a certificate).

## Frozen rational cases
1. c=1/2,tau=0,d=0: Lcrit=2 (E002-590 reduction).
2. c=1/2,tau=0,d=1/10: Lcrit=5/2.
3. c=1/2,tau=0,d=1/4: Lcrit=4.
4. c=1/2,tau=0,d=1/2: impossible at finite speed.
5. c=1/2,tau=1/10,d=3/10: Lcrit=81/23.
6. c=1/5,tau=0,d=1/10: Lcrit=80/81.
7. c=1/2,tau=1/10,d=3/5: impossible at finite speed.

## Independent adversarial tests
- Exact-rational Python and independently implemented Node BigInt witnesses at finite thresholds: exact endpoints, slope ceiling, sustained dwell length, mean c, and no violations of [0,1].
- Exact-rational one-percent-subcritical exclusion using the analytic upper bound, not an empirical optimizer; independent numerical discretized LP sanity check if SciPy available.
- Reject invalid c/tau/d/L, finite-speed claims at impossible cap, and any treatment of a single sample with a<=tau as proof of positive-duration closure.
- For prospective high-rate anatomy, provide a separate one-sided interval certificate: if an independent hard speed bound V and a time-stamped sample has a rigorously upper-bounded aperture u<=tau, then [t-(tau-u)/V,t+(tau-u)/V] is certified <=tau, intersected with the observation domain. Union only overlapping/touching certified intervals; do not fill gaps. Missing independent V, timestamp/geometry provenance or nuisance flags forces abstention. This certificate is model-conditional, not a human velocity calibration.
- No re-download or re-analysis of Silesian5 or LPW this run; those sources already showed index-only omission and an instrument pipeline. No claim that investigator frame labels give continuous dwell, a hard velocity ceiling, or physical shutter integration.

## Product gate
Do not use instantaneous-closure thresholds to certify a positive-duration endpoint or vice versa. Without independently validated anatomy, imaging response, shutter timing, clock, velocity ceiling, geometry and nuisances, return ABSTAIN_UNCALIBRATED; release BLOCKED. Do not advertise physiological or clinical measurement. No PR merge.
