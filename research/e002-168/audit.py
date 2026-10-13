#!/usr/bin/env python3
"""E002-168: deterministic schema and timebase audit, synthetic fixtures only."""
import json, re
from collections import OrderedDict
KEYS=('TIME TIME_TICK FPOGX FPOGY FPOGS FPOGD FPOGID FPOGV '
'LPOGX LPOGY LPOGV RPOGX RPOGY RPOGV BPOGX BPOGY BPOGV '
'LPCX LPCY LPD LPS LPV RPCX RPCY RPD RPS RPV '
'LEYEX LEYEY LEYEZ LPUPILD LPUPILV REYEX REYEY REYEZ RPUPILD RPUPILV '
'BKID BKDUR BKPMIN LPMM LPMMV RPMM RPMMV PIXX PIXY PIXS PIXV').split()
assert len(KEYS)==48
def fixture(counter=True,n=251):
    result=[]
    for i in range(n):
        f=OrderedDict()
        if counter: f['CNT']=i+1484
        for key in KEYS: f[key]='1.00000'
        f['TIME']=f'{706.7038+i/50:.5f}'
        f['TIME_TICK']=str(94841050736+i*200000)
        f['LPMM']=f'{3.2+i*.0002:.5f}'
        f['RPMM']=f'{3.1+i*.0002:.5f}'
        for k in ('LPUPILV','RPUPILV','LPMMV','RPMMV','LPOGV','RPOGV'): f[k]='1'
        result.append(f)
    return result
def convert(f):
    line='<REC '+' '.join(f'{k}="{v}"' for k,v in f.items())+' />'
    return [x[1:-2] for x in re.findall(r'".*?" ',line)] if 'RPOGY' in line and 'LPOGX' in line else []
def nearest(source, frames):
    return [min(range(len(source)),key=lambda j:abs(source[j]-t)) for t in frames]
def gate(rows):
    if any(len(r)!=49 for r in rows): return False,'expected_49_columns_with_CNT'
    c=[int(float(r[0])) for r in rows]
    s=[float(r[1]) for r in rows]
    t=[int(float(r[2])) for r in rows]
    if any(b<=a for x in (c,s,t) for a,b in zip(x,x[1:])):
        return False,'clock_not_monotone'
    dt=sorted(b-a for a,b in zip(s,s[1:]))
    if dt and not .001<=dt[len(dt)//2]<=1: return False,'time_not_seconds_scale'
    return True,'provisional_schema_only_requires_field_name_validation'
def evaluate():
    cases={}
    for flag,name in [(False,'counter_absent'),(True,'counter_enabled')]:
        fs=fixture(flag); rows=[convert(f) for f in fs]
        times=[float(r[1]) for r in rows]
        times=[t-times[0] for t in times]
        idx=nearest(times,[i/50 for i in range(251)])
        ok,reason=gate(rows)
        cases[name]={'fields':len(rows[0]),'column_2_key':list(fs[0])[1],
          'column_2_initial':rows[0][1], 'column_2_delta':times[1],
          'distinct_matched_tracker_samples':len(set(idx)),
          'matched_first_record':idx.count(0),'frame_count':251,
          'gate_accepts':ok,'gate_reason':reason,
          'left_mm_column_42_key':list(fs[0])[41],
          'left_mm_col_42_value':rows[0][41]}
    shifted=[]
    for f in fixture(True):
        g=OrderedDict((k,v) for k,v in f.items() if k!='FPOGX')
        g['SPARE']='0'
        shifted.append(g)
    rows=[convert(f) for f in shifted]
    ok,reason=gate(rows)
    cases['counter_present_shifted']={
      'classification':'adversarial_fixture; not observed in released data',
      'column_2_key':list(shifted[0])[1],'fields':len(rows[0]),
      'gate_accepts':ok,'gate_reason':reason,
      'left_mm_column_42_key':list(shifted[0])[41]}
    assert cases['counter_enabled']['distinct_matched_tracker_samples']==251
    assert cases['counter_absent']['distinct_matched_tracker_samples']==1
    assert cases['counter_present_shifted']['gate_accepts']
    assert cases['counter_present_shifted']['left_mm_column_42_key']=='LPMMV'
    return {'experiment':'E002-168',
      'classification':'source-level conditional audit; synthetic fixtures',
      'cases':cases}
if __name__=='__main__': print(json.dumps(evaluate(),indent=2,sort_keys=True))
