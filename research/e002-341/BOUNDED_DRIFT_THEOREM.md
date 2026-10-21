# E002-341: exact bounded-drift observability

For an RGB-derived scalar ocular feature under a **calibrated** finite temporal nuisance-drift model, compare H0: y_i=b_i+e_i and H1: y_i=beta*s_i+b_i+e_i, with nuisance path |b_i-b_j|<=L|t_i-t_j|, observation error |e_i|<=eta, and arbitrary baseline b_0. The nuisance and errors may differ across hypotheses.

**Sharp iff condition:** the two possible observation sets are disjoint exactly when

max_(i<j) [ |beta*(s_i-s_j)| - 2*L*(t_j-t_i) - 4*eta ] > 0.

At equality they intersect. Thus L_critical=max_(i<j)(|beta*(s_i-s_j)|-4eta)/(2*(t_j-t_i)); certification requires 0<=L<L_critical.

**Proof:** An overlap gives beta*s=d+n where d is 2L-Lipschitz and |n_i|<=2eta, implying all pairwise inequalities. Conversely, the pairwise inequalities imply a 2L-Lipschitz selection d_i in the intervals [beta*s_i-2eta,beta*s_i+2eta]. Taking nuisance paths +/-d/2 and errors +/-(beta*s-d)/2 constructs exactly the same observations under both hypotheses. This proves sharpness.

**Measurement origin:** with fully visible approximately coplanar iris/pupil and a common affine projection, sqrt(A_p/A_i)=r_p/r_i. With visibility fractions v_p,v_i, log apparent ratio equals log(r_p/r_i)+0.5log(v_p/v_i)+photometric and projection bias+error. The latter terms must be independently shown L-Lipschitz; shutter integration needs a separate error bound. At pupil occlusion v_p approaches zero and no finite bound can be assumed. This is a feature-level theorem, not a universal RGB-video theorem.

**Synthetic boundary:** t=[0,.1,.2,.3]s, s=[0,0,1,1], beta=1, eta=.1 gives L_critical=3 feature units/s. L=2.9 certifies; L=3.0 intersects; L=3.1 cannot certify. These values are illustrative, not human measurements.

Independent LP feasibility oracle (650 random cases; 185 boundary pairs; geometry, brightness, missingness, smoothness controls) passed. No human outcomes evaluated, no publication-level novelty established. The result refines the earlier unbounded-nuisance-subspace analysis by specifying the weakest usable calibrated drift constraint.
