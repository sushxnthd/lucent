# E002-319: Sharp conditional reference-folding observability law

**Scope:** Ideal 3-second session with exactly 90 90-Hz Tobii samples in each of three 1-second bins, 90 sequential 30-fps webcam frames, no missing data, aligned session start. The actual public script can encounter unequal bins and NaNs; no Kaggle rows were inspected.

**Primary implementation:** https://github.com/vijulshah/eyedentify/blob/main/data_creation/eyedentify/tobii_and_webcam_data_alignment.py , blob f46d7ae369a62596f7044ca647d361c38fcb16ea. Timestamp precision is reduced to whole seconds; the three per-second Tobii groups are concatenated by *row index*, averaged, then paired in order with extracted webcam frames. The published paper also describes this process: https://arxiv.org/abs/2407.11204 .

## Theorem 1 — exact nullspace and preserved aggregate
Let x[0..269] be native Tobii samples and y[0..89] the processed labels. The operator is y[j]=(x[j]+x[j+90]+x[j+180])/3. Its 90-by-270 matrix A has disjoint row supports, so A A^T=I/3, rank(A)=90 and nullity(A)=180. Its kernel comprises all traces with x[j]+x[j+90]+x[j+180]=0 for every j. Nevertheless, mean(y)=mean(x). This last identity requires equal bin sizes and no missingness/truncation.

## Theorem 2 — exact slow-frequency null and time warp
For x(t)=a+Re[B exp(i 2π f t)] and u=j/90, the folded label is y(u)=a+Re[B exp(i 2π f u) H(f)], where H(f)=(1+exp(i2πf)+exp(i4πf))/3=exp(i2πf)(1+2 cos(2πf))/3. Thus H(f)=0 for f=k+1/3 or k+2/3 Hz (integer k). A smooth 1/3-Hz oscillation is **completely erased** in the processed labels even though it is below the nominal 15-Hz webcam Nyquist limit.

Exact positive counterexample: x_A(t)=3+0.2 sin(2πt/3+φ) mm and x_B(t)=3-0.2 sin(2πt/3+φ) mm produce identical y[j]=3. They have distinct native traces. Their RGB images could differ: this is a *label collision*, not a physical full-RGB impossibility.

RGB frame j nominally occurs at t=j/30, while label j averages samples at j/90, 1+j/90 and 2+j/90. For linear x(t)=a+bt, folded y[j]=a+b(1+j/90), so the label slope against RGB frame time is b/3. Thus even surviving temporal components are not frame-time synchronized.

## Theorem 3 — sharp bounded-speed error envelope
If x is L-Lipschitz (mm/s), the nominal instantaneous frame-reference discrepancy obeys |y[j]-x(j/30)| <= L B_j, where B_j=(|0-2j/90|+|1-2j/90|+|2-2j/90|)/3 seconds. It is **sharp for each j**: x(t)=a+L|t-j/30| attains equality, and smooth approximations approach it. B_0=1 second, B_45=2/3 second, B_89=134/135 second; min_j B_j=2/3 and max_j B_j=1. No empirical human L or camera shutter duration is assumed.

## Consequence and limits
The published preprocessing operator does not provide valid frame-synchronous ground truth for rapid pupil waveform, physiological phase/lag or blink dynamics. In the ideal case it retains a three-second mean, which may support a weaker endpoint after human verification. The finding is **source-specific** and conditional on actual released data following the public script; it is not a claim that the ordinary RGB camera cannot see these signals. Rank-nullity, Fourier transfer and Lipschitz bounds are classical mathematics. Human validation and publication novelty remain open.
