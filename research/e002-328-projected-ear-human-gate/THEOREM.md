# Sharp projected six-landmark EAR uncertainty bound

Let six measured 2D landmarks be p_hat_1,...,p_hat_6. Assume each true projected point is independently within Euclidean distance eps of its measured point. Set a=||p_hat_2-p_hat_6||, b=||p_hat_3-p_hat_5||, w=||p_hat_1-p_hat_4||.

The true *projected* eye aspect ratio r=(||p_2-p_6||+||p_3-p_5||)/(2||p_1-p_4||) obeys, when w>2eps:

r_min = (max(0,a-2eps)+max(0,b-2eps))/(2(w+2eps))
r_max = (a+b+4eps)/(2(w-2eps)).

Both bounds are attainable. Proof: triangle inequality bounds each pair distance by measured distance +/- 2eps. The three pairs use disjoint landmarks, so the numerator pairs can simultaneously contract while the denominator expands, and vice versa. Choose displacements along each pair's axis to attain all extrema. When w<=2eps, the upper ratio is generally unbounded. At w=eps=0 the ratio is undefined.

For a separate independently calibrated open EAR o in [o_min,o_max] with o_min>0, the closure proxy c=clip(1-r/o,0,1) has sharp interval
c_min=max(0,1-r_max/o_min), c_max=min(1,max(0,1-r_min/o_max)).
At threshold theta, certify CLOSED only when c_min>theta, OPEN only when c_max<theta; otherwise ABSTAIN. Equality is abstention.

Frozen synthetic boundary: a=b=6 px, w=30 px, o=0.30, theta=0.30. CLOSED iff (6+2eps)/(30-2eps)<0.21, i.e. eps<15/121 px (0.12396694214876033 px). At eps=0.12 CLOSED, at 0.124 ABSTAIN. Relative critical error eps/w=1/242.

**Scope limitation:** This theorem concerns the six-point 2D projected feature. It is NOT a bound on anatomical eyelid closure, true PERCLOS, hidden interframe events or fatigue. Pose/gaze and glasses can change the projected ratio without a physiological closure change. Real camera landmark-error and pose-transfer bounds have not been calibrated. The geometry is elementary and not claimed novel.
