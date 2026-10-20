# Lucent E002-322 — directional shutter-gap observability

Conditional mathematical measurement result extending E002-321 to unequal exposures and independently bounded *closing* and *reopening* speeds. This branch is isolated; no product application code was modified.

A frozen synthetic instrument holdout predicts hidden normalized closure H=0.09636240805676727; 9.5% closure can be hidden, while 10% is excluded **only under the stated calibrated scalar model**. A 40-ms dropped-frame extension increases H to 0.19636240805676725. No human ordinary-RGB/reference validation was performed; field-level novelty is unproven.

Run python independent_checker.py (numpy, scipy) to regenerate checks. Read THEOREM.md and FAILED_GATES.md before citing. Model assumes independently verified shutter-mean closure proxy; arbitrary RGB pixels do NOT satisfy that assumption.