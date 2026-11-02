#!/usr/bin/env python3
"""E002-605: frozen independent human-label native-index alias assay.

NO physical shutter/velocity/closure inference from broad blink events. No source
images or individual source event times are emitted. Source acquisition is bounded.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import urllib.request
from collections import Counter

DATASET = '9yzdnng594'
FRAMES = {'S1':31071,'S2':32230,'S3':41388,'S4':8720,'S5':34355,'S6':20460,
          'S7':32074,'S8':11278,'S9':57557,'S10':41684,'S11':36345,'S12':43289}
SPLIT = {s:('development' if int(s[1:])<=4 else 'holdout') for s in FRAMES}
KEYS = {
 'subject':{'subject','subject_id','sample','video'},
 'start':{'start_frame','startframe','blink_start_frame','start_frame_index'},
 'end':{'end_frame','endframe','blink_end_frame','end_frame_index'},
 'kind':{'kind','type','annotation_type','event_type'},
}
ALLOWED = {'blink_event','fully_closed'}

def header_map(header):
    norm=[re.sub(r'[^a-z0-9]+','_',str(x).strip().lower()).strip('_') for x in header]
    result={}
    for key,choices in KEYS.items():
        found=[i for i,name in enumerate(norm) if name in choices]
        if len(found)!=1: raise ValueError('AMBIGUOUS_OR_MISSING_'+key.upper()+'_COLUMN')
        result[key]=found[0]
    return result

def exact_int(value):
    if isinstance(value,bool): raise ValueError('NONINTEGER_FRAME')
    if isinstance(value,int): return value
    if isinstance(value,float) and value.is_integer(): return int(value)
    if isinstance(value,str) and re.fullmatch(r'[0-9]+',value.strip()): return int(value.strip())
    raise ValueError('NONINTEGER_FRAME')

def normalize_subject(raw):
    s=str(raw).strip().upper()
    if re.fullmatch(r'S(?:[1-9]|1[0-2])',s): return s
    raise ValueError('UNSUPPORTED_SUBJECT')

def read_rows(rows):
    if not rows: raise ValueError('EMPTY_ANNOTATION_TABLE')
    cols=header_map(rows[0])
    result=[]; rejected=Counter()
    for row in rows[1:]:
        if not any(str(x).strip() for x in row): continue
        try:
            if len(row)<=max(cols.values()): raise ValueError('SHORT_ROW')
            sub=normalize_subject(row[cols['subject']]); lo=exact_int(row[cols['start']]); hi=exact_int(row[cols['end']])
            kind=str(row[cols['kind']]).strip().lower().replace(' ','_')
            if kind not in ALLOWED: raise ValueError('AMBIGUOUS_EVENT_KIND')
            if not (0<=lo<=hi<FRAMES[sub]): raise ValueError('OUT_OF_BOUNDS_OR_INVALID_INTERVAL')
            result.append((sub,lo,hi,kind))
        except ValueError as exc:
            rejected[str(exc)]+=1
    return result,rejected

def from_csv(raw):
    return read_rows(list(csv.reader(io.StringIO(raw.decode('utf-8-sig')))))

def from_xls(raw):
    try: import xlrd
    except ImportError: raise ValueError('XLRD_NOT_INSTALLED')
    try: wb=xlrd.open_workbook(file_contents=raw)
    except Exception as exc: raise ValueError('UNREADABLE_XLS_WORKBOOK') from exc
    all_events=[]; errors=Counter(); valid_sheets=0
    for sheet in wb.sheets():
        if sheet.nrows==0: continue
        rows=[sheet.row_values(i) for i in range(sheet.nrows)]
        try:
            events,rejected=read_rows(rows)
            all_events+=events; errors.update(rejected); valid_sheets+=1
        except ValueError as exc:
            errors['SHEET_'+str(exc)]+=1
    if valid_sheets==0: raise ValueError('NO_EXPLICIT_TYPED_FRAME_INTERVAL_TABLE')
    return all_events,errors

def evaluate(events,rejected=None,missing=None):
    rejected=Counter(rejected or {}); missing=missing or {}
    if len(events)!=len(set(events)): raise ValueError('DUPLICATE_EVENT_ROWS')
    agg={split:{kind:{'events':0,'missed_phases':0,'total_phases':0,'unknown_phases':0,'participants':set()}
                for kind in sorted(ALLOWED)} for split in ('development','holdout')}
    for sub,lo,hi,kind in events:
        if sub not in FRAMES or not(0<=lo<=hi<FRAMES[sub]) or kind not in ALLOWED:
            raise ValueError('UNVALIDATED_EVENT')
        a=agg[SPLIT[sub]][kind]; a['events']+=1; a['participants'].add(sub)
        miss=set(missing.get(sub,()))
        for p in range(3):
            if any(lo<=n<=hi for n in miss): a['unknown_phases']+=1; continue
            a['total_phases']+=1
            if lo+(p-lo)%3>hi: a['missed_phases']+=1
    for split in agg:
        for kind,a in agg[split].items():
            a['participants']=len(a['participants'])
    return {'experiment':'E002-605','evidence':'ANNOTATION_INDEX_ONLY_NOT_SHUTTER',
            'dataset_doi':'10.17632/9yzdnng594.1','phase_rule':'native_index_mod_3',
            'counts':agg,'excluded':dict(sorted(rejected.items())),
            'physical_shutter_calibrated':False,'continuous_velocity_certified':False,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}

def _get(url,limit):
    req=urllib.request.Request(url,headers={'Accept':'application/json','User-Agent':'Lucent-E002605-research/1.0'})
    with urllib.request.urlopen(req,timeout=25) as resp:
        size=0; chunks=[]
        while True:
            part=resp.read(min(65536,limit+1-size))
            if not part: break
            chunks.append(part); size+=len(part)
            if size>limit: raise ValueError('SOURCE_TOO_LARGE')
        return b''.join(chunks)

def probe_mendeley():
    base=f'https://api.data.mendeley.com/datasets/{DATASET}'
    try:
        meta=json.loads(_get(base+'/files?version=1&%24limit=100',1_000_000))
        files=meta.get('results',meta.get('files',[])) if isinstance(meta,dict) else meta
        if not isinstance(files,list): raise ValueError('UNKNOWN_FILE_LIST_FORMAT')
        candidates=[f for f in files if re.search(r'annotations?\.xls$',f.get('filename',''),re.I)]
        if len(candidates)!=1: raise ValueError('ANNOTATION_FILE_NOT_UNIQUE')
        file=candidates[0]; fid=file.get('id'); detail=file.get('content_details') or {}
        url=detail.get('download_url') or (base+'/files/'+str(fid)+'/file_downloaded?version=1' if fid else None)
        if not url: raise ValueError('NO_PUBLIC_DOWNLOAD_URL')
        data=_get(url,40_000_000)
        expected=detail.get('sha256_hash')
        if expected and hashlib.sha256(data).hexdigest().lower()!=str(expected).lower(): raise ValueError('SOURCE_SHA256_MISMATCH')
        events,errors=from_xls(data)
        result=evaluate(events,errors)
        result['source_access']='PUBLIC_XLS_VERIFIED' if expected else 'PUBLIC_XLS_UNPINNED_SHA256'
        result['annotation_sha256']=hashlib.sha256(data).hexdigest()
        result['recognized_events']=len(events)
        return result
    except Exception as exc:
        return {'experiment':'E002-605','source_access':'ABSTAIN','reason':type(exc).__name__+':'+str(exc)[:150],
                'recognized_events':0,'human_closure_validated':False,
                'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv');p.add_argument('--xls');p.add_argument('--probe-mendeley',action='store_true');args=p.parse_args()
    if args.probe_mendeley: out=probe_mendeley()
    elif args.csv or args.xls:
        raw=open(args.csv or args.xls,'rb').read()
        ev,errors=from_csv(raw) if args.csv else from_xls(raw)
        out=evaluate(ev,errors)
    else: p.error('provide --csv, --xls, or --probe-mendeley')
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
