#!/usr/bin/env python3
"""Independent XML-based checker. Does not import audit.py."""
import json,sys
from xml.etree import ElementTree as ET
K=('TIME TIME_TICK FPOGX FPOGY FPOGS FPOGD FPOGID FPOGV '
'LPOGX LPOGY LPOGV RPOGX RPOGY RPOGV BPOGX BPOGY BPOGV '
'LPCX LPCY LPD LPS LPV RPCX RPCY RPD RPS RPV '
'LEYEX LEYEY LEYEZ LPUPILD LPUPILV REYEX REYEY REYEZ RPUPILD RPUPILV '
'BKID BKDUR BKPMIN LPMM LPMMV RPMM RPMMV PIXX PIXY PIXS PIXV').split()
def fields(counter):
    attrs=([('CNT','1484')] if counter else [])+[(k,'1') for k in K]
    return list(ET.fromstring('<REC '+' '.join(f'{k}="{v}"' for k,v in attrs)+' />').attrib)
def verify(d):
    a,b=fields(True),fields(False)
    assert len(a)==49 and len(b)==48
    assert (a[1],a[41])==('TIME','LPMM')
    assert (b[1],b[41])==('TIME_TICK','LPMMV')
    x=d['cases']
    assert x['counter_enabled']['distinct_matched_tracker_samples']==251
    assert x['counter_absent']['distinct_matched_tracker_samples']==1
    assert x['counter_absent']['matched_first_record']==251
    assert x['counter_enabled']['column_2_key']==a[1]
    assert x['counter_absent']['column_2_key']==b[1]
    shifted=[k for k in a if k!='FPOGX']+['SPARE']
    assert len(shifted)==49 and shifted[41]=='LPMMV'
    assert x['counter_present_shifted']['left_mm_column_42_key']==shifted[41]
    assert x['counter_present_shifted']['gate_accepts']
    assert 10_000_000//50>2*5
    return {'status':'PASS','checked_cases':3,
       'independent_parser':'xml.etree.ElementTree',
       'source_parser_reused':False,'source_data':'synthetic_fixture_only'}
if __name__=='__main__':
    with open(sys.argv[1] if len(sys.argv)>1 else 'RESULTS.json') as f: data=json.load(f)
    print(json.dumps(verify(data),sort_keys=True))
