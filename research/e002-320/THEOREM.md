# Exact restricted shutter-duty and occupancy theorems

Let c(t)∈[0,1] be normalized anatomical eyelid closure. Assume calibrated scalar measurements y_i=E^{-1}∫_{iP}^{iP+E}c(t)dt+e_i, |e_i|≤η, 0<E≤P, no missing frames for Theorem A, and a known null baseline c=0. This proxy is NOT known to be valid for ordinary RGB without calibration.

## A. Sharp worst-phase event distinguishability

For an alternative c(t)=a 1_[s,s+d](t), 0≤d≤P, define G=P−E and o_i(s)=|[s,s+d]∩[iP,iP+E]|. Then

min_s max_i o_i(s) = (d−G)_+/2.

Proof: an interval of length ≤P contains ≤G total unexposed time, so it has ≥(d−G)_+ overlap with exposed time. It intersects at most two exposures; one overlap is at least half. Equality is attained by centering on a gap (or hiding fully within it when d≤G).

Under null, coordinate i lies in [−η,η]. Under the event, it lies in [a o_i/E−η,a o_i/E+η]. The product sets intersect iff all a o_i/E≤2η. Hence guaranteed distinguishability for *every* phase iff

a(d−G)_+/(2E)>2η.

For η/a<1/4, dcrit=G+4ηE/a. Equality cannot certify. For η/a≥1/4 no d≤P is guaranteed. Exact collision witnesses: when d≤G, place the entire plateau in the shutter gap; for G<d≤dcrit, choose null error +a o_i/(2E) and event error −a o_i/(2E).

## B. Sharp shutter-window closure burden

For N disjoint exposures length E in a total window T, uncovered time U=T−NE, measured means y_i with |e_i|≤η, and arbitrary c(t)∈[0,1], true B=T^{-1}∫c satisfies

(E/T)Σmax(0,y_i−η) ≤ B ≤ [U+EΣmin(1,y_i+η)]/T.

Sharp: take c constant at each allowed exposure mean and set all uncovered c to 0 or 1. For complete exposure coverage and η=0, the mean is exactly identified even though timing within frames is not.

## C. Sharp raw threshold occupancy (NOT blink-filtered PERCLOS)

Let Pθ=T^{-1}|{t:c(t)≥θ}|, 0<θ<1. Then

Pθ ≥ (E/T)Σmax(0,[max(0,y_i−η)−θ]/(1−θ)),
Pθ ≤ U/T+(E/T)Σmin(1,min(1,y_i+η)/θ).

For a single interval with mean m and threshold occupancy p, θp≤m≤θ(1−p)+p. Optimize each interval and assign arbitrary states in gaps. Upper bounds attained with 0/θ mixtures; lower bounds are sharp infima using θ−ε/1 mixtures. Conventional PERCLOS variants exclude rapid blinks and require temporal ordering; they are not certified by this theorem.

## Important limits

Rectangular *closure plateaus* are not generic smooth blink waveforms. Unbounded geometry, lighting, glasses, rolling shutter, unknown exposure, ISP nonlinearities, temporal aftereffects and missing frames invalidate the simple guarantee. This is classical sampling/dead-time and moment-bound mathematics, not an established novel field-level result.