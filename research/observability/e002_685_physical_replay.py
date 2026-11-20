"""E002-685 physical replay, stdlib only. Authentication must be independently established."""
import csv,json,math,sys
KEYS=('left','right','threshold','velocity_ceiling','gap_upper','reference_min','reference_error')
def replay(rows):
 out=[]
 for r in rows:
  try:
   z={k:float(r[k]) for k in KEYS}
   if any(not math.isfinite(x) or x<0 for x in z.values()): raise ValueError('invalid physical value')
   if r.get('authenticated')!='external_verified':
    out.append(dict(trial=r.get('trial','?'),decision='ABSTAIN_UNAUTHENTICATED'));continue
   a,b,c,v,h,m,e=(z[k] for k in KEYS)
   if abs(a-b)>v*h+1e-12: raise ValueError('endpoint violates velocity bound')
   bound=max(0,(a+b-v*h)/2)
   decision='EXCLUDE_CLOSURE' if bound>c else 'ABSTAIN'
   truth='CLOSED' if m+e<=c else ('OPEN' if m-e>c else 'INDETERMINATE')
   out.append(dict(trial=r.get('trial','?'),phase=r.get('phase','unspecified'),decision=decision,truth=truth,lower_bound=bound,false_exclusion=decision=='EXCLUDE_CLOSURE' and truth=='CLOSED'))
  except (ValueError,KeyError,TypeError) as exc:
   out.append(dict(trial=r.get('trial','?'),decision='ABSTAIN_INVALID',reason=str(exc)))
 return dict(rows=out,holdout_false_exclusions=sum(x.get('false_exclusion',False) for x in out if x.get('phase')=='holdout'))
def selftest():
 def row(**kw):
  r=dict(trial='t',phase='holdout',left='1',right='1',threshold='.2',velocity_ceiling='10',gap_upper='.05',reference_min='.7',reference_error='.01',authenticated='external_verified');r.update(kw);return r
 assert replay([row()])['rows'][0]['decision']=='EXCLUDE_CLOSURE'
 assert replay([row(reference_min='0',reference_error='0')])['holdout_false_exclusions']==1
 assert replay([row(gap_upper='.2')])['rows'][0]['decision']=='ABSTAIN'
 assert replay([row(authenticated='self')])['rows'][0]['decision']=='ABSTAIN_UNAUTHENTICATED'
 assert replay([row(right='0')])['rows'][0]['decision']=='ABSTAIN_INVALID'
 assert replay([row(reference_min='.2',reference_error='.1')])['rows'][0]['truth']=='INDETERMINATE'
 print('six synthetic selftests passed')
if __name__=='__main__':
 if len(sys.argv)==1:selftest()
 else:
  with open(sys.argv[1],newline='') as f:print(json.dumps(replay(list(csv.DictReader(f))),indent=2))
