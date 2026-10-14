"""Independent, separate tri-state check of fixed shortlist."""
import json,pathlib
P=pathlib.Path(__file__).resolve().parent
rows=json.loads((P/'CANDIDATES.json').read_text())
fields=('rgb_video','tracker_diameter','native_unfolded_time','schema_verified','verified_paired_access','participant_holdout')
assert len(rows)==7
assert sum(all(r[k] is True for k in fields) for r in rows)==0
assert any(r['id']=='js_meye_2025' and r['prior_art_collision'] and r['verified_paired_access'] is False for r in rows)
assert any(r['id']=='meye_2021_zenodo' and r['rgb_video'] is False for r in rows)
assert len({r['id'] for r in rows})==len(rows)
print('PASS_7_CANDIDATES_TRI_STATE_INDEPENDENT')
