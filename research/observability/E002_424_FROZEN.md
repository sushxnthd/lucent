# E002-424 — frozen subphase shutter-alias falsification protocol

**Date:** 2026-10-25. **Status:** hypotheses frozen before implementation/results. **Evidence tier:** synthetic instrument and exact scalar optical models only; no camera, human, photodiode or physiology measurement.

## Question and falsification target

E002-423 passed a held-out interleaved LED pulse-phase test of a fitted boxcar shutter. Is that evidence sufficient to identify the shutter's *within-phase-bin temporal response*? Try to construct two nonnegative, normalized shutters with exactly the same entire E002-423 LED phase-sweep observations, but different temporal weighting of a moving eyelid. This tests an unprobed acquisition nuisance, not a new Lipschitz theorem.

## Frozen conditions

- Two exposures: duration E=2.4 ms, centers c0=0.0 ms and c1=3.2 ms, pulse width p=0.50 ms. Phase sweep s=-3.0 to +7.0 ms at 0.10-ms steps (101 phases); odd phases are held out from the boxcar fit as in E002-423.
- Baseline shutter h0(t)=1/E within [c-E/2,c+E/2] and zero outside. Adversarial shutter h1 is also nonnegative and normalized, but each 0.10-ms cell has two 0.05-ms half-cells. At the first row use h1=(1+alpha)/E then (1-alpha)/E; at the second row reverse that order. Freeze alpha=0.99, so both weights remain positive.
- For a pulse beginning on the 0.10-ms grid with width 0.50 ms, all overlap boundaries are grid aligned. Predict **H1**: for both rows, all 101 exact integrated pulse responses match baseline to numerical tolerance <=1e-11. This includes both training and held-out phases; a fit on either world cannot distinguish shutters.
- Independently integrate a piecewise-linear V-shaped physical aperture a(t)=m+V|t-d/2| with d=3.2 ms, V=0.05 normalized aperture units/ms (a *hypothetical* 50/s hard bound), threshold theta=0.20. Fix the two *observed exposure-weighted* aperture means to 0.281 by choosing m separately in the baseline and adversarial worlds. Predict **H2**: baseline m0=0.201>theta; adversarial m1=0.201-alpha*V*0.10/4=0.1997625<theta; both yield exactly the same two observed aperture means to <=1e-11, satisfy the same hard speed bound and remain physically in [0,1]. Thus applying the boxcar E002-422 certificate to adversarial shutter data would incorrectly certify a no-closure gap.
- **H3 rescue experiment:** keep pulse starts on the original grid but vary the pulse width to 0.45 ms, never used in the original fitting/held-out phase set. Predict a maximal per-row baseline-vs-adversary LED response difference >0.015, demonstrating an available discriminating acquisition experiment without claiming it is universally sufficient.
- **H4 adversarial controls:** verify both shutters are normalized/nonnegative and their full integrated responses are physically valid. Independent midpoint numerical integration must reproduce the exact LED and moving-aperture responses within declared numerical tolerance. Test invalid phase/pulse/row inputs and reject them.
- **H5 product consequence:** no synthetic shutter fit, including zero held-out error, authenticates the real camera response. The only physical decision is `ABSTAIN_UNCALIBRATED`. The counterexample does not establish a general arbitrary-shutter boundary, anatomical measurement or actual human closure.

## Independent verification

Implement exact half-cell integration and a separate numerical quadrature oracle. Freeze H1-H5 and decision thresholds above. Preserve any failed predictions without retroactively changing thresholds. Report phase-grid alias, aperture-world counterexample, rescue response, nuisance limitations, and code/data reproducibility. Add a dedicated CI regression and update existing draft PR #26 only after the scientific files are committed.

## Physical study consequence

Before real-world shutter authorization, independently measure optical pulse shape/phase with photodiode plus external clock, probe randomized **off-grid phases and multiple independently verified pulse widths**, acquire linear RAW row responses at several exposure settings, and bound response-kernel uncertainty rather than reporting only a best-fitting boxcar. Pair this with two blinded anatomical human raters, physical velocity bounds and held-out ordinary-camera predictions. Without these, E002-371 remains physically unvalidated.
