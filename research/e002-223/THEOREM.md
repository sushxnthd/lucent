# Conditional theorem and scope

Given native reference s(t), camera reported time u=t+delta and video observable y(u)=F(s(u-delta-tau)), replace (delta,tau) by (delta+c,tau-c). Their sum is unchanged, so the entire observable is identical for every u, any s, any F. Even perfect RGB segmentation cannot identify the two parameters separately. An independent exposure-time anchor breaks this symmetry.

For stationary bandlimited s with power spectrum supported in [-B,B], normalized autocorrelation is the spectral average of cos(2*pi*f*h). For |h|<=1/(2B), it is at least cos(2*pi*B*|h|), sharply attained by a single frequency B. This is NOT a bound on finite five-second sample Pearson correlation.

At an illustrative r=0.7 pure-sinusoid threshold, allowable offsets are 126.59 ms (1 Hz), 63.30 ms (2 Hz), and 25.32 ms (5 Hz). No claim of new mathematical novelty or human validation.
