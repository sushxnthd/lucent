#!/usr/bin/env python3
"""E002-395 independent aggregate oracle; source verification, no aperture inference."""
import argparse, hashlib, json, pathlib, random

def md5(path):
    h=hashlib.md5()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def auc(p,n):
    return sum((a>b)+.5*(a==b) for a in p for b in n)/(len(p)*len(n))

def threshold_fit(p,n):
    scores=sorted(set(p+n))
    def J(t):
        return sum(x>=t for x in p)/len(p)-sum(x>=t for x in n)/len(n)
    return max(scores+[scores[-1]+1e-9],key=lambda t:(J(t),t))

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--archive",required=True)
    a.add_argument("--output",required=True)
    v=a.parse_args()
    out=pathlib.Path(v.output)
    r=json.loads((out/"e002_395_result.json").read_text())
    x=json.loads((out/"e002_395_anonymous_scores.json").read_text())
    assert md5(v.archive)==r["source_md5"]=="fef02cb7ebf62e4f3efb6303284fd6cb"
    assert len(x["train"])==r["train_pairs"]==x["train_n"]
    assert len(x["test"])==r["heldout_pairs"]>=20
    assert r["pairs"]==len(x["train"])+len(x["test"])
    assert r["excluded_previously_inspected_phantom_ids"]==[758,1249,1667,2610,3284,4045]
    p=[z["clean"]["positive"] for z in x["train"]]
    n=[z["clean"]["control"] for z in x["train"]]
    assert abs(threshold_fit(p,n)-r["threshold_fit_on_training_only"])<1e-12
    for variant,vv in r["variants"].items():
        p=[z[variant]["positive"] for z in x["test"]]
        n=[z[variant]["control"] for z in x["test"]]
        assert abs(auc(p,n)-vv["auc"])<1e-12
        t=r["threshold_fit_on_training_only"]
        assert abs(sum(s>=t for s in p)/len(p)-vv["sensitivity"])<1e-12
        assert abs(sum(s<t for s in n)/len(n)-vv["specificity"])<1e-12
    rng=random.Random(371)
    pos=[z["clean"]["positive"] for z in x["test"]]
    neg=[z["clean"]["control"] for z in x["test"]]
    for _ in range(1000):
        _=[rng.randrange(len(pos)) for q in pos]
    labels=[1]*len(pos)+[0]*len(neg)
    rng.shuffle(labels)
    scores=pos+neg
    null=auc([s for s,l in zip(scores,labels) if l],
             [s for s,l in zip(scores,labels) if not l])
    assert abs(null-r["shuffled_label_auc"])<1e-12
    assert r["frozen_primary_auc_ge_075"]==(r["variants"]["clean"]["auc"]>=.75)
    assert r["product_decision"]=="ABSTAIN_UNCALIBRATED"
    assert not r["physical_aperture_validated"] and not r["actual_exposure_known"]
    print(json.dumps({"independent_oracle":"PASS","pairs":r["pairs"],
       "test":r["heldout_pairs"],"clean_auc":r["variants"]["clean"]["auc"],
       "primary_pass":r["frozen_primary_auc_ge_075"],
       "product":r["product_decision"]}))

if __name__=="__main__":
    main()
