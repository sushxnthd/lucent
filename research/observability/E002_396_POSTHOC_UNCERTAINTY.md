# E002-396 post-hoc uncertainty analysis (exploratory; 2026-10-23)

**Not preregistered.** The three original frozen E002-396 hypotheses all failed and remain failed. This addendum quantifies uncertainty in the already reported cross-recording rank reversal, not evidence of a general population effect.

Using anonymous per-pair scores from the independently verified E002-395 S01 holdout (35 pairs) and E002-396 S19 (36 pairs), compute ROC AUC as the mean over all event-control score comparisons with half-credit for ties. For each of **2,000** bootstrap iterations, independently resample each participant's *event/control pairs as a unit*, with replacement, using NumPy `default_rng(371)`. Use the 2.5th and 97.5th empirical percentiles; compute the difference S19 minus S01 per bootstrap iteration.

| Estimand | Observed | Exploratory paired-bootstrap 95% percentile interval |
| --- | ---: | ---: |
| S01 held-out direct AUC | 0.200408 | [0.081612, 0.336347] |
| S19 unseen-participant direct AUC | 0.926698 | [0.870370, 0.972222] |
| S19 minus S01 AUC | **+0.726289** | **[+0.577062, +0.857895]** |

Reproduction with artifacts 12506595116 and 12506996600 (both expire 2026-11-06):

```python
import json, zipfile, numpy as np
def get(zip_path, score_path, key=None):
    with zipfile.ZipFile(zip_path) as z:
        x=json.loads(z.read(score_path))
    return x[key] if key else x
s01=get("github-actions-artifact-12506595116.zip","e002_395_anonymous_scores.json","test")
s19=get("github-actions-artifact-12506996600.zip","e002_396_anonymous_scores.json")
def auc(data):
    p=np.array([r["clean"]["positive"] for r in data])
    n=np.array([r["clean"]["control"] for r in data])
    return float(np.mean((p[:,None]>n[None,:])+.5*(p[:,None]==n[None,:])))
rng=np.random.default_rng(371)
b1,b19=[],[]
for _ in range(2000):
    b1.append(auc([s01[j] for j in rng.integers(0,len(s01),len(s01))]))
    b19.append(auc([s19[j] for j in rng.integers(0,len(s19),len(s19))]))
print(auc(s01),np.percentile(b1,[2.5,97.5]))
print(auc(s19),np.percentile(b19,[2.5,97.5]))
print(auc(s19)-auc(s01),np.percentile(np.array(b19)-np.array(b1),[2.5,97.5]))
```

**Interpretation boundary:** These intervals condition on **two selected participants** and their within-person event/control sampling. They do **not** quantify variability across people, cameras, annotators or nuisance conditions. The source labels are EEG markers, not measured physical aperture. The strong opposite-direction ranking on two people is a concrete reason to reject unqualified cross-person intensity claims, not a universal law or proof of human no-hidden-closure observability. Product remains `ABSTAIN_UNCALIBRATED`.
