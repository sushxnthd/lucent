import csv,hashlib,io,json,pathlib,sys,zipfile
import numpy as np
from PIL import Image
BASE=pathlib.Path(__file__).resolve().parent
def pixel_metrics(jpg,mask_bytes):
    with Image.open(io.BytesIO(jpg)) as im:
        mode=im.mode; rgb=np.asarray(im.convert("RGB"),dtype=np.uint8)
    mask=np.asarray(Image.open(io.BytesIO(mask_bytes)).convert("RGB"))
    assert rgb.shape==mask.shape
    p=mask[:,:,0]>=128; eye=p|(mask[:,:,1]>=128)
    assert eye.any()
    a=rgb.astype(np.int16)
    spread=a.max(axis=2)-a.min(axis=2)
    return dict(mode=mode,all_exact_gray=float((spread==0).mean()),eye_exact_gray=float((spread[eye]==0).mean()),
        all_gt2=float((spread>2).mean()),eye_gt2=float((spread[eye]>2).mean()),
        all_mean_spread=float(spread.mean()),eye_mean_spread=float(spread[eye].mean()))
def main():
    sys.path.insert(0,str(BASE.parent/"e002-158"))
    from download import get
    from pairs import matched
    from score import score
    result={"status":"NOT_EVALUABLE","waveform":"NOT_EVALUABLE"}
    try:
        td,path,manifest=get()
        rows=[];excluded={}
        with zipfile.ZipFile(path) as z:
            pairs,inventory=matched(z)
            for n,m in pairs[960:]:
                try:
                    b=z.read(n);mb=z.read(m)
                    oracle,err=score(b,mb,n,len(rows)+sum(excluded.values()))
                    if err:
                        excluded[err]=excluded.get(err,0)+1
                        continue
                    d=pixel_metrics(b,mb)
                    d.update(path=n,group=oracle["group"],image_sha256=hashlib.sha256(b).hexdigest())
                    rows.append(d)
                except Exception as e:
                    k="exception_"+type(e).__name__;excluded[k]=excluded.get(k,0)+1
                if len(rows)>=480:break
        td.cleanup()
        with (BASE/"RAW_CHROMA.csv").open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        a=np.array([r["all_exact_gray"] for r in rows]);b=np.array([r["eye_exact_gray"] for r in rows])
        result=dict(status="ORIGINAL_HUMAN_SOURCE_PIXEL_AUDIT",manifest=manifest,inventory=inventory,
            n=len(rows),groups=len(set(r["group"] for r in rows)),excluded=excluded,
            all_gray99=int((a>=.99).sum()),eye_gray99=int((b>=.99).sum()),
            all_gray99_fraction=float((a>=.99).mean()),eye_gray99_fraction=float((b>=.99).mean()),
            all_pixel_exact_gray_mean=float(a.mean()),eye_pixel_exact_gray_mean=float(b.mean()),
            all_gt2_mean=float(np.mean([r["all_gt2"] for r in rows])),
            eye_gt2_mean=float(np.mean([r["eye_gt2"] for r in rows])),
            modes={k:sum(r["mode"]==k for r in rows) for k in sorted(set(r["mode"] for r in rows))},
            G0_n480=len(rows)==480,G1_effectively_monochrome=float((a>=.99).mean())>=.95,
            G3_rgb_tracker_waveform="NOT_EVALUABLE",limitations="Previously examined cohort; not a paired physiological experiment.")
    except Exception as e:
        result["error"]=type(e).__name__+": "+str(e)
    (BASE/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    files=[p for p in [BASE/"RAW_CHROMA.csv",BASE/"RESULTS.json"] if p.exists()]
    (BASE/"SHA256SUMS").write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest()+"  "+p.name+"\n" for p in files))
    print(json.dumps(result,indent=2))
    if result["status"]!="ORIGINAL_HUMAN_SOURCE_PIXEL_AUDIT" or not result["G0_n480"]:raise SystemExit(2)
if __name__=="__main__":main()
