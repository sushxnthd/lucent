"""Inspect Figshare ADHD pupil dataset structure for temporal-locality study.

Dataset:
Rojas-Libano et al. 2019, Figshare 7218725 v3, CC BY 4.0.
Direct public file: https://figshare.com/ndownloader/files/14298953

MATLAB MCOS decoding approach adapted from D1D2DOPAMINE's MIT-licensed
ADHD_PUPIL_VALIDATOR.py:
https://github.com/d1d2dopamine/allostatic-sprint-hypothesis
"""

from __future__ import annotations

from pathlib import Path
import re
import requests
import numpy as np
import pandas as pd
from mat73_reader import load as mcos_load

URL = "https://figshare.com/ndownloader/files/14298953"
TARGET = Path("/tmp/adhd_pupil_dataset_v3.mat")


def norm(x):
    return re.sub(r"[^a-z0-9]+", "", str(x).lower())


def download():
    if TARGET.exists() and TARGET.stat().st_size > 1_000_000_000:
        print("using cached:", TARGET.stat().st_size)
        return
    with requests.get(URL, stream=True, timeout=(30, 300)) as r:
        r.raise_for_status()
        total=int(r.headers.get("Content-Length") or 0)
        print("status",r.status_code,"bytes expected",total,"final",r.url)
        with TARGET.open("wb") as f:
            done=0
            for chunk in r.iter_content(8*1024*1024):
                if chunk:
                    f.write(chunk); done+=len(chunk)
                    if total and done%(128*1024*1024)<8*1024*1024:
                        print("downloaded",done)
    print("downloaded total",TARGET.stat().st_size)


def records_from_object(obj):
    if isinstance(obj,list): return obj
    if isinstance(obj,tuple): return list(obj)
    if isinstance(obj,np.ndarray):
        if obj.dtype.names:
            return [{name: row[name] for name in obj.dtype.names} for row in obj.reshape(-1)]
        return list(obj.reshape(-1))
    if isinstance(obj,dict):
        lengths=[]
        for v in obj.values():
            try:
                if not isinstance(v,(str,bytes)): lengths.append(len(v))
            except Exception: pass
        n=max(lengths,default=0)
        if n>1 and sum(z==n for z in lengths)>=2:
            return [{k:(v[i] if hasattr(v,"__len__") and not isinstance(v,(str,bytes)) and len(v)==n else v) for k,v in obj.items()} for i in range(n)]
        return [obj]
    return [obj]


def get(rec,*aliases):
    if not isinstance(rec,dict): return None
    lookup={norm(k):v for k,v in rec.items()}
    for a in aliases:
        if norm(a) in lookup: return lookup[norm(a)]
    return None


def to_df(obj):
    if isinstance(obj,pd.DataFrame): return obj
    if isinstance(obj,dict):
        try:
            return pd.DataFrame({str(k):list(np.asarray(v).reshape(-1)) for k,v in obj.items()})
        except Exception:
            pass
    if isinstance(obj,list) and obj and isinstance(obj[0],dict): return pd.DataFrame(obj)
    if isinstance(obj,np.ndarray) and obj.ndim==2: return pd.DataFrame(obj)
    raise TypeError(type(obj).__name__)


def describe_cell(x):
    print("  type",type(x).__name__)
    try:
        a=np.asarray(x,dtype=object)
        print("  array shape",a.shape,"dtype",a.dtype)
        if a.size:
            for i,v in enumerate(a.reshape(-1)[:4]):
                try:
                    q=np.asarray(v)
                    print("   part",i,"type",type(v).__name__,"shape",q.shape,"dtype",q.dtype,
                          "head",q.reshape(-1)[:8].tolist())
                except Exception as e:
                    print("   part",i,"repr",repr(v)[:300],"err",e)
    except Exception as e:
        print("  cannot array:",e,"repr",repr(x)[:500])


def main():
    download()
    print("loading MCOS Pupil_data...")
    obj=mcos_load(str(TARGET),variable="Pupil_data")
    recs=records_from_object(obj)
    print("sessions",len(recs))
    rec=recs[0]
    print("record keys",list(rec.keys()) if isinstance(rec,dict) else type(rec))
    print("subject",get(rec,"Subject"),"group",get(rec,"Group"))

    epoch=get(rec,"Task_epocs","Task_epochs","Task_epoch")
    df=to_df(epoch)
    print("epoch shape",df.shape)
    print("epoch columns",list(df.columns))
    print("epoch row0 scalar preview")
    for col in df.columns:
        if norm(col)=="pupil":
            continue
        v=df.iloc[0][col]
        print(" ",col,repr(v)[:300])

    pupil_col=next((c for c in df.columns if norm(c)=="pupil"),None)
    if pupil_col:
        print("Pupil cell:")
        describe_cell(df.iloc[0][pupil_col])

    raw=get(rec,"Task_data","TaskData")
    print("Task_data type",type(raw).__name__)
    try:
        rdf=to_df(raw)
        print("raw shape",rdf.shape)
        print("raw columns",list(rdf.columns))
        for col in rdf.columns:
            print("raw",col,"first",repr(rdf.iloc[0][col])[:300])
    except Exception as e:
        print("raw decode failed",type(e).__name__,e)
        if isinstance(raw,dict): print("raw keys",list(raw.keys()))


if __name__=="__main__":
    main()
