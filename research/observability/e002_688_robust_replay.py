"""E002-688: interval endpoint physical replay; conditional gate, not validation."""
import csv,json,math,sys
FIELDS=('left_low','left_high','right_low','right_high','threshold','velocity_ceiling','gap_upper','reference_min','reference_error')
def evaluate(r):
 trial=r.get('trial','?')
 try:
  if r.get('authenticated')!='external_verified':return dict(trial=trial,decision='ABSTAIN_UNAUTHENTICATED')
  z={k:float(r[k]) for k in FIELDS}
  if any(not math.isfinite(x) or x<0 for x in z.values()):raise ValueError('invalid value')
  al,au,bl,bu,c,v,h,m,e=(z[k] for k in FIELDS)
  if al>au or bl>bu:raise ValueError('reversed interval')
  d=v*h
  if not math.isfinite(d):raise ValueError('overflow')
  if al>bu+d or bl>au+d:return dict(trial=trial,decision='ABSTAIN_INCONSISTENT')
  a=max(al,bl-d);b=max(bl,al-d)
  if a>au or b>bu or abs(a-b)>d:return dict(trial=trial,decision='ABSTAIN_INCONSISTENT')
  lower=max(0,(a+b-d)/2)
  decision='EXCLUDE_CLOSURE' if math.isfinite(lower) and math.nextafter(c,math.inf)<lower else 'ABSTAIN'
  truth='CLOSED' if m+e<=c else ('OPEN' if m-e>c else 'INDETERMINATE')
  return dict(trial=trial,phase=r.get('phase','unspecified'),decision=decision,truth=truth,lower_bound=lower,false_exclusion=decision=='EXCLUDE_CLOSURE' and truth=='CLOSED')
 except (ValueError,KeyError,TypeError,OverflowError) as exc:return dict(trial=trial,decision='ABSTAIN_INVALID',reason=str(exc))
def replay(rows):
 out=[evaluate(r) for r in rows]
 return dict(rows=out,holdout_false_exclusions=sum(x.get('false_exclusion',False) for x in out if x.get('phase')=='holdout'))
def selftest():
 base=dict(trial='t',phase='holdout',left_low='1',left_high='1',right_low='1',right_high='1',threshold='.25',velocity_ceiling='1',gap_upper='1',reference_min='.8',reference_error='0',authenticated='external_verified')
 def check(changes,expected):
  actual=evaluate(dict(base,**changes))['decision']
  assert actual==expected,(changes,actual,expected)
 check({},'EXCLUDE_CLOSURE')
 check(dict(left_low='.5',right_low='.5'),'ABSTAIN')
 check(dict(left_low='2.1',left_high='2.1'),'ABSTAIN_INCONSISTENT')
 check(dict(left_low='nan'),'ABSTAIN_INVALID')
 check(dict(authenticated='self'),'ABSTAIN_UNAUTHENTICATED')
 check(dict(threshold='.5'),'ABSTAIN')
 check(dict(reference_min='0'),'EXCLUDE_CLOSURE')
 assert replay([dict(base,reference_min='0')])['holdout_false_exclusions']==1
 print('8 synthetic assertions passed')
if __name__=='__main__':
 if len(sys.argv)==1:selftest()
 else:
  with open(sys.argv[1],newline='') as f:print(json.dumps(replay(csv.DictReader(f)),indent=2))
