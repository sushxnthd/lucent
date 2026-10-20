"""Independently reproduce the published pandas rowwise group mean."""
import numpy as np
import pandas as pd
rng=np.random.default_rng(319)
v=rng.normal(3,.2,270)
groups=[pd.Series(v[k*90:(k+1)*90]).reset_index(drop=True) for k in range(3)]
folded=pd.concat(groups,axis=1).mean(axis=1)
assert len(folded)==90
assert np.max(abs(folded.to_numpy()-(v[:90]+v[90:180]+v[180:])/3))<1e-14
unequal=[pd.Series(v[:89]),pd.Series(v[89:179]),pd.Series(v[179:])]
rows=pd.concat(unequal,axis=1).mean(axis=1)
assert len(rows)==91
truncated=rows.iloc[:90]
assert len(truncated)==90
print("PASS: equal bins reproduce exact fold; unequal 89/90/91 bins yield 91 rows then 90 after frame truncation")
