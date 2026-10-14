"""E002-174: source eligibility only; no physiological estimates."""
import json,hashlib,pathlib
P=pathlib.Path(__file__).resolve().parent
K=('rgb_video','tracker_diameter','native_unfolded_time','schema_verified','verified_paired_access','participant_holdout')
def classify(x):
    vals=[x[k] for k in K]
    assert all(v is True or v is False or v is None for v in vals)
    return 'ELIGIBLE' if all(v is True for v in vals) else ('BLOCKED' if False in vals else 'UNRESOLVED')
def main():
    raw=(P/'CANDIDATES.json').read_bytes()
    rows=json.loads(raw)
    assert len(rows)==7 and len(set(r['id'] for r in rows))==7
    result={'n_candidates':len(rows),'n_verified_eligible':sum(classify(r)=='ELIGIBLE' for r in rows),
      'statuses':{r['id']:classify(r) for r in rows},
      'prior_art_collisions':[r['id'] for r in rows if r['prior_art_collision']],
      'manifest_sha256':hashlib.sha256(raw).hexdigest()}
    print(json.dumps(result,sort_keys=True))
    assert result['n_verified_eligible']==0
if __name__=='__main__': main()
