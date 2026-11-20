# E002-619 | Exposure integration makes the boundary-aperture certificate non-identifiable

Status: **analytical counterexample and reproducible synthetic instrument test; no new human or physical data**. 2026-11-03.

## Question and failure mode

E002-618 correctly states a conditional continuous-time travel bound, but the proposed ordinary-camera product cannot substitute *frame-level aperture estimates* for the **instantaneous gap-boundary apertures** required by that theorem. A camera integrates radiance over a nonzero exposure; its output generally does not identify the eyelid position at either exposure endpoint. A high-speed reference may supply endpoint apertures during a scientific experiment, but that does not make them observable to a deployed ordinary camera.

## Constructive non-identifiability counterexample

Consider a simplified calibrated camera whose frame signal is the exposure-average of a scalar eyelid aperture x(t). For each exposure of duration T, construct two nonnegative continuous trajectories:

* World A: x_A(t)=h for the entire exposure.
* World B: x_B(t)=h + d cos(2 pi t/T), with 0<d<h.

Both produce the identical exposure-average h exactly, yet at **both** exposure endpoints the true apertures are h and h+d, respectively. Their instantaneous endpoint velocities differ too. Set the inter-exposure dark gap length G and closure threshold c<h. Between exposures, extend both worlds continuously with admissible piecewise-linear trajectories. Under a fixed velocity ceiling V, a hidden closure is possible iff G >= (x_left-c + x_right-c)/V (assuming endpoints above c). Choose

    2(h-c)/V <= G < 2(h+d-c)/V.

Then world A permits a full closure in the dark gap, while world B forbids one. Both worlds give exactly the same two observed exposure-average values h. The cosine exposure trajectory has speed bound 2*pi*d/T; choose V at least this large, and choose the gap extension accordingly. The result persists with arbitrary deterministic downstream processing of the identical exposure averages.

Concrete witness: h=3 mm, d=0.5 mm, c=1 mm, T=20 ms, V=200 mm/s, G=22 ms. The cosine speed is <=157.080 mm/s. World A's minimum closure round trip is 20 ms, so closure is possible. World B's minimum round trip is 25 ms, so closure is impossible. Both recorded frames average 3 mm. The gap may be embedded between consecutive exposures; the two worlds can have distinct unobserved trajectories in the dark gap.

This is an **idealized scalar radiometric model**, not a proof that every pixel-level optical image is identical: real blur, nonlinearity, illumination and shape may encode additional trajectory information. It is enough to refute any *general* certificate that treats a frame-average aperture as a known boundary aperture without an independently validated inverse model.

## Product consequence: stricter abstention

1. **Do not compute Q from uncalibrated per-frame aperture estimates** and present it as a physical impossibility certificate. If endpoint aperture lower bounds cannot be derived from the full exposure observation under a validated optical model, output `ABSTAIN_ENDPOINT_UNIDENTIFIABLE`.
2. A scientifically valid alternative is to derive a **set-valued endpoint lower bound** from exposure integration plus a defensible velocity ceiling and calibrated measurement errors, then evaluate the most closure-permissive Q. This is not a license to infer a physiological V from the same test data.
3. For a scalar idealized exposure average m over duration T and |x'|<=V, every endpoint obeys x_endpoint >= m - V*T/2 (because |x(t)-x_endpoint|<=V|t-endpoint| and integration yields |m-x_endpoint|<=VT/2). Include image-to-aperture calibration error epsilon by lowering this to m-epsilon-VT/2, clipped at zero. This bound is **sharp** for affine x(t) with slope +/-V, provided the trajectory stays physically admissible. Use independent uncertainties in exposure length, aperture calibration, and clock alignment; never plug in nominal frame period as exposure time.
4. Under the idealized scalar model, for adjacent exposures with means m1,m2, durations T1,T2, and error bounds e1,e2, conservative endpoint bounds are L1=max(0,m1-e1-V*T1/2), L2=max(0,m2-e2-V*T2/2). A hidden closure is ruled out only if V*G_upper < max(0,L1-c)+max(0,L2-c). Equality does not rule it out. A low or zero denominator forces abstention. This is a **conditional sufficient certificate**, not a necessary test and not yet validated for image measurements.

## Testable prediction for physical study

Predeclare the two decision rules (naive Q using frame-average as endpoint; conservative Q using the VT/2 endpoint penalty) and compare against synchronized high-speed ground truth. Sweep independently calibrated shutter duty cycles while keeping nominal fps and frame-average signal fixed. The naive rule should over-certify on constructed endpoint-varying trajectories; the conservative rule should never issue a false no-closure certificate if the idealized scalar measurement, Lipschitz ceiling, and timing bounds all hold. Falsify or withdraw the certificate on a single trusted contradictory ground-truth closure. Report every abstention. Prioritize the physical measurement campaign over additional synthetic polishing.

## Evidence tier

Exact mathematical construction with a numerically checkable witness. No human velocity ceiling, pixel-level optical inversion, camera exposure timing, or clinical measurement has been validated. **Lucent remains ABSTAIN_UNCALIBRATED and production BLOCKED.**
