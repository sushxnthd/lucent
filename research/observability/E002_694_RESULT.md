# E002-694 — Exposure-mean-aware conditional shutter-gap certificate

**Evidence tier:** exact-rational synthetic verification; no human or physical acquisition.

## Frozen decision and mathematical justification

Let a scalar anatomical aperture x(t) be V-Lipschitz over both exposure windows and the intervening gap. Assume the *ideal calibrated* sensor returns exact exposure means m0 on [-T,0] and m1 on [h,h+T], with exposure length T and blind gap h. For any t in [-T,0], x(0) >= x(t)-V(0-t); integration gives x(0) >= m0-VT/2. Similarly x(h) >= m1-VT/2. The Lipschitz cones from both gap boundaries yield, for every t in [0,h], x(t) >= max(m0-VT/2-Vt, m1-VT/2-V(h-t)). Consequently x(t) >= (m0+m1-V(T+h))/2. **Only when this lower bound strictly exceeds closure threshold c** may a hidden closure be excluded under these assumptions. This bound is conservative, not claimed jointly sharp under integral constraints.

A naive rule treating m0,m1 as instantaneous endpoints uses (m0+m1-Vh)/2 and can issue false certificates. For uncertain means m_i in [l_i,u_i], substitute lower limits l_i; for differing exposure durations use V(T0+T1)/2 in the numerator before dividing by 2. Timing uncertainty requires upper exposure and gap bounds. This derivation does not validate that pixel brightness is anatomical aperture, nor that V is a physiological ceiling.

## Executed synthetic falsification

Run `python research/observability/e002_694_exposure_mean_certificate.py` (Python standard library). Enumerate all 9^5 quantized five-node trajectories, retain 3,611 satisfying |slope|<=1, integrate the two exposure windows exactly using rational trapezoids (T=1/4, h=1/2, c=1/4), and compare both rules against the exact minimum on the *gap only*. Robust rule: **1,101 certificates, 0 false exclusions**. Naive rule: **1,724 certificates, 48 false exclusions**. Example witness nodes at [-1/4,0,1/4,1/2,3/4] with apertures [1/8,1/4,1/2,3/4,1] have m0=3/16 and m1=7/8; naive excludes a closure despite true gap minimum 1/4. Counts are properties of this enumerated synthetic grid, not human frequencies.

## Enforcement and release gate

This repairs the specific unsafe inference identified in E002-693 *conditionally*: exposure averages must not be fed directly to instantaneous-endpoint rules. In a physically calibrated aperture instrument, an exposure-mean-aware conservative certificate could be evaluated, subject to independent shutter timing, integration calibration, upper velocity ceiling and uncertainty intervals. A consumer phone pixel/ML landmark output has **none** of those guarantees by default. Therefore current product remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. E002-690 synchronized physical instrument and participant-disjoint human acquisition are still decisive. No independent replay or external validation was performed.
