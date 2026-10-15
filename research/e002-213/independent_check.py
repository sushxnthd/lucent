"""Independent numerical checker for E002-213, synthetic data only."""
import csv
from pathlib import Path
import numpy as np
from experiment import derivative,STEPS,SETS
with Path(__file__).with_name("RAW_SYNTHETIC.csv").open() as f:
    rows=list(csv.DictReader(f))
assert len(rows)==90
for row in rows:
    q=dict(r=float(row["radius_px"]),blur=float(row["blur_px"]),contrast=.55,background=.75,x=.14,y=-.12,ellipticity=.95,gradient=.01)
    j=derivative(q,"r",STEPS["r"]/2)
    names=SETS[row["model"]]
    if names:
        J=np.column_stack([derivative(q,k,STEPS[k]/2) for k in names])
        U,s,V=np.linalg.svd(J,full_matrices=False)
        assert min(s)>1e-8
        j=j-U@(U.T@j)
    observed=float(j@j/.02**2)
    expected=float(row["info_eff"])
    assert np.isclose(observed,expected,rtol=.08,atol=.03)
print("PASS: 90 synthetic cases, independent SVD projection")
