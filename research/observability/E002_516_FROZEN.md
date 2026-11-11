# E002-516 | Preregistered primary-literature velocity-cap eligibility audit

Date: 2026-10-29. Primary E002-371 research branch; draft PR #26. This protocol is frozen before writing the source-comparison result. It is a **literature-priority and product-claim falsification**, not another S01 metadata pass or synthetic clock sweep.

## Question and independent criteria

Can published human eyelid peak-velocity observations, including high-speed videos, justify the deterministic *continuous-time, normalized-aperture* speed cap required by E002-371 for an unobserved interval on an unseen participant and device?

A source is eligible as a hard-cap certificate **only** if it establishes all of: (i) a mathematically guaranteed upper bound on absolute continuous-time aperture velocity over the intended population/condition, not an observed sample maximum or mean; (ii) an independently calibrated timebase and shutter; (iii) a mapping from physical eyelid displacement to the exact scalar aperture and geometry used by the theorem, with positive denominator uncertainty; (iv) worst-case treatment of unobserved between-frame extrema, gaze, voluntary/reflex/spontaneous blink type and subject variation; and (v) independently replicable evidence. Mere acquisition at 240/600/1000 fps is insufficient.

## Frozen decisions

- If papers only report finite-sample speeds or averages, **reject** the inference "published maximum = certified hard bound"; retain papers as pilot priors and test-design constraints, not a release gate.
- If papers establish high-speed optical or coil feasibility but do not supply publicly auditable frame-level timing and source labels, they may guide a physical study but do not authenticate S01.
- Compare units without conflating mm/s, angular velocity and dimensionless 1/s. Normalized speed is physical speed divided by the independently measured scale in mm only when the scalar observable matches that displacement geometry.
- Any primary paper demonstrating dependence on gaze, subject or blink type requires explicit nuisance strata; no single population-wide speed claim from a small cohort.
- Distinguish prior art (high-speed blink kinematics and LED/rolling-shutter calibration) from the narrower proposed contribution (sharp conditional observability/abstention law and physically validated boundary).
- Do not change E002-515's frozen optical replay or fit speed limits after held-out labels. No physical or human measurements are invented.

## Kill criterion and output

If no eligible hard-cap source exists, the deterministic "no hidden closure" product claim remains **BLOCKED**; keep `ABSTAIN_UNCALIBRATED`. The defensible scientific path is to independently calibrate the camera, obtain genuine blinded anatomical measurements and evaluate *conditional* certificates or explicitly statistical population risks, with participant-disjoint testing and measured coverage. Record any negative priority finding, DOI links, scope limitations and what observation would reverse the decision.

Hush remains untouched on this primary run.
