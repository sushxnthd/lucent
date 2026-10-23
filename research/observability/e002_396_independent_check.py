#!/usr/bin/env python3
"""Independent source reparse and pairwise rank oracle for E002-396."""
import argparse,csv,hashlib,io,json,pathlib,zipfile

def auc(p,n):
    return sum((a>b)+.5*(a==b) for a in p for b in n)/(len(p)*len(n))

def md5(path):
    h=hashlib.md5()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):
            h.update(block)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    out=pathlib.Path(a.output)
    r=json.loads((out/"e002_396_result.json").read_text())
    scores=json.loads((out/"e002_396_anonymous_scores.json").read_text())
    assert md5(a.archive)==r["source_md5"]=="8a16cf170a9c7e9660f6e22b81d7d0a"
    with zipfile.ZipFile(a.archive) as z:
        sync=r["selected_session_stem"]+"_sync.csv"
        assert sync in z.namelist()
        with z.open(sync) as f:
            rows=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig"))
            nframe=0;nmark=0
            for row in rows:
                if row.get("PhanFrame","").strip():
                    nframe+=1
                try:
                    nmark+=float(row.get("Blinks") or 0)>0
                except ValueError:
                    pass
    assert nframe==r["camera_frames"] and nmark==r["eeg_markers"]
    assert len(scores)==r["paired_windows"]>=15
    t=r["frozen_s01_threshold"]
    assert abs(t-.7938034188034189)<1e-14
    for variant,v in r["variants"].items():
        pos=[z[variant]["positive"] for z in scores]
        neg=[z[variant]["control"] for z in scores]
        d=auc(pos,neg)
        inv=auc([1-x for x in pos],[1-x for x in neg])
        assert abs(d-v["direct_auc"])<1e-12
        assert abs(inv-v["inverse_auc"])<1e-12
        assert abs(d+inv-1)<1e-12
        assert abs(sum(x<t for x in neg)/len(neg)-v["specificity"])<1e-12
    clean=r["variants"]["clean"]
    assert r["H1_inverse_auc_ge_075"]==(clean["inverse_auc"]>=.75)
    assert r["H2_direct_auc_below_050"]==(clean["direct_auc"]<.5)
    assert r["H3_frozen_threshold_specificity_le_050"]==(clean["specificity"]<=.5)
    assert r["product"]=="ABSTAIN_UNCALIBRATED"
    assert not r["human_physical_aperture"] and not r["exposure_calibrated"]
    print(json.dumps({"independent_oracle":"PASS","frames":nframe,
      "markers":nmark,"pairs":len(scores),"direct_auc":clean["direct_auc"],
      "inverse_auc":clean["inverse_auc"],"product":r["product"]}))

if __name__=="__main__":
    main()
