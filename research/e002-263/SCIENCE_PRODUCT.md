# E002-263 SCIENCE / PRODUCT

## SCIENCE — what is true?
For four collinear boundary points (-R,-r,+r,+R) on a single planar concentric model, their cross-ratio C=((R-r)/(R+r))^2 is invariant under any projective transformation of that line. Therefore r/R=(1-sqrt(C))/(1+sqrt(C)). Proof: standard projective invariance, independently verified with 15 exact-rational parameter pairs. This is NOT a novel general observability theorem, NOT a measured human pupil waveform, and NOT valid under arbitrary corneal refraction or incorrect correspondence.

For f(x)=x/(1+kx), naive projected span ratio equals r(1-k²)/(1-k²r²). At r=0.35, k=0.35, it biases by -10.913%, whereas ideal cross-ratio is exact. With 0.5 px endpoint noise and fixed 120 px iris span, 4000 seeded trials yield RMSE 0.007664 (cross ratio) vs 0.038515 (naive). At k=0.8 cross-ratio noise RMSE rises to 0.02394: noise sensitivity is not invariant. A nonprojective cubic warp with arbitrary coefficient 0.10 produces CR estimate 0.318993 rather than 0.35. This coefficient is NOT physiologically calibrated.

## PRODUCT — what capability changes?
Promote four-boundary projective cross-ratio as a **candidate nuisance-resistant observable**, not a deployable measurement. Reject using naive span ratio alone as a geometry certificate. Require explicit boundary order, sufficient pixel separation, consistent iris/pupil boundary pairing, photometric/occlusion quality and out-of-plane/refraction stress testing. Never use cross-ratio to assert absolute millimeter diameter without independent iris size calibration.

The practical go/no-go remains EVE Basler 60Hz visible RGB paired with native-time same-eye Tobii reference, frozen in E002-261. This kernel informs one cheap geometry-only control, not a replacement for prospective human data. Retired detector and fatigue claims remain retired.

## Prior art / collision
- Aguirre, 2019, *A model of the entrance pupil of the human eye*, https://doi.org/10.1038/s41598-019-45827-3 : refraction makes entrance pupil nontrivial.
- Gaze-angle dependency of pupil-size measurements, https://doi.org/10.3758/s13428-021-01657-8 : pupil foreshortening and corneal refraction already known.
- Eye pupil-size artifact across viewing direction, https://pmc.ncbi.nlm.nih.gov/articles/PMC8516786/ : pupil center shifts under refraction.
- EVE DATASET.md Git blob 9b04b892e248c2030168c627357e4cb66c87104a, https://github.com/swook/EVE/blob/master/DATASET.md : Basler synchronized; Logitech timestamps less reliable.
