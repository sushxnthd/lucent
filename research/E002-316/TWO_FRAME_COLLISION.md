# Exact opposite-sign full-video collision (E002-316)

Let P be the exact complete observed profile [1/10,1/5,3/10,3/10,3/10,1/5,1/10]. It admits latent realizations A=(aperture 3, contrast 1/2, PSF uniform width 5) and B=(aperture 5, contrast 3/10, PSF uniform width 3). Both produce P **exactly**.

Construct two complete two-frame RGB videos, both observed as (P,P). Latent video X uses (A,B): anatomical aperture **increases** 3→5. Latent video Y uses (B,A): anatomical aperture **decreases** 5→3. The complete RGB videos are pixelwise identical at both frames, with opposite anatomical aperture-change signs. The same proportional contrast construction works in all three channels. The states are static within each exposure. Smooth interpolation between exposures can be added when temporal gap and velocity bounds permit.

This proves temporal sign is not identified by arbitrary noiseless full-frame estimators over an instrument class allowing independent per-frame contrast and PSF variation. It does not apply if independently calibrated stable contrast or PSF rules out the alternatives. The positive full-support area-ratio invariant and contrast-drift sign boundary remain the candidate conditional remedy. Not human evidence or a novel blind-deconvolution principle.
