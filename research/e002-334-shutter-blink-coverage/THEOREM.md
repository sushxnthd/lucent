# E002-334 sharp event-detectability boundary

Let global-shutter windows be W_n=[nF,nF+E], 0<E<=F. A rectangular eyelid-closure event B_t=[t,t+D] has calibrated scalar exposure response s_n(t)=a*length(W_n intersection B_t)/E. Observations y_n=s_n(t)+e_n, with a>0 and |e_n|<=eta. In the no-event world, y_n=e_n.

**Exact conditional result:** If a<=2eta, the event and no-event feasible observation sets overlap for every D and every onset. If a>2eta, they overlap for some onset phase if and only if D<=Dcrit=F-E+4eta E/a. For D>Dcrit, the sets are disjoint for all phases. Equality is ambiguous.

**Proof:** The two worlds have a common observation sequence iff s_n<=2eta for every n. Put h=2eta E/a<E. A shutter overlap exceeds h iff the event onset belongs to (nF+h-D,nF+E-h). The intervals repeat with period F, each having width D+E-2h. They cover every onset phase iff their width is strictly >F. Thus guaranteed distinction iff D>F-E+2h. If all overlaps are <=h, the common observation y_n=s_n/2 is feasible with errors +/-s_n/2. QED.

**Full RGB zero-noise special case:** If D<=F-E, an event can fit entirely in a shutter dead-time gap; all captured images equal the no-event images, independently of the appearance during the unobserved event. If D>F-E, some exposure intersects the event, but image distinguishability still needs contrast/nuisance assumptions.

**General irregular shutter condition:** For shutters [t_j,t_j+E_j], contrast a_j and noise eta_j, guarantee detection iff the union of open onset intervals (t_j+h_j-D,t_j+E_j-h_j), h_j=2eta_j E_j/a_j, covers the specified onset domain. Frame drops therefore change the boundary through maximum shutter gap.

**Limits:** scalar rectangular-event model, fixed calibrated contrast and bounded error, global shutter and exact exposure timing. Rolling shutter, gaze/glasses effects, variable contrast, nonrectangular partial blinks, nonlinear ISP and clock errors need independent calibration. Not a general pupil/fatigue observability theorem.
