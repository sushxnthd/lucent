import numpy as np
# Independent exact rank and noninjectivity demonstration for published 3-bin rowwise mean.
n=89
i=np.arange(n,dtype=float)
base=np.stack([3.2+.05*np.sin(i/8),3.3+.05*np.sin(i/8),3.4+.05*np.sin(i/8)])
perturb=np.stack([.2*np.sin(i/5),-.1*np.sin(i/5),-.1*np.sin(i/5)])
alt=base+perturb
M=np.concatenate([np.eye(n)/3]*3,axis=1)
assert np.linalg.matrix_rank(M)==n
assert np.all(base>0) and np.all(alt>0)
assert np.max(np.abs(base.mean(axis=0)-alt.mean(axis=0)))<1e-14
print(dict(rank=n,nullity=2*n,max_input_difference=float(np.max(np.abs(base-alt))),max_output_difference=float(np.max(np.abs(base.mean(axis=0)-alt.mean(axis=0)))))
