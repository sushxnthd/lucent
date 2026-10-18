# E002-283: Spatial-gradient observability

A conditional measurement-science result, not a human blink or fatigue claim.

Model: co-exposed, camera-linearized eye patch and four stable control patches. Spatial affine nuisance plus bounded quadratic residual. Define H_i=(baseline_radiance_i,1,x_i,y_i), w=H_eye H_controls^{-1}, M=sum_i w_i (position_i-position_eye)(position_i-position_eye)^T.

Under full rank and independent bounded patch errors epsilon, the exact affine nuisance set-separation threshold is A>2 epsilon (1+||w||_1). With an unrestricted quadratic spatial nuisance whose Hessian spectral norm is bounded by kappa, the exact conditional threshold is A>2 epsilon (1+||w||_1)+kappa||M||_*. Equality is ambiguous. General bounded-Hessian nuisance yields only a sufficient upper envelope, not this exact equality.

Product consequence: do not certify two-reference brightness-ratio blinks when spatial gradients are possible; four stable, texture-diverse, co-exposed controls and independently calibrated nuisance bounds are required for a conditional certification attempt. Abstain otherwise. Human waveform observability remains unresolved.
