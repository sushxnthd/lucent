#!/usr/bin/env python3
"""Fail-closed RGB-only admission / provenance guard for E002-267 evaluation.
Scientific waveform gates remain E002-267; this is not a new physiology model.
"""
import hashlib, math, pathlib, sys
from collections import defaultdict

ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research'/'e002-267'))
from evaluate import evaluate, sd

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def verify_human_source(manifest,raw_path=None,clock_evidence_path=None):
    if manifest.get('data_type')!='human':return False
    if not raw_path or not clock_evidence_path:raise ValueError('HUMAN_RAW_AND_CLOCK_EVIDENCE_REQUIRED')
    for path,key in ((raw_path,'source_dataset_sha256'),
                     (clock_evidence_path,'clock_evidence_sha256')):
        declared=manifest.get(key,'')
        if len(declared)!=64 or sha256_file(path)!=declared:
            raise ValueError('SOURCE_BYTES_HASH_MISMATCH_'+key)
    return True

def blind_windows(rows, fps):
    groups=defaultdict(list)
    for r in rows:
        if r['split']=='test':groups[r['participant_id'],r['session_id']].append(r)
    out={}
    for (p,s),g in groups.items():
        g=sorted(g,key=lambda r:r['t_rgb_s']);start=g[0]['t_rgb_s']
        bins=defaultdict(list)
        for r in g:bins[int((r['t_rgb_s']-start+1e-8)//5)].append(r)
        for wi,c in bins.items():
            if c[-1]['t_rgb_s']-c[0]['t_rgb_s']<4.9:continue
            # Only camera-side values; NEVER read reference_mm, t_ref_s or valid_ref.
            out[p,s,wi]=(len(c)>=round(5*fps)*.8 and
               len({r['t_rgb_s'] for r in c})==len(c) and
               sd([r['rgb_ratio'] for r in c])>=.005 and
               all(math.isfinite(r[k]) for r in c for k in
                   ('rgb_ratio','brightness','geometry','iris_ratio','t_rgb_s')))
    return out

def strict_evaluate(rows,manifest,raw_path=None,clock_evidence_path=None):
    human_verified=verify_human_source(manifest,raw_path,clock_evidence_path)
    blind=blind_windows(rows,float(manifest['camera_fps']))
    old=evaluate(rows,manifest)
    lookup={(w['participant'],w['session'],w['window']):w for w in old['windows']}
    if set(lookup)!=set(blind):raise ValueError('WINDOW_ACCOUNTING_MISMATCH')
    accepted=[k for k,v in blind.items() if v]
    scored=[lookup[k] for k in accepted]
    certified=sum(bool(w['admitted'] and w['accurate']) for w in scored)
    unscorable=sum(not w['admitted'] for w in scored)
    return dict(source_type=manifest['data_type'],human_source_verified=human_verified,
      blind_admitted=len(accepted),total_windows=len(blind),
      blind_coverage=len(accepted)/len(blind) if blind else 0,
      certified_windows=certified,unscorable_admitted=unscorable,
      certified_fraction=certified/len(accepted) if accepted else 0,
      # Fail closed: original reference-selected bootstrap and holdouts remain unaudited.
      product_certificate=False,
      certification_blocker='REQUIRES_REFERENCE_BLIND_BOOTSTRAP_AND_HOLDOUT_AUDIT')
